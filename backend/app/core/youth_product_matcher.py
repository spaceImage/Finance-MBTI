"""
16가지 도토리 유형(types.json)에 이미 큐레이션된 "실제 은행 상품명"을 화이트리스트로 두고,
금융감독원 금융상품한눈에 API 응답에서 같은 상품을 찾아 실시간 금리를 붙여주는 모듈.

⚠️ 범위 제한:
  - 금감원 예·적금 API는 "은행권 예금·적금"만 다룬다.
  - ETF(KODEX, TIGER), 로보어드바이저(파운트, 핀트), 증권사 PB형 ELS는
    이 API 범위 밖이라 실시간 연동 대상이 아니다. → 금리는 항상 정적 데이터 그대로 노출된다.
  - 즉, 16유형 중 은행 예·적금 상품인 5개 유형만 실시간 금리가 붙고,
    나머지 11개 유형은 기존처럼 정적 설명이 그대로 나가는 게 정상 동작이다.
  - 단, 공식 홈페이지 링크(get_product_url)는 금리와 별개로 ETF·로보어드바이저 4개
    상품에도 정적으로 붙어있다. "증권사 PB 추천형 ELS"만 특정 상품명이 없어 링크가 없다.

⚠️ topFinGrpNo(업권 코드)는 finlife 문서 기준 추정치이며,
   실제 인증키로 첫 호출을 해본 뒤 반환되는 kor_co_nm으로 은행이 맞게 잡히는지
   반드시 확인이 필요하다. (틀렸다면 이 상수만 바꾸면 된다)
"""
import logging
from app.core.finlife_client import fetch_deposit_products, fetch_saving_products

logger = logging.getLogger("dotori")

TOP_FIN_GRP_BANK = "020000"          # 은행 (카카오뱅크·케이뱅크·토스뱅크·전북은행 포함 추정)
TOP_FIN_GRP_SAVINGS_BANK = "030200"  # 저축은행 (OK저축은행 포함 추정)

# types.json의 financial_product 문자열과 대조할 "은행명 키워드 + 상품명 키워드" 화이트리스트.
# 이 리스트에 없는 상품(ETF, 로보어드바이저 등)은 애초에 매칭 시도조차 하지 않는다.
#
# ⚠️ product_url은 금감원 API가 아니라 각 은행 공식 홈페이지에서 직접 확인한 값이다
# (2026-07-30). 금감원 "금융상품한눈에" API 자체에는 상품 상세페이지 URL 필드가 없어서,
# 실시간 API로는 절대 채울 수 없는 값 — 정적으로 큐레이션해서 하드코딩한다.
# 전북은행만 공개된 "씨드모아통장" 전용 딥링크를 찾지 못해 은행 홈페이지로 대체했다.
YOUTH_PRODUCT_WHITELIST = [
    {
        "bank_keyword": "토스뱅크", "product_keyword": "토스뱅크 통장",
        "group": TOP_FIN_GRP_BANK, "kind": "saving",
        "product_url": "https://www.tossbank.com/product-service/savings/account",
    },
    {
        "bank_keyword": "케이뱅크", "product_keyword": "플러스박스",
        "group": TOP_FIN_GRP_BANK, "kind": "saving",
        "product_url": "https://www.kbanknow.com/ib20/mnu/FPMDPT130100?phashid=vxCheBJ",
    },
    {
        "bank_keyword": "카카오뱅크", "product_keyword": "세이프박스",
        "group": TOP_FIN_GRP_BANK, "kind": "saving",
        "product_url": "https://www.kakaobank.com/products/safeboxes",
    },
    {
        "bank_keyword": "전북은행", "product_keyword": "씨드모아",
        "group": TOP_FIN_GRP_BANK, "kind": "saving",
        "product_url": "https://www.jbbank.co.kr/",
    },
    {
        "bank_keyword": "OK저축은행", "product_keyword": "OK짠테크",
        "group": TOP_FIN_GRP_SAVINGS_BANK, "kind": "saving",
        "product_url": "https://m.oksavingsbank.com/product/withdraw/free.jsp",
    },
]

# ETF·로보어드바이저 상품은 finlife API 범위 밖이라 실시간 금리 연동 대상이 아니지만,
# 공식 홈페이지 URL 자체는 은행 상품과 동일하게 정적으로 큐레이션해서 붙여줄 수 있다.
# (2026-07-30, 검색+실접속 확인 완료)
#
# ⚠️ "증권사 PB 추천형 ELS (주가연계증권)"(FVRI 유형)은 특정 증권사·상품명이 없는
# 일반 카테고리라 실제 상품 링크를 붙일 수가 없다. 대신 성향이 가장 가까운 PVRI
# 유형의 "핀트(Fint)" 로보어드바이저 링크로 대체한다 — 둘 다 "전문가 추천을 받아
# 투자한다"는 성격이 같고(코드상 V·R·I 공유, P/F만 다름), 핀트 역시 ELS를 포함한
# 다양한 자산군을 추천하는 서비스라 완전히 무관하진 않다. 다만 엄밀히는 ELS 전용
# 상품 링크가 아니라 "가장 가까운 대체 링크"라는 점은 분명히 해둔다.
STATIC_PRODUCT_URLS = [
    {"keyword": "KODEX 200", "product_url": "https://www.samsungfund.com/etf/product/view.do?id=2ETF01"},
    {
        "keyword": "TIGER 리츠부동산인프라",
        "product_url": "https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7329200000",
    },
    {"keyword": "파운트", "product_url": "https://fount.co/"},
    {"keyword": "핀트", "product_url": "https://fint.co.kr/"},
    {"keyword": "증권사 PB 추천형 ELS", "product_url": "https://fint.co.kr/"},
]


def _best_rate(product: dict) -> float | None:
    """상품의 옵션(만기/기간별 금리) 중 최고 우대금리를 찾는다. 우대금리가 없으면 기본금리를 쓴다."""
    rates = []
    for opt in product.get("options", []):
        rate = opt.get("intr_rate2") if opt.get("intr_rate2") is not None else opt.get("intr_rate")
        if isinstance(rate, (int, float)):
            rates.append(rate)
    return max(rates) if rates else None


def find_live_rate(bank_keyword: str, product_keyword: str, group: str, kind: str) -> dict | None:
    """화이트리스트 항목 하나에 대해 API 응답에서 동일 상품을 찾아 반환. 못 찾으면 None."""
    fetcher = fetch_saving_products if kind == "saving" else fetch_deposit_products
    products = fetcher(group)

    for p in products:
        bank_name = p.get("kor_co_nm", "")
        product_name = p.get("fin_prdt_nm", "")
        if bank_keyword in bank_name and product_keyword in product_name:
            rate = _best_rate(p)
            if rate is None:
                continue
            return {
                "bank_name": bank_name,
                "product_name": product_name,
                "interest_rate": rate,
            }
    return None


def get_product_url(financial_product_text: str) -> str | None:
    """
    화이트리스트(은행 예·적금) 또는 ETF·로보어드바이저용 정적 목록에 매칭되는
    상품의 공식 홈페이지 URL을 반환한다. 실시간 금리 조회(enrich_with_live_rate)와
    달리 API 키/호출 성공 여부와 무관하게 항상 반환된다 — 정적으로 큐레이션된 값이기 때문이다.
    """
    for entry in YOUTH_PRODUCT_WHITELIST:
        if entry["bank_keyword"] in financial_product_text and entry["product_keyword"] in financial_product_text:
            return entry.get("product_url")

    for entry in STATIC_PRODUCT_URLS:
        if entry["keyword"] in financial_product_text:
            return entry.get("product_url")

    return None


def enrich_with_live_rate(financial_product_text: str) -> dict | None:
    """
    financial_product_text: types.json의 financial_product 필드 원문
    (예: "토스뱅크 통장 — 조건 없이 연 3.5%, 자동이체 연동")

    화이트리스트와 일치하면 {"bank_name", "product_name", "interest_rate"} 반환.
    일치하지 않거나(ETF 등) API 호출에 실패하면 None — 이 경우 mapper.py가
    기존 정적 설명을 그대로 사용하므로 서비스 동작에는 영향이 없다.
    """
    for entry in YOUTH_PRODUCT_WHITELIST:
        if entry["bank_keyword"] in financial_product_text and entry["product_keyword"] in financial_product_text:
            try:
                return find_live_rate(
                    entry["bank_keyword"], entry["product_keyword"], entry["group"], entry["kind"]
                )
            except Exception as e:
                logger.error(f"[YOUTH_MATCH] 매칭 중 오류: {e}")
                return None
    return None
