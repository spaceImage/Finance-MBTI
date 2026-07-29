"""
온통청년 API의 실제 응답 필드를 눈으로 확인하기 위한 스크립트.

사용법:
  1. backend/.env 파일에 YOUTHCENTER_API_KEY를 채워넣는다.
  2. backend 폴더에서 실행: python scripts/inspect_youthcenter_response.py
  3. 정책명/정책설명이 어떤 키로 오는지 확인한다.
  4. app/core/youthcenter_client.py 맨 아래 YOUTHCENTER_NAME_FIELD,
     YOUTHCENTER_DESC_FIELD를 실제 키 이름으로 교체한다.
"""
import sys
import os
import json
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 이 스크립트는 app.main을 거치지 않고 단독 실행되기 때문에,
# main.py에서 하던 logging.basicConfig()가 적용되지 않아 [YOUTHCENTER] INFO 로그가
# 화면에 안 보이는 문제가 있었다. 여기서 직접 설정해준다.
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from app.core.youthcenter_client import fetch_raw_policies

if __name__ == "__main__":
    policies = fetch_raw_policies()

    if not policies:
        print("결과가 비어있습니다. 다음을 확인하세요:")
        print("  1) .env에 YOUTHCENTER_API_KEY가 채워져 있는지")
        print("  2) 온통청년 마이페이지에서 이 API 인증키가 '승인' 상태인지")
        print("  3) 콘솔에 [YOUTHCENTER] 로 시작하는 에러 로그가 있는지")
        sys.exit(0)

    print(f"총 {len(policies)}건 수신. 첫 번째 항목의 필드 목록:\n")
    first = policies[0]
    for key, value in first.items():
        print(f"  {key}: {value}")

    print("\n--- 첫 번째 항목 전체 (raw) ---")
    print(json.dumps(first, ensure_ascii=False, indent=2))
