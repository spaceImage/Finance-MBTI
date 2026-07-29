"""
온통청년(한국고용정보원) 청년정책 오픈API 클라이언트.

✅ 실제 응답으로 확정된 사실 (2026-07-29):
   - 요청 URL: https://www.youthcenter.go.kr/go/ythip/getPlcy
   - 파라미터: apiKeyNm(인증키), pageNum, pageSize, rtnType=json, lclsfNm(정책대분류)
   - 응답 골격: result.youthPolicyList (배열)
   - 정책명 필드: plcyNm / 설명 필드: plcyExplnCn
   - 분류 필드: lclsfNm(대분류, 예: "금융･복지･문화") / mclsfNm(중분류, 예: "취약계층 및 금융지원")
   - 나이 필드: sprtTrgtMinAge, sprtTrgtMaxAge (숫자로 구조화되어 있음 — kinfa의 자유텍스트 age와 다름)

✅ plcyKywdNm은 자유 검색어가 아니라 "대출/보조금/주거지원" 같은 정해진 태그값만 받는
   파라미터로 보인다 (자유 텍스트 "청년 금융"을 넣었더니 사실상 무시되고 전체 결과가 왔음).
   대신 mclsfNm(중분류)이 "취약계층 및 금융지원"으로 정확히 분류돼 있어서,
   이 프로젝트에서는 키워드 정규식 대신 이 카테고리 값으로 필터링한다.
"""
import time
import logging
import httpx

from app.config import settings

logger = logging.getLogger("dotori")

BASE_URL = "https://www.youthcenter.go.kr/go/ythip/getPlcy"
CACHE_TTL_SECONDS = 6 * 60 * 60

_cache: dict[str, tuple[float, list[dict]]] = {}

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}

# 실제 응답에서 확인된, 금융지원 성격 정책들의 정확한 중분류 값
FINANCE_MCLSF_NAME = "취약계층 및 금융지원"
# 서버 요청 단계에서부터 범위를 좁히는 대분류 값 (금융+복지+문화가 묶여있어 완전히
# 좁히진 못하지만, 2,691건 전체를 받는 것보다는 훨씬 적게 받아올 수 있다)
FINANCE_LCLSF_NAME = "금융･복지･문화"


def _extract_policy_list(payload: dict) -> list[dict]:
    result = payload.get("result", {})
    policy_list = result.get("youthPolicyList", [])
    if isinstance(policy_list, list):
        return policy_list

    logger.error(f"[YOUTHCENTER] 응답에서 정책 리스트를 못 찾음. 최상위 키: {list(payload.keys())}")
    return []


def fetch_raw_policies(lclsf_nm: str = FINANCE_LCLSF_NAME, page_size: int = 100) -> list[dict]:
    """
    lclsf_nm: 정책대분류명으로 서버 단에서 1차로 좁힌다.
    """
    cache_key = f"youthcenter:{lclsf_nm}:{page_size}"
    now = time.time()

    cached = _cache.get(cache_key)
    if cached and (now - cached[0] < CACHE_TTL_SECONDS):
        return cached[1]

    if not settings.YOUTHCENTER_API_KEY:
        logger.info("[YOUTHCENTER] API 키 미설정 — 조회를 건너뜁니다.")
        return []

    try:
        resp = httpx.get(
            BASE_URL,
            params={
                "apiKeyNm": settings.YOUTHCENTER_API_KEY,
                "pageNum": 1,
                "pageSize": page_size,
                "rtnType": "json",
                "lclsfNm": lclsf_nm,
            },
            headers=_BROWSER_HEADERS,
            follow_redirects=True,
            timeout=10.0,
        )
        if resp.status_code >= 400:
            logger.error(f"[YOUTHCENTER] API 에러 응답 본문: {resp.text[:1000]}")
        resp.raise_for_status()

        payload = resp.json()
        policy_list = _extract_policy_list(payload)

        _cache[cache_key] = (now, policy_list)
        return policy_list

    except Exception as e:
        logger.error(f"[YOUTHCENTER] API 호출 실패: {e}")
        return cached[1] if cached else []


YOUTHCENTER_NAME_FIELD = "plcyNm"
YOUTHCENTER_DESC_FIELD = "plcyExplnCn"

# ✅ 2026-07-29, 37건 검수로 확정된 지역명 목록.
# 지역 한정 정책은 "그 지역 거주자만" 대상이라, 우리 서비스는 지역 정보를
# 별도로 받지 않는 구조라 애초에 매칭이 불가능하다. 이름+설명에 지역명이
# 하나라도 들어가면 제외한다.
REGION_KEYWORDS = [
    # 광역자치단체 (정식명 + 흔히 쓰는 축약형)
    "서울특별시", "서울", "부산광역시", "부산", "대구광역시", "대구",
    "인천광역시", "인천", "광주광역시", "광주", "대전광역시", "대전",
    "울산광역시", "울산", "세종특별자치시", "세종",
    "경기도", "경기", "강원특별자치도", "강원",
    "충청북도", "충북", "충청남도", "충남",
    "전북특별자치도", "전북", "전라남도", "전남",
    "경상북도", "경북", "경상남도", "경남", "제주특별자치도", "제주",
    # 실제 데이터에서 발견된 기초자치단체(시/군)
    "태안", "서산", "아산", "공주", "부여", "홍성", "삼척",
]


def _mentions_region(policy: dict) -> bool:
    """정책명 + 설명을 합쳐서 지역명이 하나라도 포함되는지 검사."""
    combined = f"{policy.get(YOUTHCENTER_NAME_FIELD, '')} {policy.get(YOUTHCENTER_DESC_FIELD, '')}"
    return any(region in combined for region in REGION_KEYWORDS)


def fetch_finance_youth_policies() -> list[dict]:
    """
    lclsfNm="금융･복지･문화"로 1차로 좁혀서 받아온 뒤,
    mclsfNm(중분류)이 정확히 "취약계층 및 금융지원"인 것만 남기고,
    그중에서도 지역명이 언급된(=특정 지역 거주자만 대상인) 정책은 제외한다.
    """
    raw = fetch_raw_policies(lclsf_nm=FINANCE_LCLSF_NAME)
    finance_only = [p for p in raw if p.get("mclsfNm") == FINANCE_MCLSF_NAME]
    return [p for p in finance_only if not _mentions_region(p)]