import React from 'react';
import { ProgressBar } from '../components/quiz/ProgressBar';
import { QuizCard } from '../components/quiz/QuizCard';
import { QuestionItem } from '../services/api';

interface QuizPageProps {
  currentQuestion: QuestionItem;
  currentIndex: number;
  totalQuestions: number;
  selectedChoiceIndex?: number;
  onSelectAnswer: (idx: number) => void;
  onPrev: () => void;
}

export const QuizPage: React.FC<QuizPageProps> = ({
  currentQuestion,
  currentIndex,
  totalQuestions,
  selectedChoiceIndex,
  onSelectAnswer,
  onPrev,
}) => {
  return (
    <div className="page-container">
      <div className="header-logo">
        <span className="logo-icon">🌰</span>
        <span className="logo-text">DOTORI</span>
        <span className="logo-sub">금융 MBTI & 위험도 진단</span>
      </div>

      <ProgressBar current={currentIndex + 1} total={totalQuestions} />

      {currentQuestion && (
        <QuizCard
          question={currentQuestion}
          selectedChoiceIndex={selectedChoiceIndex}
          onSelect={onSelectAnswer}
          onPrev={onPrev}
          canPrev={currentIndex > 0}
        />
      )}
    </div>
  );
};
