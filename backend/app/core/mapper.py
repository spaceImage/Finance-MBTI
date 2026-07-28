def get_recommendations(mbti_code: str, calc_res: dict) -> list[dict]:
    """
    Returns actual financial product and government policy recommendation cards matching youth MBTI type.
    """
    financial_prod = calc_res.get("financial_product", "")
    policy = calc_res.get("government_policy", "")
    risk_color = calc_res.get("risk_color", "🟢")
    
    return [
        {
            "id": 1,
            "category": "실제 금융상품",
            "name": financial_prod.split(" — ")[0] if " — " in financial_prod else financial_prod,
            "description": financial_prod.split(" — ")[1] if " — " in financial_prod else "맞춤형 우대 금리 및 안전 자산 운용",
            "tag": "맞춤 금융",
            "risk_level": risk_color,
            "items": ["우대 금리 / 수시입출금 혜택", "자동이체 연동 저축 서비스", "안전 자산 관리"]
        },
        {
            "id": 2,
            "category": "정부 청년정책",
            "name": policy.split(" — ")[0] if " — " in policy else policy,
            "description": policy.split(" — ")[1] if " — " in policy else "자립준비청년 전용 매칭 지원 및 자산형성",
            "tag": "정부 지원",
            "risk_level": "🟢 지원혜택",
            "items": ["정부 매칭 지원금 제공", "자립수당 연계 혜택", "청년 맞춤 가입조건"]
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
