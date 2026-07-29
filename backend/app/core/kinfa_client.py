"""
서민금융진흥원 / 공공데이터포털(data.go.kr) API 클라이언트.

✅ 필드명 확정됨 (2026-07-29, 실제 응답으로 검증 완료):
   - 상품명: finprdnm
   - 대상 카테고리: trgt, tgtFltr (예: "대학생·청년", "소상공인" 등)
   - 나이 조건: age (예: "35세 이하", "19~69세", "없음")
   - 상세 지원조건: suprtgtdtlcond (자유 텍스트, 나이/자격 조건 포함)

⚠️ 응답 포맷은 JSON이 아니라 XML이다. (공공데이터포털 상세페이지의 "데이터포맷: XML" 표기가 맞았음)
⚠️ 엔드포인트 경로에 서비스명이 두 번 들어간다 (공공데이터포털에서 실제로 승인된 구조 그대로):
   /B553701/LoanProductSearchingInfo/LoanProductSearchingInfo/getLoanProductSearchingInfo
"""
import time
import logging
import httpx
import xml.etree.ElementTree as ET

from app.config import settings
from app.core.keyword_filter import filter_youth_products

logger = logging.getLogger("dotori")

# 서민금융진흥원_대출상품한눈에 정보 서비스 (실제 승인된 요청 URL로 확인된 경로 — 서비스명이 두 번 들어감)
BASE_URL = "https://apis.data.go.kr/B553701/LoanProductSearchingInfo/LoanProductSearchingInfo"
OPERATION = "getLoanProductSearchingInfo"

CACHE_TTL_SECONDS = 6 * 60 * 60
_cache: dict[str, tuple[float, list[dict]]] = {}


def _parse_xml_items(xml_text: str) -> list[dict]:
    """XML 응답을 파싱해서 item 하나당 dict 하나로 변환한다."""
    root = ET.fromstring(xml_text)

    result_code = root.findtext("header/resultCode")
    if result_code is not None and result_code != "00":
        result_msg = root.findtext("header/resultMsg")
        logger.error(f"[KINFA] API 에러 응답: {result_code} {result_msg}")
        return []

    items = []
    for item_el in root.findall("body/items/item"):
        item = {child.tag: (child.text or "") for child in item_el}
        items.append(item)
    return items


def fetch_raw_products(page_no: int = 1, num_rows: int = 500) -> list[dict]:
    """
    원본 상품 리스트를 그대로 반환 (필터링 없음).
    전체 상품이 총 300여 건 수준이라, 페이지네이션 없이 한 번에 넉넉히(500건) 받아온다.
    """
    cache_key = f"kinfa:{page_no}:{num_rows}"
    now = time.time()

    cached = _cache.get(cache_key)
    if cached and (now - cached[0] < CACHE_TTL_SECONDS):
        return cached[1]

    if not settings.KINFA_API_KEY:
        logger.info("[KINFA] API 키 미설정 — 조회를 건너뜁니다.")
        return []

    try:
        resp = httpx.get(
            f"{BASE_URL}/{OPERATION}",
            params={
                "serviceKey": settings.KINFA_API_KEY,  # 디코딩 키 (httpx가 알아서 인코딩)
                "pageNo": page_no,
                "numOfRows": num_rows,
            },
            timeout=15.0,
        )
        resp.raise_for_status()

        item_list = _parse_xml_items(resp.text)
        _cache[cache_key] = (now, item_list)
        return item_list

    except Exception as e:
        logger.error(f"[KINFA] API 호출 실패: {e}")
        return cached[1] if cached else []


KINFA_NAME_FIELD = "finprdnm"

# keyword_filter.py는 필드 하나만 검사하므로, 여러 필드(대상/나이/상세조건)를 합쳐서
# 하나의 "가상 필드"로 만들어 전달한다.
KINFA_ELIGIBILITY_FIELD = "_eligibility_text"


def _with_combined_eligibility(item: dict) -> dict:
    parts = [
        item.get("trgt", ""),
        item.get("tgtFltr", ""),
        item.get("age", ""),
        item.get("suprtgtdtlcond", ""),
    ]
    combined = " ".join(p for p in parts if p and p != "-" and p != "없음")
    return {**item, KINFA_ELIGIBILITY_FIELD: combined}


# ✅ 2026-07-29, 전체 318건 검수(워크플로우 6단계)로 확정된 오탐 목록.
# 전부 "가입대상 텍스트에서 청년/연령 조건 발견"으로 걸렸지만, 실제 trgt/age를 보면
# 사업자·소상공인·중소기업 대상 상품이다. suprtgtdtlcond 안에 "청년 고용 시 우대금리" 같은
# 부가조건으로만 "청년"이 등장해서 걸린 것으로 판단, 이름으로 직접 제외한다.
KNOWN_FALSE_POSITIVES = [
    "서울시 중소기업 육성자금 지원(운전_창업기업자금)",
    "서울시 중소기업 육성자금 지원(운전_일자리창출우수기업자금)",
    "징검다리론",
    "충청북도 출산 장려 정책’ 활성화 등 지원 특별보증",
    "전북 기술창업 활성화 특례보증",
    "충북 스타트업 활성화 지원 특별보증",
    "경기도 중소기업 육성자금(운전_일자리창출기업)",
]


def fetch_youth_filtered_loan_products() -> list[dict]:
    """서민금융 대출상품 중 청년 키워드/나이조건에 걸리는 것만 반환. (검수된 오탐 7건은 제외)"""
    raw = fetch_raw_products()
    enriched = [_with_combined_eligibility(item) for item in raw]
    return filter_youth_products(
        enriched, KINFA_NAME_FIELD, KINFA_ELIGIBILITY_FIELD,
        exclude_names=KNOWN_FALSE_POSITIVES,
    )