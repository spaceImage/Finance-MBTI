import React, { useState } from 'react';

interface NicknamePageProps {
  onStart: (nickname: string) => void;
}

const MAX_LENGTH = 10;

export const NicknamePage: React.FC<NicknamePageProps> = ({ onStart }) => {
  const [value, setValue] = useState('');
  const [touched, setTouched] = useState(false);

  const trimmed = value.trim();
  const errorMessage =
    trimmed.length === 0
      ? '닉네임을 입력해주세요.'
      : trimmed.length > MAX_LENGTH
      ? `닉네임은 ${MAX_LENGTH}자 이내로 입력해주세요.`
      : null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setTouched(true);
    if (errorMessage) return;
    onStart(trimmed);
  };

  return (
    <div className="page-container">
      <div className="header-logo">
        <span className="logo-icon">🌰</span>
        <span className="logo-text">DOTORI</span>
        <span className="logo-sub">금융 MBTI & 위험도 진단</span>
      </div>

      <form className="nickname-card" onSubmit={handleSubmit}>
        <p className="nickname-lead">진단을 시작하기 전에,</p>
        <h2 className="nickname-title">뭐라고 불러드릴까요?</h2>
        <p className="nickname-desc">
          입력하신 닉네임은 이 세션에서만 사용되고 별도로 저장되지 않아요.
        </p>

        <input
          className="nickname-input"
          type="text"
          value={value}
          maxLength={MAX_LENGTH + 5}
          placeholder="예: 자립왕도토리"
          onChange={(e) => setValue(e.target.value)}
          autoFocus
        />

        {touched && errorMessage && (
          <p className="nickname-error">⚠️ {errorMessage}</p>
        )}

        <button type="submit" className="start-btn">
          진단 시작하기 🌰
        </button>
      </form>
    </div>
  );
};
