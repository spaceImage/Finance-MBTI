"""
온통청년 정책 중 mclsfNm(중분류)이 "취약계층 및 금융지원"으로 분류된 것만 뽑아서 보여주는 스크립트.

사용법: backend 폴더에서 실행
    python scripts/list_youth_finance_policies.py
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from app.core.youthcenter_client import fetch_raw_policies, fetch_finance_youth_policies

if __name__ == "__main__":
    all_policies = fetch_raw_policies()
    matched = fetch_finance_youth_policies()

    print(f"\n대분류 '금융･복지･문화'로 받아온 {len(all_policies)}건 중 "
          f"{len(matched)}건이 '취약계층 및 금융지원' 중분류에 해당합니다.\n")
    print("=" * 80)

    for m in matched:
        print(f"✅ {m.get('plcyNm')}")
        print(f"   설명: {m.get('plcyExplnCn')}")
        print(f"   나이: {m.get('sprtTrgtMinAge')}세 ~ {m.get('sprtTrgtMaxAge')}세")
        print("-" * 80)

    if not matched:
        print("걸린 정책이 없습니다. .env 키 설정이나 lclsfNm 값을 다시 확인해보세요.")