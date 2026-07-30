# DOTORI 프로젝트 보안 설계서 (PoC 기준)

**기준 코드**: `backend/app/` (FastAPI + SQLite, 무인증 세션, 3개 외부 공공 API 연동)
**전제**: 이 문서는 원본 "비기능 요구사항 명세서" 9개 항목 중 **6.보안 / 7.개인정보 보호**를 중심으로, 실제 코드베이스 구조에 맞게 채택/축소/제외했습니다. 프로덕션 확장 시 필요한 항목은 "추후 확장" 표로 별도 정리했습니다.

---

## 0. 왜 원본을 그대로 못/안 쓰는가

원본 명세서는 **다중 인스턴스 + Redis/RabbitMQ + PostgreSQL + AWS + Prometheus/PagerDuty** 운영 환경을 전제로 합니다. DOTORI는 현재:

- FastAPI 단일 프로세스 + SQLite 1개 파일 (`backend/dotori.db`)
- 인증 없는 익명 `session_uuid` 세션 하나뿐 (관리자 페이지 없음 → JWT 불필요)
- 이름/연락처/주민번호를 아예 수집하지 않음 (`schemas/diagnosis.py` 확인 결과 `question_id`, `choice_index`만 받음)
- 외부 API 3개(finlife/kinfa/youthcenter)는 이미 **키 미설정 시 빈 리스트 반환 + 6시간 캐시 + 실패 시 이전 캐시 폴백**이 구현되어 있음 (`finlife_client.py`)

따라서 인프라 레벨 보안(WAF, Multi-AZ, Secrets Manager, mTLS 등)은 지금 만들 이유가 없고, **"공개 엔드포인트를 익명으로 두드릴 수 있는 PoC"에 실제로 발생 가능한 위협**에 맞춰 축소했습니다.

---

## 1. 채택 항목 (지금 적용 대상)

### 1-1. 입력 검증 — ✅ 이미 구현됨, 유지
`schemas/diagnosis.py`가 원본 명세의 "Pydantic Schema 기반 choice_index Strict 검증"을 이미 만족합니다.
- `choice_index` 0~3 범위 검증 (`field_validator`)
- 7문항 전부 응답했는지, 중복/미정의 문항 ID 없는지 (`model_validator`)

→ **추가 조치**: 없음. 이 패턴을 새 필드 추가 시에도 그대로 따르면 됨 (자유 텍스트 입력 필드가 생기면 그때 길이 제한 추가 검토).

### 1-2. Rate Limiting — ⚠️ 미구현, 우선순위 높음
원본의 "IP당 초당 10회/분당 100회"는 그대로 가져오되, Slowapi 같은 별도 인프라 대신 **FastAPI 미들웨어 수준의 가벼운 제한**으로 축소 제안합니다.

- 대상: `POST /api/diagnosis/submit` (DB 쓰기 발생), `GET /youth-products`, `/youth-policies` (외부 API 캐시 미스 시 3rd-party 호출 유발)
- 제안 값: IP당 **분당 30회** 수준 (실제 사용자는 세션당 1회 제출이 정상 패턴이므로 넉넉히 잡아도 스팸 방지 효과 있음)
- 이유: 지금 `submit_diagnosis`는 인증도, 요청 빈도 제한도 없어서 동일 세션 UUID를 계속 재전송하며 SQLite에 delete+insert를 반복시키는 것이 가능 (WAL 락 경합 유발 가능)

### 1-3. CORS — ✅ 이미 적절히 제한됨, 배포 시 조정 필요
`config.py`의 `CORS_ORIGINS`는 localhost 4개로 하드코딩되어 있어 지금은 안전합니다.
→ **추가 조치**: 배포 도메인이 정해지면 하드코딩 대신 `.env`의 `CORS_ORIGINS` 값으로 전환 (콤마 구분 문자열 → 리스트 파싱). `allow_origins=["*"]`로 절대 바꾸지 말 것 (지금 `allow_credentials=True`와 같이 쓰면 브라우저가 거부하거나, 향후 쿠키 인증 도입 시 CSRF 노출).

### 1-4. 비밀정보 관리 — ✅ `.env` 분리는 잘 되어 있음, 운영 습관 보강
- `backend/.env`는 `.gitignore`에 등록되어 있고 git 추적 대상 아님을 확인함 (`git ls-files`에 없음, `git check-ignore` 통과).
- **주의**: `.env`에는 finlife/kinfa/youthcenter 실키가 평문으로 들어있음. IDE에서 파일을 열어둔 채 화면 공유·캡처·이 대화창 같은 곳에 **내용을 그대로 붙여넣지 않기** — 지금은 안 붙였지만 습관적으로 조심할 것.
- 확장 시에도 AWS Secrets Manager 같은 별도 서비스는 과함. Render/Railway/Vercel 등 배포 플랫폼의 "Environment Variables" 설정으로 충분.

### 1-5. Rate 이외의 DoS 저항 — Payload 크기
원본의 "JSON 64KB 제한"은 그대로 가져올 필요 없음: `answers`는 스키마상 정확히 7개 항목(`question_id`, `choice_index` 정수 2개)으로 강제되므로 **요청 바디 크기가 애초에 수백 바이트 수준**. 별도 Body Limit 미들웨어는 우선순위 낮음 (추후 확장 표로 이동).

### 1-6. 로그 — 최소한의 마스킹 원칙 유지
- 지금 로그(`logger.error(f"...session {payload.session_uuid}...")`)에는 PII가 없음 (session_uuid는 클라이언트가 생성한 랜덤 UUID일 뿐, 실명/연락처 아님) → 원본의 "010-****-5678 마스킹"은 **해당 데이터 자체가 없으므로 불필요**.
- 다만 원칙은 유지: 앞으로 상담 연계 등으로 연락처를 받는 기능이 생기면, 그 시점에 반드시 로그 마스킹 규칙을 추가할 것.

---

## 2. 개인정보 보호 — 원본 대비 대폭 축소, 그러나 핵심 원칙은 채택

### 2-1. 최소 수집 원칙 — ✅ 이미 원본 취지 이상으로 잘 지켜짐
현재 수집 데이터: `session_uuid`(클라이언트 생성 랜덤값), `question_id`, `choice_index` 뿐. 성명·연락처·주민번호는 스키마에 필드 자체가 없음.

### 2-2. 민감 판단 데이터 — 위기 신호등(🔴/🟡/🟢)은 예외적으로 신경 써야 함
`dual_engine.py`가 계산하는 `risk_color`(RED/YELLOW/GREEN)는 "재정 위기 신호"로, **개인 식별은 안 되지만 민감한 판단 결과**입니다. 원본의 "RED 3년 보존" 같은 정교한 정책은 지금 규모에 과하지만, 아래 최소선은 채택 권장:

| 원본 | DOTORI 축소판 |
|---|---|
| 일반 세션 90일 후 자동 파기 | **보존 기간 정책 자체가 없음 → 최소 이거라도 도입 권장**: `created_at` 기준 일정 기간(예: 90일) 지난 `sessions`/`responses`/`results` 행을 주기적으로 삭제하는 스크립트 (cron 없이 서버 시작 시 1회 체크만 해도 충분한 규모) |
| RED 3년 보존 + 동의 | 지금은 RED라고 별도 상담 연계·개인 식별 저장을 하지 않으므로 **불필요**. 향후 "상담원 연결" 기능에서 연락처를 받는 순간부터만 별도 동의/보존 정책이 필요해짐 |
| AI 입력 전 PII 정규식 필터링 | 외부 LLM 호출이 코드에 없음(정적 JSON 매핑 + 공공 API 호출뿐) → **불필요**. LLM 연동(예: 결과 설명 생성)을 추가하는 순간 재검토 |
| 테스트/프로덕션 DB 분리 | 지금 단일 SQLite 파일 하나뿐이고 `*.db`가 gitignore되어 있음 → 로컬 테스트 시 `DATABASE_URL`을 별도 파일(`test.db`)로 돌리는 정도로 충분, 별도 인프라 불필요 |

### 2-3. 채택 안 하는 항목과 이유
- **AES-256 DB 파일 암호화**: SQLite 파일에 실명·계좌번호가 없고 session_uuid+선택지 인덱스뿐이라 유출되어도 개인 특정이 사실상 불가능. 지금 단계에서는 과설계.
- **TLS 1.3 직접 구현**: 앱 코드가 아니라 배포 플랫폼(리버스 프록시/호스팅)이 처리할 영역. FastAPI/uvicorn에 TLS 코드를 넣지 말고, 배포 시 HTTPS 강제 여부만 체크리스트로 남김.

---

## 3. 제외 항목 요약 (원본 9개 항목 → 처리 결과)

| 원본 항목 | 처리 | 이유 |
|---|---|---|
| 1. 성능(TPS/latency 목표치) | 제외 | 부하 테스트 인프라(K6 등) 없는 학습용 PoC. 실사용자 수십~수백 명 규모에서 SQLite+FastAPI 단일 프로세스로 충분 |
| 2. 가용성(RTO/RPO, Multi-AZ) | 제외 | 단일 서버 PoC. `graceful degradation`(외부 API 실패 시 캐시/정적 폴백)은 이미 코드로 구현되어 있어 실질적 목적은 달성 |
| 3. 확장성(파티셔닝, Read Replica) | 제외 | 트래픽 규모상 불필요. Stateless FastAPI 구조 자체는 이미 되어 있어 필요 시 확장 여지는 있음 |
| 4. 신뢰성(Circuit Breaker, DLT 테이블) | 축소 채택 | Circuit Breaker는 과함. 대신 이미 있는 "캐시 폴백" 패턴 유지. 재시도(`httpx.get` 실패 시 로그만)는 지금 수준으로 충분, DLT 테이블은 데이터 유실이 치명적이지 않은 진단 결과 특성상 불필요 |
| 5. 정합성(배치 재산출, 최종 동기화) | 제외 | 통계 대시보드/외부 연계가 없음. `submit`이 동기 처리로 계산→커밋까지 한 번에 끝남 (원본의 "강한 정합성" 요구는 이미 만족) |
| **6. 보안** | **채택 (축소)** | 위 1절 |
| **7. 개인정보 보호** | **채택 (축소)** | 위 2절 |
| 8. 유지보수성(95% 커버리지, API 버저닝) | 부분 채택 권장이나 이 문서 범위 아님 | 별도 품질 문서에서 다룰 사안 |
| 9. 관측가능성(Prometheus/PagerDuty) | 제외 | 모니터링 인프라 없음. 지금은 `logging.basicConfig` 수준으로 충분, 장애 알림은 사람이 직접 확인하는 규모 |

---

## 4. 지금 바로 할 수 있는 액션 아이템 (우선순위순)

1. **Rate limiting 추가** — `slowapi` 또는 직접 미들웨어로 `/submit`, `/youth-*` 엔드포인트에 IP 기준 분당 제한
2. **CORS_ORIGINS 환경변수화** — 배포 전 하드코딩 리스트를 `.env` 기반으로 전환
3. **오래된 세션 정리 스크립트** — `created_at` 기준 N일 지난 레코드 삭제 (수동 실행 or 서버 시작 시 체크)
4. **README/체크리스트에 "배포 시 HTTPS 강제" 항목 추가** — 코드 변경 아님, 배포 체크리스트

원하시면 1번(Rate limiting)부터 바로 코드에 적용해드릴까요?
