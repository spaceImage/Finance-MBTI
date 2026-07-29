"""
서민금융진흥원 대출상품 전체(318건 수준) 중, 청년 필터(keyword_filter.py)에
실제로 걸리는 상품만 뽑아서 보여주는 스크립트. 오탐/누락 검수(워크플로우 6단계)용.

사용법: backend 폴더에서 실행
    python scripts/list_youth_loan_products.py
"""
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from app.core.kinfa_client import fetch_raw_products, fetch_youth_filtered_loan_products

if __name__ == "__main__":
    all_products = fetch_raw_products()
    matched = fetch_youth_filtered_loan_products()

    print(f"\n전체 {len(all_products)}건 중 {len(matched)}건이 청년 필터에 걸렸습니다.\n")
    print("=" * 80)

    for m in matched:
        print(f"✅ {m.get('finprdnm')}")
        print(f"   대상: {m.get('trgt')} / 나이: {m.get('age')}")
        print(f"   걸린 이유: {m.get('_match_reason')}")
        print("-" * 80)

    if not matched:
        print("걸린 상품이 없습니다. .env 키 설정이나 필터 조건을 다시 확인해보세요.")