const API_BASE_URL = 'http://localhost:8001/api/diagnosis';

export interface AnswerItem {
  question_id: number;
  choice_index: number;
}

export interface QuestionOption {
  text: string;
}

export interface QuestionItem {
  id: number;
  type: string;
  category: string;
  question: string;
  options: QuestionOption[];
}

export interface ProductRecommendation {
  id: number;
  name: string;
  category: string;
  description: string;
  risk_level: string;
  tag: string;
  items?: string[];
}

export interface SubmitDiagnosisResponse {
  session_uuid: string;
  mbti_code: string;
  crisis_score?: number;
  risk_color: string;
  crisis_status?: string;
  combined_label: string;
  character_name: string;
  feature?: string;
  summary?: string;
  mascot?: string;
  financial_product?: string;
  government_policy?: string;
  crisis_title?: string;
  crisis_advice?: string;
  crisis_guide?: string;
  recommended_products: ProductRecommendation[];
}

export async function fetchQuestions(): Promise<QuestionItem[]> {
  const res = await fetch(`${API_BASE_URL}/questions`);
  if (!res.ok) {
    throw new Error('문항 데이터를 불러오는 데 실패했습니다.');
  }
  return res.json();
}

export async function submitDiagnosis(sessionUuid: string, answers: AnswerItem[]): Promise<SubmitDiagnosisResponse> {
  const res = await fetch(`${API_BASE_URL}/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_uuid: sessionUuid,
      answers,
    }),
  });

  if (!res.ok) {
    throw new Error('진단 제출에 실패했습니다.');
  }

  return res.json();
}
