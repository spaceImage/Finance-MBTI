import { useState, useEffect, useCallback } from "react";
import {
  fetchQuestions,
  submitDiagnosis,
  QuestionItem,
  AnswerItem,
  SubmitDiagnosisResponse,
} from "../services/api";

export function useQuizSession() {
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [result, setResult] = useState<SubmitDiagnosisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchQuestions()
      .then((data) => {
        setQuestions(data);
        setAnswers(new Array(data.length).fill(-1));
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "질문을 불러오지 못했습니다. 백엔드 서버를 확인해 주세요.");
        setLoading(false);
      });
  }, []);

  const selectAnswer = useCallback(
    (choiceIndex: number) => {
      if (submitting) return;
      if (!questions[currentIndex]) return;

      const newAnswers = [...answers];
      newAnswers[currentIndex] = choiceIndex;
      setAnswers(newAnswers);

      if (currentIndex < questions.length - 1) {
        // Auto advance
        setTimeout(() => setCurrentIndex((i) => i + 1), 200);
      } else {
        // Last question – submit
        handleSubmit(newAnswers);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [currentIndex, questions, answers, submitting]
  );

  const handleSubmit = async (finalAnswers: number[]) => {
    setError(null);

    const hasInvalidAnswer = finalAnswers.some(
      (answer) => !Number.isInteger(answer) || answer < 0 || answer > 3,
    );
    if (hasInvalidAnswer) {
      setError("모든 질문에 답한 뒤 다시 시도해 주세요.");
      return;
    }

    setSubmitting(true);

    let uuid = sessionStorage.getItem("dotori_session_uuid");
    if (!uuid) {
      uuid = crypto.randomUUID();
      sessionStorage.setItem("dotori_session_uuid", uuid);
    }

    const payload: AnswerItem[] = questions.map((q, i) => ({
      question_id: q.id,
      choice_index: finalAnswers[i],
    }));

    try {
      const res = await submitDiagnosis(uuid, payload);
      sessionStorage.setItem("dotori-result", JSON.stringify(res));
      setResult(res);
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "결과를 계산하지 못했습니다. 잠시 후 다시 시도해 주세요.";
      setError(message);
      setSubmitting(false);
    }
  };

  const prevQuestion = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1);
    }
  }, [currentIndex]);

  const progress = questions.length
    ? Math.round(((currentIndex + 1) / questions.length) * 100)
    : 0;

  return {
    questions,
    currentIndex,
    currentQuestion: questions[currentIndex] ?? null,
    totalQuestions: questions.length,
    answers,
    result,
    loading,
    submitting,
    error,
    progress,
    selectAnswer,
    prevQuestion,
  };
}
