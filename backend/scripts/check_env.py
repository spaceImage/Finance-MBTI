"""
.env 파일이 제대로 읽히고 있는지 확인하는 스크립트.
터미널에서 따옴표 꼬이는 문제 없이, backend 폴더에서 이렇게 실행하면 됩니다:
 
    python scripts/check_env.py
"""
import sys
import os
 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 
from app.config import settings
 
print("=== .env 로딩 상태 확인 ===")
print(f"FINLIFE_API_KEY    : {'설정됨 (' + str(len(settings.FINLIFE_API_KEY)) + '자)' if settings.FINLIFE_API_KEY else '❌ 비어있음'}")
print(f"KINFA_API_KEY       : {'설정됨 (' + str(len(settings.KINFA_API_KEY)) + '자)' if settings.KINFA_API_KEY else '❌ 비어있음'}")
print(f"YOUTHCENTER_API_KEY : {'설정됨 (' + str(len(settings.YOUTHCENTER_API_KEY)) + '자)' if settings.YOUTHCENTER_API_KEY else '❌ 비어있음'}")
 