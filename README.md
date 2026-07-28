# 🌰 DOTORI - 금융 투자 성향 진단 PoC

FastAPI + Next.js(React) + SQLite 기반의 금융 MBTI 및 위험도 신호등(🟢/🟡/🔴) 이중 진단 시스템입니다.

## 🏗️ 시스템 구성 (Step 6 PoC 아키텍처)

```
[React/Vite 클라이언트 (Port 3001)]
        │  (HTTP POST/GET)
        ▼
  [FastAPI 서버 (Port 8001)]
        │  (동기 계산 및 DB 저장)
        ▼
   [SQLite 파일 (dotori.db)]
```

## 🚀 실행 방법

### 1. 백엔드 실행 (FastAPI - Port 8001)
```bash
cd backend
python app/main.py
```
> 백엔드가 구동되면 `http://localhost:8001/docs` 에서 Swagger API문서를 확인할 수 있습니다.

### 2. 프론트엔드 실행 (React - Port 3001)
```bash
cd frontend
cmd /c npm run dev
```
> 브라우저에서 `http://localhost:3001` 접속

---

## 🛠️ 주요 기능
1. **7문항 금융 진단 (Q1~Q7)**: 목적, 위험감수, 기간, 분석방식, 자산비중, 수익활용, 투자지식
2. **이중 진단 엔진**: 16가지 금융 MBTI 성향 코드 + 위험도 신호등(🟢/🟡/🔴)
3. **맞춤형 3대 금융 상품 추천**: 성향 및 위험도에 맞춘 3개 상품군 매핑
4. **SQLite 결합 & Fallback**: 무인증 세션 기록, DB 저장 오류 시에도 계산 결과 정상 반환
