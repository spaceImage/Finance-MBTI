import os

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

settings = Settings()
