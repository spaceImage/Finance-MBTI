import React from 'react';
import { ResultBanner } from '../components/result/ResultBanner';
import { ProductCard } from '../components/result/ProductCard';
import { SubmitDiagnosisResponse } from '../services/api';

interface ResultPageProps {
  result: SubmitDiagnosisResponse;
  onRestart: () => void;
}

export const ResultPage: React.FC<ResultPageProps> = ({ result, onRestart }) => {
  return (
    <div className="page-container result-page-container">
      <div className="header-logo">
        <span className="logo-icon">🌰</span>
        <span className="logo-text">DOTORI</span>
        <span className="logo-sub">진단 리포트</span>
      </div>

      <ResultBanner result={result} />

      <ProductCard products={result.recommended_products} />

      <div className="action-row">
        <button className="restart-btn" onClick={onRestart}>
          🔄 다시 진단하기
        </button>
      </div>
    </div>
  );
};
