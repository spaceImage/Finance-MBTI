"""
서로 다른 API(금감원 금융상품통합, 서민금융진흥원 등)의 원본 상품 리스트에서
"청년 상품"만 걸러내는 범용 필터.

API마다 필드명이 다르므로, 이 모듈은 필드명을 몰라도 되게 설계했다.
호출하는 쪽(finlife_client, kinfa_client 등)이 "상품명 필드"와
"가입대상/신청대상 텍스트 필드"의 키 이름만 알려주면 된다.

⚠️ 키워드 매칭은 100% 정확할 수 없다. 워크플로우 6~7단계(오탐 검수 + 화이트/블랙리스트 보정)를
반드시 거쳐야 하며, 아래 EXCLUDE_KEYWORDS는 그 안전장치의 시작점일 뿐이다.
"""
import re

# 상품명에 이 단어가 있으면 바로 청년상품으로 인정
NAME_KEYWORDS = ["청년"]

# 가입대상/신청대상 텍스트에 이 단어가 있으면 청년상품 후보로 인정
ELIGIBILITY_KEYWORDS = ["청년", "만 19세", "만 34세"]

# 나이 범위 패턴: "19~26세", "만 19세 ~ 26세", "26세 이하" 등을 잡아낸다
AGE_RANGE_PATTERN = re.compile(r"(19|2[0-6])\s*[~\-]\s*(19|2[0-6])\s*세")
AGE_UNDER_PATTERN = re.compile(r"(19|2[0-6])\s*세\s*(이하|미만)")

# 나이 조건이 걸려도 청년 취지가 아닌 게 명백한 경우 (오탐 방지용 블랙리스트)
# 실제 검수하면서 여기에 계속 추가해나가는 게 정상적인 운영 방식
EXCLUDE_KEYWORDS = ["65세 이상", "노인", "시니어", "기초연금"]


def _clean_text(text: str) -> str:
    """줄바꿈·중복 공백 등을 정리 (워크플로우 4단계: 텍스트 전처리)"""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


# 나이 패턴 뒤에 이 단어가 가까이 있으면 "청년 조건"이 아니라 "청년 제외 조건"일 가능성이 높다.
# 예: "만 35세 미만 단독세대주 제외" → 35세 미만을 오히려 배제한다는 뜻
NEGATION_WINDOW = 10  # 나이 패턴 끝난 지점부터 이 글자 수 이내에서 검사


def _age_signal_found(text: str) -> bool:
    for pattern in (AGE_RANGE_PATTERN, AGE_UNDER_PATTERN):
        for m in pattern.finditer(text):
            after = text[m.end(): m.end() + NEGATION_WINDOW]
            if "제외" not in after:
                return True
    return False


def _has_youth_signal(text: str) -> bool:
    text = _clean_text(text)
    if not text:
        return False
    if any(kw in text for kw in ELIGIBILITY_KEYWORDS):
        return True
    return _age_signal_found(text)


def _is_excluded(text: str) -> bool:
    text = _clean_text(text)
    return any(kw in text for kw in EXCLUDE_KEYWORDS)


def filter_youth_products(
    products: list[dict],
    name_field: str,
    eligibility_field: str,
    exclude_names: list[str] | None = None,
) -> list[dict]:
    """
    products: API에서 받은 원본 상품 리스트 (딕셔너리 리스트)
    name_field: 상품명이 들어있는 키 이름 (예: finlife의 'fin_prdt_nm')
    eligibility_field: 가입대상 텍스트가 들어있는 키 이름 (예: finlife의 'join_member')
    exclude_names: 오탐 검수(워크플로우 6단계)로 확정된, 이름으로 직접 제외할 상품명 목록.
                   (예: 상세조건 텍스트에 "청년 고용 우대" 같은 부가조건으로만 "청년"이 등장해
                   걸린, 실제로는 기업 대상 상품)

    반환: 청년 상품으로 판단된 항목만 담긴 리스트. 각 항목에는
          "_match_reason" 필드를 추가해서 왜 걸렸는지(상품명/가입대상) 표시한다.
          → 이 필드는 6단계(오탐 검수) 할 때 사람이 빠르게 이유를 확인하기 위한 것.
    """
    exclude_names = set(exclude_names or [])
    matched = []
    for p in products:
        name = _clean_text(p.get(name_field, ""))
        eligibility = _clean_text(p.get(eligibility_field, ""))

        if name in exclude_names:
            continue

        if _is_excluded(eligibility) or _is_excluded(name):
            continue

        if any(kw in name for kw in NAME_KEYWORDS):
            matched.append({**p, "_match_reason": "상품명에 '청년' 포함"})
            continue

        if _has_youth_signal(eligibility):
            matched.append({**p, "_match_reason": "가입대상 텍스트에서 청년/연령 조건 발견"})

    return matched