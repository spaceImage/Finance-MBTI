from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.session import Base

class DiagnosisSession(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DiagnosisResponse(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_uuid = Column(String(36), index=True)
    question_id = Column(Integer, nullable=False)
    choice_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class DiagnosisResult(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_uuid = Column(String(36), index=True)
    mbti_code = Column(String(10), nullable=False)
    risk_color = Column(String(10), nullable=False)
    combined_label = Column(String(100), nullable=False)
    scores_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

