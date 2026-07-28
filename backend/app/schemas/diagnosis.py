from pydantic import BaseModel, Field
from typing import List, Optional

class AnswerItem(BaseModel):
    question_id: int
    choice_index: int

class SubmitDiagnosisRequest(BaseModel):
    session_uuid: str = Field(..., description="Unique client session ID")
    answers: List[AnswerItem]

class ProductRecommendation(BaseModel):
    id: int
    name: str
    category: str
    description: str
    risk_level: str
    tag: str
    items: Optional[List[str]] = Field(default_factory=list)

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
