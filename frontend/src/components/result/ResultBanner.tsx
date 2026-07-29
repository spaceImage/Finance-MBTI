import React from 'react';
import { SubmitDiagnosisResponse } from '../../services/api';

interface ResultBannerProps {
  result: SubmitDiagnosisResponse;
  nickname?: string;
}

export const ResultBanner: React.FC<ResultBannerProps> = ({ result, nickname }) => {
  const summaryText = result.feature || result.summary || '금융 진단 결과입니다.';

  return (
    <div className="result-banner">
      <div className="result-badge-group">
        <span className="mbti-chip">{result.mbti_code}</span>
        <span className="risk-chip">{result.risk_color} {result.crisis_status || '성향'}</span>
      </div>

      <div className="mascot-avatar">
        <span className="mascot-icon">🌰</span>
      </div>

      {nickname && <p className="nickname-tag">{nickname}님의 금융 MBTI는</p>}

      <h1 className="character-name">
        {result.character_name}
      </h1>

      <p className="combined-label">
        {result.combined_label}
      </p>

      <div className="summary-box">
        <p>{summaryText}</p>
      </div>

      {result.crisis_title && (
        <div className="crisis-box">
          <h4 className="crisis-title">{result.crisis_title}</h4>
          {result.crisis_advice && <p className="crisis-advice">{result.crisis_advice}</p>}
          {result.crisis_guide && <p className="crisis-guide">💡 {result.crisis_guide}</p>}
        </div>
      )}
    </div>
  );
};
