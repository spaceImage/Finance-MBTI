from app.core.youth_product_matcher import enrich_with_live_rate, get_product_url
from app.core.youthcenter_client import pick_real_policy, extract_policy_url


def get_recommendations(mbti_code: str, calc_res: dict) -> list[dict]:
    """
    Returns actual financial product and government policy recommendation cards matching youth MBTI type.
    """
    financial_prod = calc_res.get("financial_product", "")
    policy = calc_res.get("government_policy", "")
    risk_color = calc_res.get("risk_color", "🟢")

    # 은행 예·적금 상품(토스뱅크/케이뱅크/카카오뱅크/전북은행/OK저축은행)이면
    # 금감원 API에서 실시간 금리를 찾아본다. ETF·로보어드바이저 등은 매칭 대상이 아니라 None 반환.
    live = enrich_with_live_rate(financial_prod)
    product_url = get_product_url(financial_prod)

    policy_name = policy.split(" — ")[0] if " — " in policy else policy
    # 온통청년 API에서 유형에 가장 가까운 실제 정책을 찾는다.
    # RED(위험 신호)일 때는 pick_real_policy 내부에서 대출성 정책을 먼저 제외한다.
    matched_policy = pick_real_policy(policy_name, risk_color)
    policy_url = extract_policy_url(matched_policy) if matched_policy else ""

    product_items = ["우대 금리 / 수시입출금 혜택", "자동이체 연동 저축 서비스", "안전 자산 관리"]
    if live:
        product_items = [f"실시간 최고 우대금리: 연 {live['interest_rate']}%"] + product_items

    return [
        {
            "id": 1,
            "category": "실제 금융상품",
            "name": financial_prod.split(" — ")[0] if " — " in financial_prod else financial_prod,
            "description": financial_prod.split(" — ")[1] if " — " in financial_prod else "맞춤형 우대 금리 및 안전 자산 운용",
            "tag": "실시간 금리" if live else "맞춤 금융",
            "risk_level": risk_color,
            "items": product_items,
            "is_live": bool(live),
            "url": product_url
        },
        {
            "id": 2,
            "category": "정부 청년정책",
            "name": policy_name,
            "description": policy.split(" — ")[1] if " — " in policy else "자립준비청년 전용 매칭 지원 및 자산형성",
            "tag": "정부 지원",
            "risk_level": "🟢 지원혜택",
            "items": ["정부 매칭 지원금 제공", "자립수당 연계 혜택", "청년 맞춤 가입조건"],
            "url": policy_url or None
        },
        {
            "id": 3,
            "category": "재정위기 맞춤 가이드",
            "name": calc_res.get("crisis_title", "재정위기 조기발견 자가진단"),
            "description": calc_res.get("crisis_advice", "위기 상황 대비 가이드"),
            "tag": calc_res.get("crisis_guide", "자립상담 지원"),
            "risk_level": risk_color,
            "items": [calc_res.get("crisis_guide", "자립지원 전담기관 전문상담"), "서민금융통합지원센터 (☎1397)", "긴급생계비 지원선 연계"]
        }
    ]
