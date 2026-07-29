import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "DOTORI PoC Diagnosis API"
    PORT: int = int(os.getenv("PORT", 8001))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dotori.db")
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    # 금융감독원 "금융상품한눈에" 오픈API 인증키
    # finlife.fss.or.kr에서 발급. 없으면 실시간 금리 연동은 자동으로 건너뛰고
    # 기존 정적 데이터(types.json)만 사용합니다.
    FINLIFE_API_KEY: str = os.getenv("FINLIFE_API_KEY", "")

    # 공공데이터포털(data.go.kr) 인증키 — "디코딩" 키를 넣을 것 (인코딩 키 아님)
    # 서민금융진흥원 관련 API에 사용
    KINFA_API_KEY: str = os.getenv("KINFA_API_KEY", "")

    # 온통청년(한국고용정보원) 청년정책 오픈API 인증키
    # 발급: youthcenter.go.kr 마이페이지 > OPEN API (담당자 심사 후 승인)
    YOUTHCENTER_API_KEY: str = os.getenv("YOUTHCENTER_API_KEY", "")

settings = Settings()
