import json
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import DiagnosisSession, DiagnosisResponse, DiagnosisResult
from app.schemas.diagnosis import SubmitDiagnosisRequest, SubmitDiagnosisResponse, QuestionItem
from app.core.dual_engine import calculate_diagnosis, QUESTIONS
from app.core.mapper import get_recommendations
from app.core.finlife_client import fetch_youth_filtered_products
from app.core.youthcenter_client import fetch_finance_youth_policies

logger = logging.getLogger("dotori")
router = APIRouter(prefix="/api/diagnosis", tags=["diagnosis"])

@router.get("/questions", response_model=list[QuestionItem])
def get_questions():
    """Returns list of 4 MBTI questions + 3 Crisis diagnostic questions"""
    formatted = []
    for q in QUESTIONS:
        formatted.append({
            "id": q["id"],
            "type": q["type"],
            "category": q["category"],
            "question": q["question"],
            "options": [{"text": opt["text"]} for opt in q["options"]]
        })
    return formatted

@router.get("/youth-products")
def get_youth_products():
    """
    금감원 금융상품통합비교공시 API에서 은행권+저축은행권 예·적금 전체를 받아
    청년 키워드 필터를 적용한 결과를 반환한다.
    (API 키 미설정 시 빈 리스트 반환 — 에러 아님)
    """
    return fetch_youth_filtered_products()


@router.get("/youth-policies")
def get_youth_policies():
    """
    온통청년 API에서 '청년 금융' 키워드로 좁힌 정책 목록을 반환한다.
    (API 키 미설정 시 빈 리스트 반환 — 에러 아님)
    """
    return {"policies": fetch_finance_youth_policies()}


@router.post("/submit", response_model=SubmitDiagnosisResponse)
def submit_diagnosis(payload: SubmitDiagnosisRequest, db: Session = Depends(get_db)):
    """
    Synchronous diagnosis calculation for Youth MBTI & Crisis Score.
    """
    answers_dicts = [a.model_dump() for a in payload.answers]
    
    # 1. Calculation
    calc_res = calculate_diagnosis(answers_dicts)
    mbti_code = calc_res["mbti_code"]
    risk_color = calc_res["risk_color"]
    combined_label = calc_res["combined_label"]
    
    # 2. Recommendations
    recommendations = get_recommendations(mbti_code, calc_res)
    
    # 3. Synchronous DB Storage with Fallback (중복 제출 방지: 기존 데이터 삭제 후 재저장)
    try:
        session_obj = db.query(DiagnosisSession).filter(DiagnosisSession.id == payload.session_uuid).first()
        if not session_obj:
            session_obj = DiagnosisSession(id=payload.session_uuid)
            db.add(session_obj)
        else:
            # 기존 응답/결과 삭제 (재진단 시 중복 방지)
            db.query(DiagnosisResponse).filter(DiagnosisResponse.session_uuid == payload.session_uuid).delete()
            db.query(DiagnosisResult).filter(DiagnosisResult.session_uuid == payload.session_uuid).delete()
        
        for ans in payload.answers:
            db_resp = DiagnosisResponse(
                session_uuid=payload.session_uuid,
                question_id=ans.question_id,
                choice_index=ans.choice_index
            )
            db.add(db_resp)
            
        db_res = DiagnosisResult(
            session_uuid=payload.session_uuid,
            mbti_code=mbti_code,
            risk_color=risk_color,
            combined_label=combined_label,
            scores_json=json.dumps({
                "mbti_code": mbti_code,
                "crisis_score": calc_res["crisis_score"],
                "risk_color": risk_color
            })
        )
        db.add(db_res)
        db.commit()
    except Exception as e:
        logger.error(f"[DB Error] SQLite write failed for session {payload.session_uuid}: {e}", exc_info=True)
        db.rollback()
        
    return SubmitDiagnosisResponse(
        session_uuid=payload.session_uuid,
        mbti_code=mbti_code,
        crisis_score=calc_res["crisis_score"],
        risk_color=risk_color,
        crisis_status=calc_res["crisis_status"],
        combined_label=combined_label,
        character_name=calc_res["character_name"],
        feature=calc_res["feature"],
        summary=f"{calc_res['character_name']} — {calc_res['crisis_status']} 등급",
        mascot=calc_res["mascot"],
        financial_product=calc_res["financial_product"],
        government_policy=calc_res["government_policy"],
        crisis_title=calc_res["crisis_title"],
        crisis_advice=calc_res["crisis_advice"],
        crisis_guide=calc_res["crisis_guide"],
        recommended_products=recommendations
    )
