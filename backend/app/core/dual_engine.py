import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS_PATH = os.path.join(BASE_DIR, "data", "questions.json")
TYPES_PATH = os.path.join(BASE_DIR, "data", "types.json")

def load_data():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open(TYPES_PATH, "r", encoding="utf-8") as f:
        types_info = json.load(f)
    return questions, types_info

QUESTIONS, TYPES_INFO = load_data()

def calculate_diagnosis(answers: list[dict]):
    """
    answers: [{"question_id": 1, "choice_index": 0}, ...]
    """
    q_map = {q["id"]: q for q in QUESTIONS}
    
    mbti_codes = {
        1: "P", # Default
        2: "E",
        3: "A",
        4: "S"
    }
    
    crisis_score = 0
    
    for ans in answers:
        q_id = ans.get("question_id")
        choice_idx = ans.get("choice_index", 0)
        
        if q_id in q_map:
            q_item = q_map[q_id]
            options = q_item["options"]
            if 0 <= choice_idx < len(options):
                opt = options[choice_idx]
                if q_item["type"] == "mbti":
                    mbti_codes[q_id] = opt.get("code", "P")
                elif q_item["type"] == "crisis":
                    crisis_score += opt.get("score", 0)

    # 1. 4-letter MBTI Code
    p1 = mbti_codes.get(1, "P")
    p2 = mbti_codes.get(2, "E")
    p3 = mbti_codes.get(3, "A")
    p4 = mbti_codes.get(4, "S")
    mbti_code = f"{p1}{p2}{p3}{p4}"
    
    # 2. Crisis Score & Risk Level
    if crisis_score <= 1:
        crisis_level_key = "GREEN"
    elif crisis_score <= 4:
        crisis_level_key = "YELLOW"
    else:
        crisis_level_key = "RED"
        
    crisis_info = TYPES_INFO["crisis_levels"][crisis_level_key]
    risk_color = crisis_info["color"]
    crisis_status = crisis_info["status"]
    
    # 3. MBTI Type Info Lookup
    mbti_data = TYPES_INFO["mbti_types"].get(mbti_code, TYPES_INFO["mbti_types"]["PEAS"])
    
    character_name = mbti_data["title"]
    combined_label = f"{mbti_code}-{risk_color} {character_name}"
    
    return {
        "mbti_code": mbti_code,
        "crisis_score": crisis_score,
        "risk_color": risk_color,
        "crisis_status": crisis_status,
        "combined_label": combined_label,
        "character_name": character_name,
        "feature": mbti_data["feature"],
        "mascot": mbti_data["mascot"],
        "financial_product": mbti_data["financial_product"],
        "government_policy": mbti_data["policy"],
        "crisis_title": crisis_info["title"],
        "crisis_advice": crisis_info["advice"],
        "crisis_guide": crisis_info["guide"]
    }
