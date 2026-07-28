import { useState, useEffect } from 'react';
import { fetchQuestions, submitDiagnosis, QuestionItem, AnswerItem, SubmitDiagnosisResponse } from '../services/api';

export function useQuizSession() {
  const [sessionUuid, setSessionUuid] = useState<string>('');
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [answers, setAnswers] = useState<AnswerItem[]>([]);
  const [result, setResult] = useState<SubmitDiagnosisResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Generate UUID or load from sessionStorage
    let uuid = sessionStorage.getItem('dotori_session_uuid');
    if (!uuid) {
      uuid = crypto.randomUUID();
      sessionStorage.setItem('dotori_session_uuid', uuid);
    }
    setSessionUuid(uuid);

    // Fetch Q1~Q7 questions
    fetchQuestions()
      .then((data) => {
        setQuestions(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || '데이터를 불러오지 못했습니다.');
        setLoading(false);
      });
  }, []);

  const selectAnswer = (choiceIndex: number) => {
    if (!questions[currentIndex]) return;

    const qId = questions[currentIndex].id;
    const newAnswers = [...answers.filter((a) => a.question_id !== qId), { question_id: qId, choice_index: choiceIndex }];
    setAnswers(newAnswers);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Last question reached, submit automatically!
      handleSubmit(newAnswers);
    }
  };

  const prevQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = async (finalAnswers: AnswerItem[]) => {
    setSubmitting(true);
    setError(null);
    try {
      const res = await submitDiagnosis(sessionUuid, finalAnswers);
      setResult(res);
    } catch (err: any) {
      setError(err.message || '진단 제출 중 오류가 발생했습니다.');
    } finally {
      setSubmitting(false);
    }
  };

  const restartQuiz = () => {
    setCurrentIndex(0);
    setAnswers([]);
    setResult(null);
  };

  return {
    sessionUuid,
    questions,
    currentIndex,
    currentQuestion: questions[currentIndex],
    totalQuestions: questions.length,
    answers,
    result,
    loading,
    submitting,
    error,
    selectAnswer,
    prevQuestion,
    restartQuiz,
  };
}
