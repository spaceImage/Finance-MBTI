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
> 아키텍처 상세는 [docs/architecture.md](docs/architecture.md), 보안/개인정보 설계는 [docs/security_design.md](docs/security_design.md) 참고.

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
5. **정책/상품 카드 실제 링크 연결**: 온통청년 API에서 유형별로 가장 가까운 정책 상세페이지를 매칭(RED 위험군은 대출성 정책 제외), 은행 예·적금/ETF/로보어드바이저 상품에는 검증된 공식 홈페이지 링크를 큐레이션해 결과 카드에서 바로 이동 가능
6. **결과 이미지 저장**: 결과 히어로 카드를 `html2canvas`로 캡처해 이미지로 다운로드(그림자가 잘려 보이지 않도록 카드 안쪽으로 크롭 처리)
7. **SQLite 결합 & Fallback**: 무인증 세션 기록, DB 저장 오류·외부 API 장애 시에도 계산 결과 정상 반환
8. **닉네임 입력 페이지 & 시작 연출**: 퀴즈 시작 전 닉네임을 받아 결과 화면에 반영, 도토리 마스코트 애니메이션과 효과음으로 시작 화면 연출
9. **공통 헤더 & 반응형 레이아웃**: 전 화면 공통 헤더에 뒤로가기·중앙 브랜드 로고 적용, 모바일 화면까지 대응하는 반응형 레이아웃
