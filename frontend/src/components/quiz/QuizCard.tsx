import React from 'react';
import { QuestionItem } from '../../services/api';

interface QuizCardProps {
  question: QuestionItem;
  selectedChoiceIndex?: number;
  onSelect: (choiceIndex: number) => void;
  onPrev?: () => void;
  canPrev: boolean;
}

export const QuizCard: React.FC<QuizCardProps> = ({
  question,
  selectedChoiceIndex,
  onSelect,
  onPrev,
  canPrev
}) => {
  return (
    <div className="quiz-card">
      <div className="quiz-card-category font-mono">
        <span>Q{question.id}.</span> {question.category}
      </div>

      <h2 className="quiz-card-title">
        {question.question}
      </h2>

      <div className="options-grid">
        {question.options.map((opt, idx) => {
          const isSelected = selectedChoiceIndex === idx;
          return (
            <button
              key={idx}
              className={`option-btn ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelect(idx)}
            >
              <div className="option-indicator">{String.fromCharCode(65 + idx)}</div>
              <div className="option-text">{opt.text}</div>
            </button>
          );
        })}
      </div>

      {canPrev && onPrev && (
        <div className="quiz-card-footer">
          <button className="prev-btn" onClick={onPrev}>
            ← 이전 문항으로
          </button>
        </div>
      )}
    </div>
  );
};
