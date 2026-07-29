"""
금융감독원 "금융상품한눈에" 오픈API 클라이언트.

- API 키가 없거나 호출이 실패해도 서비스 전체가 죽지 않도록,
  빈 리스트를 반환하고 상위 로직(mapper.py)에서 기존 정적 데이터로 Fallback한다.
- 같은 데이터를 요청마다 실시간으로 다시 받아오지 않도록 메모리 캐시(TTL 6시간)를 둔다.
"""
import time
import logging
import httpx

from app.config import settings

logger = logging.getLogger("dotori")

from app.core.keyword_filter import filter_youth_products

BASE_URL = "https://finlife.fss.or.kr/finlifeapi"
CACHE_TTL_SECONDS = 6 * 60 * 60  # 6시간마다 갱신

# {cache_key: (저장시각, 데이터)}
_cache: dict[str, tuple[float, list[dict]]] = {}


def _merge_base_and_option(base_list: list[dict], option_list: list[dict]) -> list[dict]:
    """
    API는 상품 기본정보(baseList)와 금리옵션(optionList)을 분리해서 내려준다.
    fin_prdt_cd(상품코드) 기준으로 묶어서 상품 하나당 옵션 리스트를 붙여준다.
    """
    options_by_code: dict[str, list[dict]] = {}
    for opt in option_list:
        code = opt.get("fin_prdt_cd")
        options_by_code.setdefault(code, []).append(opt)

    merged = []
    for base in base_list:
        code = base.get("fin_prdt_cd")
        merged.append({**base, "options": options_by_code.get(code, [])})
    return merged


def _cached_or_fetch(cache_key: str, url: str, params: dict) -> list[dict]:
    now = time.time()

    cached = _cache.get(cache_key)
    if cached and (now - cached[0] < CACHE_TTL_SECONDS):
        return cached[1]

    if not settings.FINLIFE_API_KEY:
        logger.info("[FINLIFE] API 키 미설정 — 실시간 금리 조회를 건너뜁니다.")
        return []

    try:
        resp = httpx.get(url, params=params, timeout=5.0)
        resp.raise_for_status()
        payload = resp.json()
        result = payload.get("result", {})

        # 인증키 오류 등은 200으로 응답하되 err_cd로 알려주는 경우가 있어 별도 확인
        err_cd = result.get("err_cd")
        if err_cd and err_cd != "000":
            logger.error(f"[FINLIFE] API 에러 응답: {err_cd} {result.get('err_msg')}")
            return cached[1] if cached else []

        merged = _merge_base_and_option(
            result.get("baseList", []),
            result.get("optionList", []),
        )
        _cache[cache_key] = (now, merged)
        return merged

    except Exception as e:
        logger.error(f"[FINLIFE] API 호출 실패({cache_key}): {e}")
        # 실패 시, 예전 캐시라도 남아있으면 그거라도 반환 (완전 공백보다 낫다)
        return cached[1] if cached else []


def fetch_deposit_products(top_fin_grp_no: str) -> list[dict]:
    """정기예금 상품 목록 조회 (캐시 적용)"""
    cache_key = f"deposit:{top_fin_grp_no}"
    url = f"{BASE_URL}/depositProductsSearch.json"
    params = {"auth": settings.FINLIFE_API_KEY, "topFinGrpNo": top_fin_grp_no, "pageNo": 1}
    return _cached_or_fetch(cache_key, url, params)


def fetch_saving_products(top_fin_grp_no: str) -> list[dict]:
    """적금(수시입출금 포함) 상품 목록 조회 (캐시 적용)"""
    cache_key = f"saving:{top_fin_grp_no}"
    url = f"{BASE_URL}/savingProductsSearch.json"
    params = {"auth": settings.FINLIFE_API_KEY, "topFinGrpNo": top_fin_grp_no, "pageNo": 1}
    return _cached_or_fetch(cache_key, url, params)


# 필터링 대상 업권 코드. (⚠️ 인증키로 첫 호출 후 kor_co_nm 값으로 맞는지 검증 필요)
TOP_FIN_GRP_CODES = {
    "은행": "020000",
    "저축은행": "030200",
}

# finlife API의 실제 필드명 (공식 문서 기준 통용되는 이름)
FINLIFE_NAME_FIELD = "fin_prdt_nm"        # 상품명
FINLIFE_ELIGIBILITY_FIELD = "join_member"  # 가입대상 텍스트


def _dedupe_by_code(products: list[dict]) -> list[dict]:
    """fin_prdt_cd 기준 중복 제거 (같은 상품이 여러 업권 코드에 겹쳐 잡히는 경우 대비)"""
    seen = set()
    deduped = []
    for p in products:
        code = p.get("fin_prdt_cd")
        if code and code in seen:
            continue
        if code:
            seen.add(code)
        deduped.append(p)
    return deduped


def fetch_youth_filtered_products() -> dict[str, list[dict]]:
    """
    은행권 + 저축은행권의 정기예금·적금 전체를 모아 청년 키워드 필터를 적용한다.
    반환 형식: {"deposit": [...], "saving": [...]}

    ⚠️ 매 요청마다 부르지 말고, 하루 1회 정도 배치로 호출해서 결과를 캐시/DB에
       저장해두는 방식을 권장한다 (기존 fetch_*_products가 이미 6시간 캐시를 갖고 있어
       최소한의 안전장치는 되어 있음).
    """
    all_deposits = []
    all_savings = []
    for group_code in TOP_FIN_GRP_CODES.values():
        all_deposits.extend(fetch_deposit_products(group_code))
        all_savings.extend(fetch_saving_products(group_code))

    all_deposits = _dedupe_by_code(all_deposits)
    all_savings = _dedupe_by_code(all_savings)

    return {
        "deposit": filter_youth_products(all_deposits, FINLIFE_NAME_FIELD, FINLIFE_ELIGIBILITY_FIELD),
        "saving": filter_youth_products(all_savings, FINLIFE_NAME_FIELD, FINLIFE_ELIGIBILITY_FIELD),
    }
