import React from 'react';
import { useQuizSession } from './hooks/useQuizSession';
import { QuizPage } from './pages/QuizPage';
import { ResultPage } from './pages/ResultPage';
import './App.css';

export function App() {
  const {
    currentQuestion,
    currentIndex,
    totalQuestions,
    answers,
    result,
    loading,
    submitting,
    error,
    selectAnswer,
    prevQuestion,
    restartQuiz,
  } = useQuizSession();

  if (loading) {
    return (
      <div className="center-screen">
        <div className="spinner">🌰</div>
        <p className="loading-text">DOTORI 진단 데이터를 불러오는 중입니다...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="center-screen">
        <div className="error-box">
          <p className="error-title">⚠️ 통신 오류 발생</p>
          <p>{error}</p>
          <button className="restart-btn" onClick={() => window.location.reload()}>
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  if (submitting) {
    return (
      <div className="center-screen">
        <div className="spinner pulse">🌰</div>
        <h2 className="loading-title">금융 MBTI & 위험도 분석 중...</h2>
        <p className="loading-desc">16가지 유형과 3대 맞춤형 상품군을 이중 엔진으로 계산하고 있습니다.</p>
      </div>
    );
  }

  if (result) {
    return <ResultPage result={result} onRestart={restartQuiz} />;
  }

  const currentAnswerObj = answers.find((a) => a.question_id === currentQuestion?.id);

  return (
    <QuizPage
      currentQuestion={currentQuestion}
      currentIndex={currentIndex}
      totalQuestions={totalQuestions}
      selectedChoiceIndex={currentAnswerObj?.choice_index}
      onSelectAnswer={selectAnswer}
      onPrev={prevQuestion}
    />
  );
}

export default App;
