import { useEffect } from "react";
import { useQuizSession } from "../hooks/useQuizSession";

const ALPHA = ["A", "B", "C", "D", "E", "F"];

export default function SurveyPage({
  onReplace,
}: {
  onReplace: (path: string) => void;
}) {
  const {
    currentQuestion,
    currentIndex,
    totalQuestions,
    answers,
    result,
    loading,
    submitting,
    error,
    progress,
    selectAnswer,
    prevQuestion,
  } = useQuizSession();

  // Navigate to result when done
  useEffect(() => {
    if (result) {
      onReplace("/");
    }
  }, [result, onReplace]);

  if (loading) {
    return (
      <main className="mobile-screen">
        <header className="result-header">
          <a className="mini-brand" href="/start" aria-label="처음 화면으로 돌아가기">
            <span className="brand-acorn" aria-hidden="true" />
            <span>돌아가기</span>
          </a>
          <span className="header-brand-title">DOTORI DNA</span>
        </header>
        <div className="status-message">
          <span className="status-spinner">🌰</span>
          <p>질문을 불러오는 중이에요…</p>
        </div>
      </main>
    );
  }

  if (error && !submitting) {
    return (
      <main className="mobile-screen">
        <header className="result-header">
          <a className="mini-brand" href="/start" aria-label="처음 화면으로 돌아가기">
            <span className="brand-acorn" aria-hidden="true" />
            <span>돌아가기</span>
          </a>
          <span className="header-brand-title">DOTORI DNA</span>
        </header>
        <div className="status-message">
          <p>{error}</p>
          <button
            type="button"
            className="prev-btn"
            onClick={() => window.location.reload()}
          >
            다시 시도
          </button>
        </div>
      </main>
    );
  }

  if (submitting) {
    return (
      <main className="mobile-screen">
        <header className="result-header">
          <a className="mini-brand" href="/start" aria-label="처음 화면으로 돌아가기">
            <span className="brand-acorn" aria-hidden="true" />
            <span>돌아가기</span>
          </a>
          <span className="header-brand-title">DOTORI DNA</span>
        </header>
        <div className="status-message">
          <span className="status-spinner">🌰</span>
          <p>결과를 만드는 중이에요…</p>
        </div>
      </main>
    );
  }

  if (!currentQuestion) return null;

  const displayNum = String(currentIndex + 1).padStart(2, "0");
  const displayTotal = String(totalQuestions).padStart(2, "0");
  const isLast = currentIndex === totalQuestions - 1;

  const categoryIcons: Record<string, string> = {
    소비: "💰",
    저축: "🏦",
    투자: "📈",
    보험: "🛡️",
    부채: "📊",
    금융지식: "📚",
    위기대응: "⚡",
  };

  return (
    <main className="mobile-screen">
      {/* Header */}
      <header className="result-header">
        <a className="mini-brand" href="/start" aria-label="처음 화면으로 돌아가기">
          <span className="brand-acorn" aria-hidden="true" />
          <span>돌아가기</span>
        </a>
        <span className="header-brand-title">DOTORI DNA</span>
        <span className="result-step">
          QUESTION {displayNum} / {displayTotal}
        </span>
      </header>

      {/* Progress Bar */}
      <div className="progress-wrap">
        <div className="progress-bar-track">
          <div
            className="progress-bar-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="progress-percent">{progress}%</span>
      </div>

      {/* Question Card */}
      <div className="question-card">
        <span className="question-sticker">Q. {displayNum}</span>
        <span className="question-icon">
          {categoryIcons[currentQuestion.category] || "💡"}
        </span>
        <span className="question-category">
          {currentQuestion.category?.toUpperCase()}
        </span>
        <h1>{currentQuestion.question}</h1>
      </div>

      {/* Answer Options */}
      <div className="answer-list" aria-label="응답 선택지">
        {currentQuestion.options.map((opt, idx) => {
          const value = idx;
          const selected = answers[currentIndex] === value;
          return (
            <button
              key={idx}
              type="button"
              className={`answer-option ${selected ? "selected" : ""}`}
              onClick={() => selectAnswer(value)}
              disabled={submitting}
            >
              <span className="answer-index">{ALPHA[idx]}</span>
              <strong className="answer-text">{opt.text}</strong>
              <i className="answer-check">{selected ? "✓" : ""}</i>
            </button>
          );
        })}
      </div>

      {/* Footer */}
      <div className="survey-footer">
        <button
          type="button"
          className="prev-btn"
          disabled={currentIndex === 0}
          onClick={prevQuestion}
        >
          ← 이전 질문
        </button>
        <span className="auto-advance-note">
          {isLast
            ? "답을 고르면 바로 결과를 보여드려요."
            : "답을 고르면 다음 질문으로 바로 넘어가요."}
        </span>
      </div>
    </main>
  );
}
