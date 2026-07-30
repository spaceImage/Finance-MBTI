# 🌰 DOTORI - 금융 투자 성향 진단 PoC

React SPA + FastAPI 백엔드 + SQLite 기반의 금융 MBTI 및 위험도 진단 시스템입니다.

## 🏗️ 시스템 구성

```
[React SPA (Port 3001)]
        │  HTTP API
        ▼
  [FastAPI 백엔드 (Port 8001)]
        │  (동기 계산 및 DB 저장)
        ├──▶ [SQLite 파일 (dotori.db)]
        │
        ├──▶ finlife.fss.or.kr   (금감원, 예·적금 실시간 금리)
        ├──▶ apis.data.go.kr     (서민금융진흥원, 청년 대출상품)
        └──▶ youthcenter.go.kr   (온통청년, 청년 정책)
```

> 3개 외부 공공 API는 모두 선택 사항입니다. 인증키가 없거나 호출이 실패해도
> 서비스는 죽지 않고 정적 데이터(`types.json`)로 자동 폴백합니다.
> 아키텍처 상세는 [docs/architecture.md](docs/architecture.md) 참고.

## 🚀 실행 방법

### 0. 환경변수 설정 (선택)
`backend/.env` 파일에 아래 키를 채우면 실시간 금리/정책 데이터가 연동됩니다. 없어도 정상 동작합니다.
```bash
FINLIFE_API_KEY=      # finlife.fss.or.kr 발급 (금감원 금융상품한눈에)
KINFA_API_KEY=        # data.go.kr 발급, "디코딩" 키 사용 (서민금융진흥원)
YOUTHCENTER_API_KEY=  # youthcenter.go.kr 마이페이지 > OPEN API 승인 후 발급
```

### 1. FastAPI 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
python app/main.py
```

### 2. React SPA 실행
```bash
cd frontend
npm install
npm run dev
```

> 브라우저에서 `http://localhost:3001/start` 접속
> API 문서는 `http://localhost:8001/docs`에서 확인

---

## 🛠️ 주요 기능
1. **7문항 금융 진단 (Q1~Q7)**: 목적, 위험감수, 기간, 분석방식, 자산비중, 수익활용, 투자지식
2. **이중 진단 엔진**: 16가지 금융 MBTI 성향 코드 + 위험도 신호등(🟢/🟡/🔴)
3. **맞춤형 3대 금융 상품 추천**: 성향 및 위험도에 맞춘 3개 상품군 매핑, 은행 예·적금 5종은 실시간 금리로 보강
4. **청년 정책·대출상품 조회**: `/youth-products`, `/youth-policies` — 서민금융진흥원·온통청년 API를 키워드 필터로 정제해 제공
5. **SQLite 결합 & Fallback**: 무인증 세션 기록, DB 저장 오류·외부 API 장애 시에도 계산 결과 정상 반환
6. **닉네임 입력 페이지**: 퀴즈 시작 전 닉네임을 받아 결과 화면에 반영
