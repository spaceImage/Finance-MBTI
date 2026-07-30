from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional

# 필수 문항 ID (Q1~Q4 성향 진단 + Q5~Q7 위기감지)
REQUIRED_QUESTION_IDS = {1, 2, 3, 4, 5, 6, 7}

class AnswerItem(BaseModel):
    question_id: int
    choice_index: int

    @field_validator("choice_index")
    @classmethod
    def choice_index_must_be_in_range(cls, v: int) -> int:
        if v < 0 or v > 3:
            raise ValueError("choice_index는 0~3 사이의 값이어야 합니다.")
        return v

class SubmitDiagnosisRequest(BaseModel):
    session_uuid: str = Field(..., description="Unique client session ID")
    answers: List[AnswerItem]

    @model_validator(mode="after")
    def validate_answers_complete(self) -> "SubmitDiagnosisRequest":
        answered_ids = [a.question_id for a in self.answers]
        answered_id_set = set(answered_ids)

        missing = REQUIRED_QUESTION_IDS - answered_id_set
        if missing:
            raise ValueError(f"응답하지 않은 문항이 있습니다: {sorted(missing)}")

        invalid = answered_id_set - REQUIRED_QUESTION_IDS
        if invalid:
            raise ValueError(f"존재하지 않는 문항 ID입니다: {sorted(invalid)}")

        if len(answered_ids) != len(REQUIRED_QUESTION_IDS):
            raise ValueError("문항당 하나의 응답만 제출해야 합니다 (중복 응답 감지).")

        return self

class ProductRecommendation(BaseModel):
    id: int
    name: str
    category: str
    description: str
    risk_level: str
    tag: str
    items: Optional[List[str]] = Field(default_factory=list)
    is_live: bool = False
    url: Optional[str] = None

class SubmitDiagnosisResponse(BaseModel):
    session_uuid: str
    mbti_code: str
    crisis_score: int
    risk_color: str
    crisis_status: str
    combined_label: str
    character_name: str
    feature: str
    summary: str
    mascot: str
    financial_product: str
    government_policy: str
    crisis_title: str
    crisis_advice: str
    crisis_guide: str
    recommended_products: List[ProductRecommendation]

class QuestionOption(BaseModel):
    text: str

class QuestionItem(BaseModel):
    id: int
    type: str
    category: str
    question: str
    options: List[QuestionOption]
