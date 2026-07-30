import { useEffect, useRef, useState } from "react";

type AnimationPhase = "idle" | "centering" | "inspecting" | "zooming";

const CENTER_DURATION = 840;
const INSPECT_DURATION = 1080;
const ZOOM_DURATION = 880;

export default function StartPage({
  onNavigate,
}: {
  onNavigate: (path: string) => void;
}) {
  const [nickname, setNickname] = useState("");
  const [animationPhase, setAnimationPhase] =
    useState<AnimationPhase>("idle");
  const timerIds = useRef<number[]>([]);
  const animationStartedAt = useRef(0);
  const motionAudioRef = useRef<HTMLAudioElement>(null);
  const canStart = nickname.trim().length > 0 && animationPhase === "idle";

  useEffect(() => {
    return () => {
      timerIds.current.forEach(window.clearTimeout);
      motionAudioRef.current?.pause();
    };
  }, []);

  const logAnimationPhase = (phase: string) => {
    const elapsed = Math.round(performance.now() - animationStartedAt.current);
    console.info(
      `[DOTORI_START_ANIMATION] phase=${phase} elapsed_ms=${elapsed}`,
    );
  };

  const handleStart = () => {
    if (!canStart) return;
    sessionStorage.setItem("dotori-nickname", nickname.trim());
    animationStartedAt.current = performance.now();

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      logAnimationPhase("reduced-motion-skip");
      onNavigate("/survey");
      return;
    }

    if (motionAudioRef.current) {
      motionAudioRef.current.currentTime = 0;
      void motionAudioRef.current.play().catch(() => {
        console.info("[DOTORI_START_AUDIO] playback=blocked");
      });
    }

    setAnimationPhase("centering");
    logAnimationPhase("centering");

    timerIds.current.push(
      window.setTimeout(() => {
        setAnimationPhase("inspecting");
        logAnimationPhase("inspecting");
      }, CENTER_DURATION),
      window.setTimeout(() => {
        setAnimationPhase("zooming");
        logAnimationPhase("zooming");
      }, CENTER_DURATION + INSPECT_DURATION),
      window.setTimeout(() => {
        logAnimationPhase("navigate-survey");
        onNavigate("/survey");
      }, CENTER_DURATION + INSPECT_DURATION + ZOOM_DURATION),
    );
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && canStart) {
      handleStart();
    }
  };

  return (
    <main
      className={`mobile-screen start-screen animation-${animationPhase}`}
      aria-busy={animationPhase !== "idle"}
    >
      {/* Header */}
      <header className="result-header">
        <a className="mini-brand" href="/start" aria-label="도토리 금융 DNA">
          <span className="brand-acorn" aria-hidden="true" />
          DOTORI DNA
        </a>
        <span className="result-step">3 MIN · 7 QUESTIONS</span>
      </header>

      {/* Hero */}
      <section className="start-hero">
        <div className="start-cloud cloud-a" aria-hidden="true" />
        <div className="start-cloud cloud-b" aria-hidden="true" />
        <div className="start-cloud cloud-c" aria-hidden="true" />
        <div className="start-cloud cloud-d" aria-hidden="true" />
        <div className="start-cloud cloud-e" aria-hidden="true" />
        <div className="start-cloud cloud-f" aria-hidden="true" />
        <div className="start-cloud cloud-g" aria-hidden="true" />
        <div className="start-grass grass-a" aria-hidden="true" />
        <div className="start-grass grass-b" aria-hidden="true" />
        <div className="start-grass grass-c" aria-hidden="true" />
        <div className="start-grass grass-d" aria-hidden="true" />
        <div className="start-grass grass-e" aria-hidden="true" />
        <div className="start-grass grass-f" aria-hidden="true" />
        <div className="start-grass grass-g" aria-hidden="true" />
        <span className="start-sticker">나의 돈 성향은?</span>
        <div className="start-title">
          <p>자립을 준비하는 나를 위한</p>
          <h1>
            도토리
            <br />
            <strong>금융 DNA</strong>
          </h1>
          <span className="test-label">TEST</span>
        </div>
        <img
          className="start-character-image"
          src="/acorns/PEAI.png"
          alt="돋보기로 금융 생활을 살펴보는 탐구 도토리"
        />
        <span className="start-alert-mark" aria-hidden="true">!</span>
        <div className="start-transition-lens" aria-hidden="true" />
        <div className="start-hill" aria-hidden="true" />
      </section>

      {/* Checkpoint Note */}
      <section className="start-note">
        <span>CHECK POINT</span>
        <h2>
          나의 금융 위험 신호를
          <br />
          신호등으로 한눈에 확인해요
        </h2>
        <div className="signal-guide">
          <img
            className="signal-illustration"
            src="/illustrations/traffic-light.png"
            alt="안정, 주의, 위험을 나타내는 신호등"
          />
          <div>
            <strong>안정 · 주의 · 위험</strong>
            <p className="checkpoint-copy">
              단계에 맞춰 필요한 도움을 안내해 드려요.
            </p>
          </div>
        </div>
        <div className="nickname-field">
          <input
            id="nickname-input"
            type="text"
            maxLength={12}
            placeholder="닉네임을 입력해 주세요"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <small>
            {nickname.length}/12
          </small>
        </div>
      </section>

      {/* CTA */}
      <button
        type="button"
        className="start-cta"
        disabled={!canStart}
        onClick={handleStart}
      >
        <span>
          {animationPhase === "idle" ? "내 도토리 찾기" : "도토리가 찾는 중"}
        </span>
        <span className="cta-sub">
          {animationPhase === "idle" ? "시작하기 ↗" : "잠시만요"}
        </span>
      </button>
      <span className="animation-status" aria-live="polite">
        {animationPhase === "centering" && "도토리가 화면 가운데로 이동합니다."}
        {animationPhase === "inspecting" && "도토리가 돋보기로 질문을 찾습니다."}
        {animationPhase === "zooming" && "돋보기를 확대해 질문 화면을 엽니다."}
      </span>
      <audio
        ref={motionAudioRef}
        src="/sounds/start-dotori-boing.wav"
        preload="auto"
      />
    </main>
  );
}
