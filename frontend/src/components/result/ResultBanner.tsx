import React from 'react';
import { SubmitDiagnosisResponse } from '../../services/api';

interface ResultBannerProps {
  result: SubmitDiagnosisResponse;
  nickname?: string;
}

const MASCOT_IMAGE_MAP: Record<string, string> = {
  PEAS: '/images/PEAS [철벽의 예산왕] 금고 속 튼튼 도토리.png',
  PEAI: '/images/PEAI [계획적인 투자자] 새싹을 꿈꾸는 탐구 도토리.png',
  PERS: '/images/PERS [안내받는 돌다리] 선배 둥지 따뜻 도토리.png',
  PERI: '/images/PERI [조력기반 성장의 힘] 가이드 탑승 모험 도토리.png',
  PVAS: '/images/PVAS [목적 명확한 밸런스] 반짝이는 왕관 도토리.png',
  PVAI: '/images/PVAI_트랜디한힙스터 도토리.png',
  PVRS: '/images/PVRS [안전지대 지킴이] 포근한 모자 도토리.png',
  PVRI: '/images/PVRI [조력기반 미래투자] 꿈나무 열매 도토리.png',
  FEAS: '/images/FEAS [알뜰한 분위기파] 굴러가는 실속 도토리.png',
  FEAI: '/images/FEAI [실속주의 즉흥러] 번개 탄 스피드 도토리.png',
  FERS: '/images/FERS [무난한 실속 수호자] 둥글둥글 순한 도토리.png',
  FERI: '/images/FERI [편안한 도전자] 호기심 퐁퐁 도토리.png',
  FVAS: '/images/FVAS [감성 가치 소비가] 달콤한 디저트 도토리.png',
  FVAI: '/images/FVAI [자유로운 투자가] 마이웨이 욜로 도토리.png',
  FVRS: '/images/FVRS [마음 든든 수호형] 솜이불 덮은 도토리.png',
  FVRI: '/images/FVRI [여유로운 감성파] 풍선 탄 낭만 도토리.png',
};

export const ResultBanner: React.FC<ResultBannerProps> = ({ result, nickname }) => {
  const summaryText = result.feature || result.summary || '금융 진단 결과입니다.';
  const imageSrc = MASCOT_IMAGE_MAP[result.mbti_code] || `/images/${result.mbti_code}.png`;

  return (
    <div className="result-banner">
      <div className="result-badge-group">
        <span className="mbti-chip">{result.mbti_code}</span>
        <span className="risk-chip">{result.risk_color} {result.crisis_status || '성향'}</span>
      </div>

      <div className="mascot-avatar">
        <img
          src={imageSrc}
          alt={result.character_name}
          className="mascot-img"
          onError={(e) => {
            // 이미지 파일이 없는 경우 🌰 이모지로 자동 대체
            const target = e.currentTarget;
            target.style.display = 'none';
            if (target.parentElement) {
              target.parentElement.innerHTML = '<span class="mascot-icon">🌰</span>';
            }
          }}
        />
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
