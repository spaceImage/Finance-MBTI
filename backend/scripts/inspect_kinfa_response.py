"""
서민금융진흥원(공공데이터포털) API의 실제 응답을 눈으로 확인하기 위한 스크립트.

사용법:
  1. backend/.env 파일에 KINFA_API_KEY(디코딩 키)를 채워넣는다.
  2. backend 폴더에서 실행: python scripts/inspect_kinfa_response.py
  3. 출력된 JSON에서 "상품명이 어떤 키에 들어있는지", "지원대상/가입대상이 어떤 키에
     들어있는지" 확인한다.
  4. app/core/kinfa_client.py 맨 아래 KINFA_NAME_FIELD, KINFA_ELIGIBILITY_FIELD를
     확인한 실제 키 이름으로 바꾼다.

이 스크립트만 실행하면 되고, 서버(main.py)를 켤 필요는 없다.
"""
import sys
import os
import json
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from app.core.kinfa_client import fetch_raw_products

if __name__ == "__main__":
    items = fetch_raw_products()

    if not items:
        print("결과가 비어있습니다. 다음을 확인하세요:")
        print("  1) .env에 KINFA_API_KEY가 채워져 있는지 (디코딩 키인지)")
        print("  2) 공공데이터포털에서 이 API 활용신청이 '승인' 상태인지")
        print("  3) 콘솔에 [KINFA] 로 시작하는 에러 로그가 있는지")
        sys.exit(0)

    print(f"총 {len(items)}건 수신. 첫 번째 항목의 필드 목록:\n")
    first = items[0]
    for key, value in first.items():
        print(f"  {key}: {value}")

    print("\n--- 첫 번째 항목 전체 (raw) ---")
    print(json.dumps(first, ensure_ascii=False, indent=2))