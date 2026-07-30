import { useEffect, useState } from "react";
import { SubmitDiagnosisResponse } from "../services/api";

const TYPE_NAMES: Record<string, string> = {
  PEAS: "금고 속 튼튼 도토리",
  PEAI: "새싹을 꿈꾸는 탐구 도토리",
  PERS: "선배 둥지 따뜻 도토리",
  PERI: "가이드 탑승 모험 도토리",
  PVRS: "포근한 모자 도토리",
  PVRI: "꿈나무 열매 도토리",
  PVAS: "반짝이는 왕관 도토리",
  PVAI: "트랜디한 힙스터 도토리",
  FEAS: "굴러가는 실속 도토리",
  FEAI: "번개 탄 스피드 도토리",
  FERS: "둥글둥글 순한 도토리",
  FERI: "호기심 퐁퐁 도토리",
  FVRS: "솜이불 덮은 도토리",
  FVRI: "풍선 탄 낭만 도토리",
  FVAS: "달콤한 디저트 도토리",
  FVAI: "마이웨이 욜로 도토리",
};

const RISK_MAP: Record<
  string,
  { className: string; stage: string }
> = {
  GREEN: { className: "risk-green", stage: "안정 신호" },
  YELLOW: { className: "risk-yellow", stage: "주의 신호" },
  RED: { className: "risk-red", stage: "위험 신호" },
};

const DEFAULT_RESULT: SubmitDiagnosisResponse = {
  session_uuid: "",
  mbti_code: "PEAI",
  risk_color: "GREEN",
  combined_label: "계획적인 투자자",
  character_name: "새싹을 꿈꾸는 탐구 도토리",
  summary:
    "계획을 세워 차곡차곡 모으고, 더 큰 가능성은 꼼꼼히 탐색하는 타입이에요.",
  crisis_title: "안정적인 금융 생활",
  crisis_advice: "현재 금융 습관을 유지하면서 더 나은 기회를 탐색해 보세요.",
  crisis_guide: "정기적인 재무 점검으로 건강한 금융 생활을 이어가세요.",
  recommended_products: [],
};

export default function ResultPage() {
  const [data, setData] = useState<SubmitDiagnosisResponse>(DEFAULT_RESULT);
  const [nickname, setNickname] = useState("");

  useEffect(() => {
    // Load nickname
    const savedNickname = sessionStorage.getItem("dotori-nickname") || "";
    setNickname(savedNickname);

    // Load result
    const raw = sessionStorage.getItem("dotori-result");
    if (raw) {
      try {
        const parsed = JSON.parse(raw) as SubmitDiagnosisResponse;
        setData(parsed);
      } catch {
        sessionStorage.removeItem("dotori-result");
      }
    }
  }, []);

  const code = data.mbti_code || "PEAI";
  const typeName = TYPE_NAMES[code] || data.character_name || "탐구 도토리";
  const typeNameWithoutSuffix = typeName.replace(/\s*도토리$/, "");
  const hasDotoriSuffix = typeNameWithoutSuffix !== typeName;
  const risk = RISK_MAP[data.risk_color] || RISK_MAP.GREEN;

  return (
    <main className="result-screen">
      {/* Header */}
      <header className="result-header">
        <a className="mini-brand" href="/start" aria-label="도토리 금융 DNA">
          <span className="brand-acorn" aria-hidden="true" />
          DOTORI DNA
        </a>
        <span className="result-step">RESULT 01</span>
      </header>

      {/* Hero Card */}
      <section className="hero-card">
        <div className="hero-cloud-a" aria-hidden="true" />
        <div className="hero-cloud-b" aria-hidden="true" />
        <div className="hero-type-badge">
          <span className="hero-type-code">{code}</span>
          <span className="hero-type-label">{data.combined_label}</span>
        </div>
        <div className="hero-title-area">
          {nickname && (
            <span className="hero-nickname-sticker">{nickname}님의 결과</span>
          )}
          <h1 className="hero-type-name">
            <span>{typeNameWithoutSuffix}</span>
            {hasDotoriSuffix && (
              <span className="hero-type-suffix">도토리</span>
            )}
          </h1>
        </div>
        <img
          key={code}
          className="result-character"
          data-character-code={code}
          src={`/acorns/${code}.png`}
          alt={typeName}
          onAnimationStart={() => {
            console.info(
              `[DOTORI_RESULT_ANIMATION] code=${code} cycle=1 phase=start`,
            );
          }}
          onAnimationIteration={() => {
            console.info(
              `[DOTORI_RESULT_ANIMATION] code=${code} cycle=2 phase=start`,
            );
          }}
          onAnimationEnd={() => {
            console.info(
              `[DOTORI_RESULT_ANIMATION] code=${code} cycles=2 phase=complete elapsed_ms=10000`,
            );
          }}
        />
      </section>

      {/* DNA Report */}
      <section className="summary-card">
        <span className="dna-report-label">DNA REPORT</span>

        <div className="keyword-chips">
          <span className="keyword-chip">#자립적립</span>
          <span className="keyword-chip">#성장투자</span>
          <span className="keyword-chip">#목표저축</span>
        </div>

        <div className="rec-grid" aria-label="맞춤 금융 추천">
          <div className="rec-item">
            <div className="rec-panel">
              <p className="rec-desc">
                <strong>청년 자산형성 지원</strong>
                자립준비청년이 활용할 수 있는 정부지원금과 자산형성 제도를 확인해 보세요.
              </p>
            </div>
          </div>
          <div className="rec-item">
            <div className="rec-panel">
              <p className="rec-desc">
                <strong>청년 우대 금융상품</strong>
                우대금리 적금과 수수료 혜택 등 은행권의 청년 맞춤 상품을 비교해 보세요.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Risk Signal Card */}
      <section className={`risk-card ${risk.className}`}>
        <div className="risk-topline">
          <span className="risk-signal-label">RISK SIGNAL</span>
          <p className="risk-stage">
            <img
              className="risk-illustration"
              src="/illustrations/traffic-light.png"
              alt="안정, 주의, 위험을 나타내는 신호등"
            />
            {risk.stage}
          </p>
        </div>
        <p className="risk-concern">
          {data.crisis_title || "현재 금융 상태를 점검해 보세요."}
        </p>
        <p className="risk-action">
          {data.crisis_advice || ""}
          {data.crisis_guide ? ` ${data.crisis_guide}` : ""}
        </p>
      </section>

      {/* Save Button */}
      <button
        type="button"
        className="save-button"
        onClick={() => {
          alert("결과가 저장되었습니다!");
        }}
      >
        결과 저장하기
      </button>
    </main>
  );
}
