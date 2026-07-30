# 도토리 금융 DNA 디자인 가이드

> **문서 상태: 구현 계약서 / Normative Specification**  
> 이 문서는 참고용 무드보드가 아니라 동일 화면을 재현하기 위한 구현 명세다.  
> `MUST`, `MUST NOT`, `SHOULD`, `MAY`는 각각 필수, 금지, 권장, 선택을 의미한다.

## 0. 정확 복제 규칙

### 0.1 구현자가 따라야 할 우선순위

내용이 충돌할 경우 아래 순서로 판단한다.

1. 이 문서의 **21. 정확 구현 계약**
2. 저장소의 실제 에셋 파일
3. 이 문서의 화면별 명세
4. 이 문서의 공통 디자인 원칙
5. 구현자의 판단

구현자는 이미 명시된 색상, 치수, 문구, 경로를 임의로 “개선”하거나 유사한 값으로 바꾸면 안 된다.

### 0.2 동일 구현의 의미

다음 조건을 모두 만족해야 “동일하게 구현”된 것으로 본다.

- 기준 뷰포트 `390 × 844px`에서 모든 핵심 요소의 위치와 크기가 명세를 따른다.
- 지정된 폰트, 색상, 외곽선, 그림자, 모서리 값이 정확히 적용된다.
- 제공된 PNG 에셋을 대체 이미지, 이모지, CSS 도형으로 바꾸지 않는다.
- 화면 문구와 줄바꿈이 명세와 일치한다.
- 활성, 비활성, 선택, 로딩, 오류 상태가 모두 구현된다.
- `/start → /survey → /` 사용자 흐름이 동일하게 동작한다.
- 브라우저 확대율 100%, DPR과 무관하게 CSS 픽셀 기준 레이아웃을 유지한다.

### 0.3 기준 환경

```yaml
framework: React 19 SPA + Vite
language: TypeScript + React
styling: global CSS
frontend_server: Vite 3001
api_server: FastAPI 8001
database: SQLite
reference_viewport:
  width: 390px
  height: 844px
document_language: ko
color_scheme: light
root_font:
  body: Noto Sans KR
  display: Black Han Sans
```

### 0.4 임의 변경 금지 항목

다음 항목은 명세 변경 없이 바꾸면 안 된다.

- 모바일 캔버스 너비 `390px`
- 좌우 패딩 `16px`
- 핵심 외곽선 색 `#173F32`
- 일반 카드 외곽선 두께 `3px` (`/start`의 전체 배경형 히어로 제외)
- 카드 그림자 방향: 오른쪽 아래
- 시작 화면 히어로 높이 `480px`
- 질문 카드 높이 `258px`
- 제공된 16개 도토리 이미지
- 신호등 이미지 `traffic-light.png`
- 위험 신호 API 값 `GREEN`, `YELLOW`, `RED`
- 닉네임 최대 길이 12자
- 질문 응답값: UI 상태와 API `choice_index` 모두 `0..3`, 미응답은 `-1`

## 1. 문서 목적

이 문서는 **도토리 금융 DNA** 서비스의 시각 언어와 UI 구현 규칙을 정의한다.  
현재 구현된 시작 화면, 설문 화면, 결과 화면을 기준으로 작성했으며, 이후 화면과 컴포넌트를 추가할 때 디자인의 일관성을 유지하기 위한 기준으로 사용한다.

### 적용 범위

- 시작 화면: `/start`
- 금융 성향 설문 화면: `/survey`
- 금융 DNA 결과 화면: `/`
- 공통 헤더, 카드, 버튼, 입력 필드, 상태 표시
- 도토리 캐릭터 및 신호등 일러스트
- 모바일 우선 반응형 동작

### 핵심 사용자

자립을 준비하는 청년이 부담 없이 자신의 금융 습관을 점검하고, 결과와 지원 정보를 쉽게 이해할 수 있어야 한다.

---

## 2. 브랜드 방향

### 한 문장 정의

> 어렵고 긴장될 수 있는 금융 진단을, 친근한 도토리 캐릭터와 손으로 만든 리포트처럼 전달하는 모바일 경험.

### 핵심 인상

1. **친근함**  
   금융 서비스 특유의 딱딱함보다 캐릭터, 둥근 형태, 부드러운 색으로 첫 진입 장벽을 낮춘다.

2. **신뢰감**  
   주요 텍스트와 인터랙션에는 짙은 녹색을 사용하고, 상태·선택·진행 결과를 명확하게 보여준다.

3. **발견의 즐거움**  
   진단 과정을 시험지가 아니라 탐색 활동처럼 느끼게 한다. 스티커, 종이 카드, 손그림 일러스트가 이 역할을 담당한다.

4. **실용성**  
   장식은 정보를 돕는 범위 안에서 사용한다. 질문, 선택지, 결과 요약, 위험 신호가 항상 시각적 우선순위를 가진다.

### 디자인 키워드

- Hand-drawn
- Editorial report
- Acorn character
- Soft nature
- Friendly finance
- Paper and sticker
- Thick outline
- Mobile first

---

## 3. 디자인 원칙

### 3.1 금융 정보는 명확하게, 표현은 부드럽게

- 위험 단계는 색상만으로 전달하지 않는다.
- `안정`, `주의`, `위험`과 같은 텍스트 라벨을 항상 함께 사용한다.
- 경고성 문구도 공포를 조성하기보다 현재 상태와 다음 행동을 설명한다.
- 전문 용어보다 일상적인 한국어를 우선한다.

### 3.2 모든 핵심 요소는 “종이 위 스티커”처럼

- 핵심 카드는 밝은 종이색 배경을 사용한다.
- 카드에는 짙은 외곽선과 오른쪽 아래 방향의 단단한 그림자를 적용한다.
- 작은 라벨은 살짝 회전시켜 붙인 스티커나 테이프처럼 표현한다.
- 지나치게 정돈된 기업형 UI보다 작은 비대칭을 허용한다.

### 3.3 캐릭터는 설명을 돕는 조력자

- 캐릭터가 정보보다 먼저 읽히지 않도록 배치한다.
- 결과 유형을 구분하거나 탐색·성장·안정의 정서를 보조할 때 사용한다.
- 입력 필드, 선택지, 본문 위에 캐릭터가 겹치지 않게 한다.

### 3.4 한 화면에는 하나의 주요 행동

- 시작 화면: `내 도토리 찾기`
- 설문 화면: 답변 선택
- 결과 화면: 결과 확인 및 저장
- 주요 행동 버튼은 짙은 녹색으로 통일한다.
- 보조 행동은 종이색 또는 테두리 버튼으로 표현한다.

### 3.5 장식보다 읽기 순서가 우선

기본 정보 위계는 다음 순서를 따른다.

1. 화면 목적 또는 질문
2. 핵심 캐릭터·결과 유형
3. 설명 또는 답변 선택지
4. 보조 정보
5. 다음 행동

---

## 4. 레이아웃 시스템

### 4.1 기준 화면

| 항목 | 기준 |
|---|---:|
| 모바일 캔버스 너비 | `390px` |
| 공통 캔버스 최소 높이 | `1000px` |
| 좌우 기본 패딩 | `16px` |
| 상단 패딩 | `18px` |
| 하단 패딩 | `24px` |
| 콘텐츠 기준 너비 | `358px` |

현재 `#root`는 `width: 100%`인 세로 Flex 셸이며, `.mobile-screen`,
`.result-screen`은 `width: 100%`와 `max-width: 390px`을 함께 사용한다. 작은 화면에서는 부모 너비로
축소되고 PC에서는 `390px`을 넘지 않는다.

```css
.mobile-screen,
.result-screen {
  width: 100%;
  max-width: 390px;
  min-height: 1000px;
  padding: 18px 16px 24px;
}
```

화면 너비는 브레이크포인트로 전환하지 않고 항상 `width: 100%`와
`max-width: 390px`을 함께 사용한다. 폭이 명확한 `#root`를 기준으로 계산하여
PC에서 캔버스가 축소되는 것을 방지한다. 작은 화면에서는 부모의 실제 콘텐츠
너비로 축소되고, 넓은 화면에서는 `390px`에서 멈춘다. `100vw`는 세로
스크롤바가 있는 PC 브라우저에서 스크롤바 너비까지 포함해 약 `15px`의
가로 오버플로를 만들 수 있으므로 사용하지 않는다.

### 4.2 정렬 원칙

- 데스크톱에서도 모바일 캔버스 비율을 유지한다.
- 현재 구현은 캔버스를 화면 상단·수평 중앙에 배치한다.
- 데스크톱 중앙 정렬은 전체 페이지 셸을 세로 Flex 컨테이너로 구성하고
  `align-items: center`로 처리한다. Grid의 퍼센트 폭과 `max-width` 조합에서
  발생할 수 있는 캔버스 폭 축소를 피하며, 모바일 캔버스 내부 치수는 유지한다.
- 카드 내부 텍스트는 기본적으로 왼쪽 정렬한다.
- 상태 숫자나 글자 수처럼 짧은 보조 정보만 오른쪽 정렬한다.

### 4.3 간격 체계

현재 스타일에 맞는 권장 간격 단위는 다음과 같다.

| 단계 | 값 | 용도 |
|---|---:|---|
| XS | `4px` | 아이콘과 짧은 라벨 사이 |
| S | `8px` | 카드 내부 작은 요소 |
| M | `12px` | 컴포넌트 내부 기본 간격 |
| L | `16px` | 화면 좌우 패딩, 섹션 내부 |
| XL | `18–20px` | 섹션 사이 |
| 2XL | `24–30px` | 주요 카드의 넓은 내부 여백 |

간격은 기계적으로 한 값만 반복하지 않는다. 손으로 구성한 편집물의 리듬을 살리되, 같은 유형의 컴포넌트 안에서는 일관된 값을 사용한다.

---

## 5. 컬러 시스템

### 5.1 핵심 토큰

| 토큰 | HEX | 역할 |
|---|---|---|
| `--ink` | `#173F32` | 기본 텍스트, 외곽선, 강한 대비 |
| `--cream` | `#FFF7DF` | 전체 모바일 화면 배경 |
| `--paper` | `#FFFDF4` | 카드, 선택지, 보조 버튼 |
| `--sky` | `#9EDAF1` | 히어로·질문 카드 배경 |
| `--grass` | `#8FC77A` | 진행 상태, 언덕, 긍정적 장식 |
| `--green` | `#397C55` | 중간 녹색, 잎과 보조 요소 |
| `--pine` | `#245943` | 주요 버튼, 진한 카드, 그림자 |
| `--brown` | `#7C4829` | 도토리 모자와 자연 소재 |
| `--tan` | `#D9A86C` | 도토리 몸통 |

### 5.2 보조 컬러

| 색상 | HEX | 사용처 |
|---|---|---|
| Soft mint | `#D8EFC8` | 입력 필드, 선택 상태, 안내 카드 |
| Shadow green | `#6EA56A` | 종이 카드의 깊은 그림자 |
| Soft shadow | `#ABC89C` | 선택지와 작은 카드 그림자 |
| Sticker yellow | `#F1C879` | 질문 번호, 테이프 라벨 |
| Muted text | `#547365` | 설명, 보조 문구 |
| Focus green | `rgba(57,124,85,.2)` | 입력 포커스 링 |

### 5.3 위험 신호 컬러

| 단계 | 배경/등 색상 | 의미 |
|---|---|---|
| 안정 | `#D7EBC6`, `#62A86D` | 현재 습관을 유지해도 되는 상태 |
| 주의 | `#FFF0B8`, `#EFBD3E` | 점검과 조정이 필요한 상태 |
| 위험 | `#F6C5B8`, `#DF6A55` | 즉각적인 보호 행동과 지원 안내가 필요한 상태 |

#### 사용 규칙

- 위험 신호는 빨강·노랑·초록만 단독으로 사용하지 않는다.
- 아이콘 또는 일러스트와 단계명, 설명을 함께 제공한다.
- 넓은 면에 순수 원색을 사용하지 않는다. 파스텔 배경과 진한 외곽선을 조합한다.
- 본문 텍스트는 위험 단계와 무관하게 `--ink` 계열을 유지해 가독성을 확보한다.

### 5.4 페이지 외부 배경

PC에서 모바일 캔버스 바깥에 생기는 좌우 영역은 흰색이나 회녹색을 사용하지
않고 앱의 크림색 `#FFF7DF`로 채운다. 모바일 캔버스는 가로 중앙에 배치하며
세로는 상단 정렬을 유지한다.

---

## 6. 타이포그래피

### 6.1 서체

| 역할 | 서체 | 굵기 |
|---|---|---|
| 대형 제목·질문 | `Black Han Sans` | Regular |
| 본문·버튼·라벨 | `Noto Sans KR` | 500–900 |
| 대체 서체 | sans-serif | 시스템 기본 |

```css
@import url("https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@500;600;700;800;900&display=swap");
```

두 서체는 모두 SIL Open Font License 1.1로 배포된다. 상업용 웹 서비스에
사용·임베드할 수 있으므로 G마켓 산스로 교체하지 않는다. 폰트 파일 자체를
단독 판매하면 안 되며, 폰트를 재배포할 때는 해당 라이선스를 함께 제공한다.

- [Black Han Sans 공식 OFL](https://github.com/google/fonts/blob/main/ofl/blackhansans/OFL.txt)
- [Noto Sans KR 공식 OFL](https://github.com/google/fonts/blob/main/ofl/notosanskr/OFL.txt)

### 6.2 권장 타입 스케일

| 용도 | 크기 | 행간 | 굵기 |
|---|---:|---:|---:|
| 시작 화면 브랜드 제목 | `55px` | `0.9` | Black Han Sans |
| 결과 유형 강조 | `36px` | `1.05` | Black Han Sans |
| 설문 질문 | `27px` | `1.25` | Black Han Sans |
| 카드 제목 | `20px` | `1.4` | 800–900 |
| 주요 CTA | `20px` | `1.25` | 900 |
| 본문 강조 | `16px` | `1.5` | 800 |
| 일반 본문 | `11–12px` | `1.4–1.55` | 600–800 |
| 메타 라벨 | `8–10px` | `1.2–1.4` | 900 |

### 6.3 자간

- 큰 한글 제목: `-0.04em`에서 `-0.05em`
- 일반 한글 본문: `-0.02em`에서 `-0.035em`
- 영문 메타 라벨: `0.09em`에서 `0.16em`
- 작은 텍스트에 과도한 음수 자간을 사용하지 않는다.

### 6.4 카피 톤

- 존댓말을 사용한다.
- 한 문장은 짧고 명확하게 쓴다.
- 결과 설명은 단정 대신 가능성과 다음 행동을 제안한다.
- “실패”, “나쁨”, “문제 있음” 같은 낙인 표현을 피한다.
- 예: “점검할 시점이에요”, “차근차근 회복 계획을 세울 수 있어요.”

---

## 7. 형태와 표면

### 7.1 외곽선

기본 외곽선은 `3px solid #173F32`이다.

```css
:root {
  --outline: 3px solid var(--ink);
}
```

- 대형 카드와 주요 버튼: `3px`
- 작은 라벨과 입력 필드: `2px`
- 작은 내부 장식: `1.5–2px`

### 7.2 모서리

완벽히 동일한 반경보다 약간 비대칭인 반경을 사용한다.

```css
border-radius: 18px 12px 20px 14px;
```

권장 범위:

- 대형 히어로 카드: `12–20px`
- 일반 카드: `10–18px`
- 버튼: `9–10px`
- 입력 필드: 높이의 절반인 완전한 캡슐형
- 작은 칩: `999px` 또는 `7–20px`

### 7.3 그림자

부드러운 블러 그림자보다 단단한 오프셋 그림자를 사용한다.

| 대상 | 권장 그림자 |
|---|---|
| 히어로 카드 | `8px 9px 0 var(--pine)` |
| 종이 카드 | `7px 8px 0 #6EA56A` |
| 주요 버튼 | `6px 7px 0 var(--ink)` |
| 선택지 | `4px 5px 0 #ABC89C` |
| 작은 스티커 | `4px 4px 0 var(--ink)` |

그림자는 항상 오른쪽 아래 방향으로 두어 종이 조각이 쌓인 인상을 만든다.

### 7.4 회전

- 스티커와 일러스트에는 `-3deg`에서 `3deg` 사이의 작은 회전을 허용한다.
- 본문, 입력 필드, 주요 버튼은 회전시키지 않는다.
- 한 화면에서 회전 요소가 지나치게 많아지지 않도록 2–4개 이하로 제한한다.

---

## 8. 공통 컴포넌트

### 8.1 모바일 화면 셸

클래스:

- `.mobile-screen`
- `.result-screen`

역할:

- 기준 너비와 기본 패딩 제공
- 크림색 종이 배경 제공
- 화면별 최소 높이 유지

### 8.2 공통 헤더

구성:

- 왼쪽: 심볼과 `DOTORI DNA`
- 오른쪽: 진행 또는 결과 메타 정보

규칙:

- 높이 `38px`
- 텍스트 크기 `10px`
- 굵기 `900`
- 영문 자간 `0.12em`
- 브랜드 링크는 시작 화면으로 이동

진행 문구 예시:

- `3 MIN · 7 QUESTIONS`
- `QUESTION 03 / 07`
- `RESULT 01`

### 8.3 브랜드 심볼

현재 `.brand-acorn`은 `18×18px`의 단순 외곽선 심볼이다.

- 시각적으로 도토리 실루엣을 연상시키는 둥근 형태
- 약 `-8deg` 회전
- 헤더 내에서만 작은 크기로 사용
- 캐릭터 일러스트를 대신하는 로고가 아니라 보조 브랜드 표시로 취급

### 8.4 스티커 라벨

사용처:

- 히어로 상단 주제
- `CHECK POINT`
- `Q. 01`
- `DNA REPORT`

스타일:

- 2px 짙은 녹색 테두리
- 노랑, 크림 또는 연두 배경
- 4px 오프셋 그림자
- 9–11px, 굵기 900
- 2–3도 회전

라벨은 최대 한 줄로 유지하며, 문장보다 짧은 명사형을 사용한다.

### 8.5 주요 버튼

예: `.start-cta`, `.survey-next`, `.save-button`

- 배경: `--pine`
- 텍스트: 흰색
- 외곽선: `3px solid --ink`
- 오른쪽 아래 그림자
- 굵기: `900`
- 행동 방향을 나타내는 화살표를 오른쪽에 배치 가능

#### 상태

| 상태 | 표현 |
|---|---|
| 기본 | 짙은 녹색 + 강한 그림자 |
| Hover | 데스크톱에서만 `translateY(-1px)` 정도 허용 |
| Active | 그림자 감소, `translate(2px, 2px)` |
| Focus | 외부 포커스 링 표시 |
| Disabled | `opacity: .45–.5`, 그림자 축소, 금지 커서 |

### 8.6 보조 버튼

- 종이색 배경
- 짙은 녹색 테두리
- 그림자 없이 사용 가능
- 이전 질문, 취소, 닫기 등 보조 행동에 사용

### 8.7 입력 필드

닉네임 입력 기준:

- 높이 `58px`
- 캡슐형 `29px` 반경
- 도토리색 배경 `#D9A86C`
- 2px 테두리
- 입력 텍스트 `15px / 800`
- 플레이스홀더와 글자 수 표시는 짙은 도토리색 `#7C4829`
- 오른쪽에 글자 수 표시
- 포커스 시 반투명 도토리색 링

검증 메시지가 추가될 경우 입력 바로 아래에 배치하며, 빨강만 사용하지 말고 문구와 아이콘을 함께 제공한다.

### 8.8 종이 카드

예: `.start-note`

- 배경 `--paper`
- 3px 외곽선
- 비대칭 모서리
- 녹색 오프셋 그림자
- 상단에 테이프 또는 라벨 부착 가능

`.summary-card`는 결과 화면 전용 배경 `#D7FAF7`을 사용하므로 이 공통
`--paper` 배경 규칙의 대상에서 제외한다.

### 8.9 추천 사각형 설명 영역

- 2열 그리드
- 별도의 추천 카드 배경과 테두리는 사용하지 않음
- 추천 제목과 부가 설명만 베이지 `#F2DFC0` 사각형 영역 안에 배치
- 별도의 `정부지원`, `은행권` 카테고리 문구나 상단 라벨은 표시하지 않음
- 작은 화면에서도 각 항목의 최소 너비가 깨지지 않게 `minmax(0, 1fr)` 사용

### 8.10 답변 선택지

구성:

1. 알파벳 원형 인덱스
2. 답변 텍스트
3. 선택 표시 원

기본:

- 최소 높이 `72px`
- 종이색 배경
- 2px 테두리
- 연두색 오프셋 그림자

선택:

- 배경을 `#D8EFC8`로 변경
- 그림자를 `--pine`으로 강화
- 인덱스와 체크 원을 짙은 녹색으로 채움
- `translateX(2px)`로 선택 반응을 표현

### 8.11 진행 표시줄

- 높이 `12px`
- 종이색 트랙
- 2px 테두리
- 잔디색 진행 바
- 오른쪽에 정수 퍼센트를 표시
- 진행 바 애니메이션을 추가할 경우 `200–300ms ease-out` 범위를 권장

---

## 9. 일러스트레이션 시스템

### 9.1 공통 스타일

- 굵고 약간 불규칙한 짙은 녹색 외곽선
- 파스텔 자연색
- 수채화 또는 종이 질감이 느껴지는 내부 표면
- 둥글고 단순한 실루엣
- 작은 크기에서도 주제가 식별되는 구성
- 현실적인 광원보다 단순한 크림색 하이라이트
- 사진처럼 사실적인 표현, 3D 렌더, 얇은 벡터 선은 사용하지 않는다.

### 9.2 도토리 캐릭터

경로:

```text
frontend/public/acorns/{TYPE_CODE}.png
```

현재 16개 금융 DNA 유형별 캐릭터를 사용한다.

규칙:

- 결과 화면에서는 해당 유형 코드를 파일명으로 연결한다.
- 캐릭터의 전체 실루엣이 잘리지 않도록 `object-fit: contain`을 사용한다.
- 캐릭터 아래에는 약한 드롭 섀도만 허용한다.
- 유형별 캐릭터의 크기와 바닥선은 가능한 한 일정하게 맞춘다.

### 9.3 신호등 일러스트

경로:

```text
frontend/public/illustrations/traffic-light.png
```

역할:

- 안정·주의·위험의 세 단계를 하나의 친근한 오브젝트로 설명
- 기존 원형 이모지 나열을 대체
- 시작 화면의 금융 위험 신호 안내에 사용

스타일:

- 짙은 녹색 외곽선
- 차분한 녹색 본체
- 위에서부터 빨강, 노랑, 초록
- 투명 배경 PNG
- 텍스트와 라벨은 이미지 안에 포함하지 않음

현재 표시 크기:

```css
.signal-illustration {
  width: 56px;
  height: 68px;
  object-fit: contain;
}
```

#### 이미지 생성에 사용한 최종 프롬프트

```text
Use case: stylized-concept
Asset type: compact transparent website illustration for a Korean mobile financial personality quiz
Primary request: Create one charming hand-drawn traffic-light illustration representing three financial risk stages: green safe, yellow caution, red danger.
Subject: a single small vintage traffic-light object with three circular lamps stacked vertically, friendly rounded proportions, slightly irregular hand-drawn shape, chunky dark forest-green outline, tiny side bolts and a short base.
Style/medium: cute Korean editorial sticker illustration matching a pastel acorn-themed mobile web app; warm paper texture, thick imperfect ink outlines, simple flat shapes.
Color palette: dark forest green #173F32, muted pine #547365, pastel red #DF6A55, mustard yellow #EFBD3E, soft green #62A86D, cream highlights #FFFbed.
Constraints: no text, no labels, no watermark, no cast shadow, no reflection.
```

### 9.4 이미지 제작 체크리스트

- [ ] 배경이 투명한가?
- [ ] 56–90px 높이에서도 형태가 구분되는가?
- [ ] 짙은 녹색 외곽선이 유지되는가?
- [ ] 앱 팔레트 밖의 네온 색상이 없는가?
- [ ] 이미지 내부에 작은 텍스트가 없는가?
- [ ] 주요 콘텐츠를 가리지 않는가?
- [ ] 장식용 이미지에는 빈 `alt`, 의미 전달 이미지에는 설명형 `alt`가 있는가?

---

## 10. 화면별 디자인 명세

## 10.1 시작 화면 `/start`

### 화면 목적

- 서비스 성격을 빠르게 이해시킨다.
- 금융 진단에 대한 긴장을 완화한다.
- 닉네임을 입력하고 설문을 시작하게 한다.

### 구성 순서

1. 공통 헤더
2. 전체 배경으로 확장된 하늘·언덕 히어로
3. `CHECK POINT` 종이 카드
4. 닉네임 입력
5. 주요 CTA

### 전체 배경형 히어로

- 높이 `480px`
- 헤더와 좌우 여백까지 이어지는 전체 파란 하늘 배경
- 화면 중간부터 체크포인트 카드 바깥까지 이어지는 넓은 잔디 언덕
- 제목을 가리지 않는 하늘 영역에 반투명 구름 군집 7개
- 초록 언덕에는 둥근 도트형 풀 군집 7개
- 왼쪽에 큰 브랜드 제목
- 오른쪽 아래에 탐구 도토리
- 상단에 노란 질문 스티커
- 히어로 자체의 사각형 테두리, 둥근 모서리, 카드 그림자는 사용하지 않음

제목은 `도토리 / 금융 DNA` 두 줄로 구성하고 크림색 채움과 짙은 외곽선을
사용한다. 가독성을 떨어뜨리는 `text-shadow`는 사용하지 않는다.

### 신호등 안내 카드

클래스: `.signal-guide`

- 신호등 일러스트와 설명을 좌우로 배치
- 배경 `#D8EFC8`
- 2px 외곽선
- 작은 녹색 그림자
- 높이 최소 `78px`
- `안정 · 주의 · 위험`을 텍스트로 명시

신호등은 의미 전달 이미지이므로 `alt="안정, 주의, 위험을 나타내는 신호등"`을 사용한다.

### 닉네임 입력

- 최대 12자
- 입력값이 없으면 CTA 비활성화
- Enter 키로도 시작 가능
- 입력값은 세션 저장소에 보관

---

## 10.2 설문 화면 `/survey`

### 화면 목적

- 현재 진행 위치를 명확하게 전달한다.
- 한 번에 하나의 질문에만 집중하게 한다.
- 답을 고르면 자연스럽게 다음 질문으로 이동시킨다.

### 구성 순서

1. 공통 헤더
2. 진행률
3. 질문 카드
4. 답변 선택지
5. 이전 버튼과 자동 진행 설명

### 질문 카드

- 높이 `258px`
- 하늘색 배경
- 오른쪽 아래 잔디 장식
- 왼쪽 위 질문 번호 스티커
- 오른쪽 위 원형 질문 아이콘
- 주제 → 질문 → 안내 문구 순서

### 답변 상호작용

- 답변 하나만 선택 가능
- 선택 즉시 명확한 시각 상태 제공
- 제출 중에는 선택지 비활성화
- 마지막 질문에서는 결과 생성 안내 표시

### 상태 화면

다음 상태는 같은 모바일 셸을 사용한다.

- 질문 불러오는 중
- 오류
- 결과 생성 중

향후 `.status-message`에 다음을 추가하는 것을 권장한다.

- 화면 중앙 정렬
- 작은 도토리 로딩 일러스트
- 재시도 가능한 오류에는 명확한 재시도 버튼

---

## 10.3 결과 화면 `/`

### 화면 목적

- 사용자의 금융 DNA 유형을 가장 먼저 전달한다.
- 성향 요약과 추천 정보를 제공한다.
- 위험 신호를 부담스럽지 않게 설명한다.
- 결과 저장 행동으로 연결한다.

### 구성 순서

1. 공통 헤더
2. 유형 히어로 카드
3. DNA 리포트 및 추천 카드
4. 위험 신호 카드
5. 결과 저장 버튼

### 유형 히어로

- 유형 코드와 유형 라벨
- 유형 이름
- 유형별 도토리 캐릭터
- 하늘과 잔디 배경
- 닉네임 스티커

캐릭터 이미지는 다음 규칙으로 연결한다.

```tsx
<img src={`/acorns/${code}.png`} alt={typeNames[code]} />
```

### DNA 리포트

- 배경 `#D7FAF7`
- 상단 노란 `DNA REPORT` 테이프
- `[성향] 캐릭터명 — 위험등급` 형식의 요약 문구는 표시하지 않음
- 정부지원 및 은행권 추천 내용은 카테고리명 없이 2열로 배치
- 베이지 `#F2DFC0` 사각형 설명 영역을 표시
- 제목과 부가 설명만 사각형 영역 안에 표시
- 핵심 키워드는 중앙 정렬된 큰 캡슐형 칩으로 표시

### 위험 신호 카드

세 단계에 따라 카드 배경이 달라진다.

```text
GREEN  → risk-green
YELLOW → risk-yellow
RED    → risk-red
```

정보 구조:

1. `RISK SIGNAL`
2. 단계명
3. 우려
4. 기대 또는 다음 행동

현재 결과 카드에서 이모지를 사용하고 있으나, 시작 화면과 완전히 통일하려면 향후 같은 신호등 일러스트의 단계별 변형 또는 코드 기반 램프 아이콘으로 교체하는 것을 권장한다.

---

## 11. 인터랙션과 모션

### 11.1 기본 원칙

- 빠르고 짧게 반응한다.
- 화려한 전환보다 선택 상태와 진행 변화에 집중한다.
- 멀미를 유발하는 큰 이동이나 반복 애니메이션은 피한다.

### 11.2 권장 시간

| 상호작용 | 시간 |
|---|---:|
| 버튼 hover/active | `120–160ms` |
| 선택지 상태 변경 | `160–220ms` |
| 진행률 증가 | `200–300ms` |
| 화면 전환 | `220–320ms` |

### 11.3 권장 움직임

- 버튼 active: `translate(2px, 2px)`와 그림자 축소
- 선택지: 배경·그림자·체크 상태 전환
- 카드 진입: `opacity`와 `translateY(6px)`의 짧은 조합
- 장식 캐릭터의 지속적인 흔들림은 사용하지 않거나 매우 약하게 제한

### 11.4 모션 접근성

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

---

## 12. 접근성

### 12.1 색상

- 색상 하나만으로 선택·오류·위험 상태를 표현하지 않는다.
- 위험 단계명과 설명을 함께 제공한다.
- 작은 본문은 연한 색 위에서 충분한 대비를 유지한다.

### 12.2 키보드

- 모든 버튼과 링크는 Tab으로 접근 가능해야 한다.
- 포커스 상태를 제거하지 않는다.
- 닉네임 입력에서 Enter로 시작할 수 있다.
- 답변 선택 후 자동 이동이 키보드 사용자에게 혼란을 주지 않도록 포커스 이동을 관리한다.

### 12.3 이미지 대체 텍스트

- 의미 있는 캐릭터: 유형명 또는 역할을 설명
- 신호등: 세 위험 단계를 설명
- 구름, 언덕, 잔디선 등 순수 장식: `aria-hidden="true"` 또는 빈 `alt`

### 12.4 터치 영역

- 주요 버튼 높이: 최소 `44px`
- 답변 선택지: 현재 `72px`로 충분
- 작은 링크나 칩을 행동 요소로 사용할 경우 최소 터치 영역을 별도로 확보

### 12.5 문장과 가독성

- 10px 이하 텍스트는 메타 정보에만 제한한다.
- 핵심 설명은 가능하면 11px 이상을 유지한다.
- 긴 문단은 2–4줄 단위로 나눈다.
- 카드 안에서 텍스트가 배경 일러스트와 겹치지 않게 한다.

---

## 13. 반응형 규칙

### 현재 규칙

- `390px` 이상: 390px 모바일 캔버스를 유지
- 모든 화면: `#root { width: 100% }`, 캔버스 `width: 100%; max-width: 390px` 적용

### 추가 권장 규칙

#### 360px 이하

- 큰 제목을 약 5–8% 축소
- 추천 카드가 지나치게 좁아지면 1열로 전환
- 신호등 안내 카드의 텍스트 줄바꿈 확인

#### 데스크톱

- 모바일 캔버스를 페이지 중앙에 배치
- 외부 배경은 앱과 동일한 크림색 `#FFF7DF` 유지
- 앱 너비를 무리하게 늘리지 않는다.

#### 안전 영역

iOS 전체 화면 환경에서는 다음 패딩을 고려한다.

```css
padding-bottom: calc(24px + env(safe-area-inset-bottom));
```

---

## 14. 콘텐츠 및 데이터 매핑

### 금융 DNA 유형

서비스는 16개 유형 코드를 캐릭터 이미지 및 유형명과 연결한다.

```text
PEAS, PEAI, PERS, PERI
PVRS, PVRI, PVAS, PVAI
FEAS, FEAI, FERS, FERI
FVRS, FVRI, FVAS, FVAI
```

새 유형을 추가하거나 이름을 변경할 때 다음 항목을 함께 갱신한다.

1. 유형명
2. 유형 라벨
3. 요약 문구
4. 캐릭터 PNG
5. 결과 추천
6. 위험 신호
7. 이미지 대체 텍스트

### 위험 신호

API 값은 다음 세 값만 사용한다.

```text
GREEN
YELLOW
RED
```

UI에서는 API 코드를 직접 노출하지 않고 한국어 단계명으로 변환한다.

---

## 15. 파일 구조

```text
frontend/
├─ public/
│  ├─ acorns/
│  │  ├─ PEAI.png
│  │  └─ ...
│  └─ illustrations/
│     └─ traffic-light.png
└─ src/
   ├─ app/
   │  ├─ globals.css
   │  ├─ page.tsx
   │  ├─ start/page.tsx
   │  └─ survey/page.tsx
   ├─ components/
   │  ├─ quiz/
   │  └─ result/
   ├─ hooks/
   └─ services/
```

### 관리 원칙

- 화면 공통 토큰은 `globals.css`의 `:root`에 둔다.
- 두 화면 이상에서 재사용되는 UI는 컴포넌트로 분리한다.
- 일러스트는 의미와 역할에 따라 `acorns`, `illustrations` 등으로 분류한다.
- 파일명은 영문 소문자와 하이픈을 기본으로 한다.
- 이미지 교체 시 기존 URL을 유지하면 캐시 무효화 전략을 함께 고려한다.

---

## 16. 구현 권장 사항

### 16.1 디자인 토큰 확장

현재 색상 중심 토큰을 다음과 같이 확장하는 것을 권장한다.

```css
:root {
  --ink: #173f32;
  --cream: #fff7df;
  --paper: #fffdf4;
  --sky: #9edaf1;
  --grass: #8fc77a;
  --green: #397c55;
  --pine: #245943;

  --mint-soft: #d8efc8;
  --yellow-soft: #fff0b8;
  --red-soft: #f6c5b8;
  --text-muted: #547365;

  --border-strong: 3px solid var(--ink);
  --border-medium: 2px solid var(--ink);

  --shadow-card: 7px 8px 0 #6ea56a;
  --shadow-button: 6px 7px 0 var(--ink);

  --radius-card: 14px;
  --radius-control: 10px;
}
```

### 16.2 컴포넌트 분리 후보

- `AppHeader`
- `StickerLabel`
- `PaperCard`
- `PrimaryButton`
- `SignalGuide`
- `ProgressBar`
- `AnswerOption`
- `RiskSignalCard`

### 16.3 이미지 최적화

- 캐릭터와 신호등 PNG의 실제 표시 크기에 맞는 리사이즈 버전을 제공한다.
- 투명 영역이 과도하게 넓은 이미지는 여백을 제거한다.
- 품질 차이가 없다면 WebP도 고려한다.
- `<img>`에는 명시적인 크기 또는 CSS 레이아웃 크기를 지정해 이동을 방지한다.

---

## 17. 금지 사항

- 순수 검정 `#000000`을 주요 외곽선으로 사용하지 않는다.
- 네온색, 강한 보라색, 차가운 기업형 파랑을 새 주조색으로 추가하지 않는다.
- 블러가 큰 회색 그림자를 사용하지 않는다.
- 카드마다 서로 다른 그림자 방향을 사용하지 않는다.
- 동일 화면에서 3개 이상의 서체를 혼합하지 않는다.
- 위험 신호를 이모지만으로 표현하지 않는다.
- 작은 이미지 안에 긴 한국어 문구를 직접 넣지 않는다.
- 캐릭터를 늘이거나 비율을 변형하지 않는다.
- 정보 카드 위에 장식을 겹쳐 본문 가독성을 낮추지 않는다.
- disabled 버튼을 색상 변화 없이 그대로 두지 않는다.

---

## 18. QA 체크리스트

### 시각

- [ ] 모바일 캔버스 너비와 패딩이 기준과 일치한다.
- [ ] 카드 외곽선과 그림자 방향이 일관적이다.
- [ ] 큰 제목에 지정 서체와 자간이 적용됐다.
- [ ] 새 색상이 기존 자연 계열 팔레트 안에 있다.
- [ ] 스티커 회전이 과도하지 않다.
- [ ] 캐릭터 또는 일러스트가 잘리지 않는다.

### 기능

- [ ] 닉네임이 없을 때 시작 버튼이 비활성화된다.
- [ ] 12자 제한과 글자 수가 일치한다.
- [ ] 답변 선택 상태가 즉시 보인다.
- [ ] 이전 질문 버튼의 비활성 상태가 명확하다.
- [ ] 결과 유형과 캐릭터 이미지가 올바르게 연결된다.
- [ ] 위험 신호 배경과 문구가 API 값에 맞는다.

### 접근성

- [ ] 모든 의미 있는 이미지에 적절한 `alt`가 있다.
- [ ] 장식 요소가 스크린 리더에 불필요하게 노출되지 않는다.
- [ ] 포커스 표시가 보인다.
- [ ] 색상 외에도 상태를 구분할 수 있다.
- [ ] 터치 영역이 최소 44px 이상이다.
- [ ] 200% 확대에서도 핵심 콘텐츠가 잘리지 않는다.

### 반응형

- [ ] 390px에서 기준 레이아웃과 일치한다.
- [ ] 375px와 360px에서 가로 스크롤이 없다.
- [ ] 긴 닉네임과 긴 답변에서도 카드가 깨지지 않는다.
- [ ] 데스크톱에서 모바일 캔버스 밖 배경이 자연스럽다.

---

## 19. 변경 관리

디자인을 변경할 때 다음 순서로 검토한다.

1. 기존 디자인 원칙에 맞는지 확인
2. 새 값이 필요한지, 기존 토큰으로 해결할 수 있는지 확인
3. 공통 컴포넌트에 영향이 있는지 확인
4. 시작·설문·결과 화면을 모두 시각 검수
5. 390px, 375px, 360px에서 반응형 검수
6. 키보드와 스크린 리더 의미 검수
7. `design.md`와 실제 구현을 함께 갱신

문서와 코드가 다를 경우 현재 배포된 코드가 동작의 기준이지만, 차이를 방치하지 않고 같은 변경 작업 안에서 문서를 갱신한다.

---

## 20. 현재 디자인의 핵심 요약

도토리 금융 DNA의 디자인은 다음 공식으로 요약할 수 있다.

> 크림색 종이 배경 + 짙은 녹색 손그림 외곽선 + 파스텔 자연색 + 단단한 오프셋 그림자 + 도토리 캐릭터 + 짧고 다정한 금융 안내

새 화면이나 에셋이 이 공식에서 크게 벗어나면, 기능적으로 맞더라도 서비스의 일부처럼 보이지 않을 가능성이 높다. 새로운 요소는 기존 요소를 그대로 복제하기보다 이 공식을 유지하면서 목적에 맞게 변형한다.

---

# 21. 정확 구현 계약

이 장은 Git 저장소를 전달받은 개발자 또는 코딩 에이전트가 화면을 자의적으로 해석하지 않고 동일하게 구현하기 위한 최종 계약이다.

## 21.1 저장소 기준 경로

프로젝트 루트에서 다음 경로를 MUST 유지한다.

```text
frontend/
├─ package.json
├─ vite.config.ts
├─ index.html
├─ src/
│  ├─ main.tsx
│  ├─ App.tsx
│  ├─ styles.css
│  ├─ pages/
│  │  ├─ ResultPage.tsx
│  │  ├─ StartPage.tsx
│  │  └─ SurveyPage.tsx
│  ├─ hooks/useQuizSession.ts
│  └─ services/api.ts
└─ public/
   ├─ acorns/
   │  ├─ FEAI.png
   │  ├─ FEAS.png
   │  ├─ FERI.png
   │  ├─ FERS.png
   │  ├─ FVAI.png
   │  ├─ FVAS.png
   │  ├─ FVRI.png
   │  ├─ FVRS.png
   │  ├─ PEAI.png
   │  ├─ PEAS.png
   │  ├─ PERI.png
   │  ├─ PERS.png
   │  ├─ PVAI.png
   │  ├─ PVAS.png
   │  ├─ PVRI.png
   │  └─ PVRS.png
   └─ illustrations/
      └─ traffic-light.png
```

URL 경로는 `public`을 포함하지 않는다.

```text
파일: frontend/public/acorns/PEAI.png
URL:  /acorns/PEAI.png

파일: frontend/public/illustrations/traffic-light.png
URL:  /illustrations/traffic-light.png
```

## 21.2 실행 계약

React SPA 실행 명령:

```powershell
cd frontend
npm install
npm run dev
```

프런트엔드 기본 URL:

```text
http://localhost:3001/start
```

FastAPI 백엔드 실행 명령:

```powershell
cd backend
$env:PORT=8001
python app/main.py
```

API 기본 URL:

```text
http://localhost:8001/api/diagnosis
```

프런트엔드는 3001, 백엔드는 8001을 사용한다. FastAPI는 API와 SQLite
접근만 담당하며 React 정적 파일을 제공하지 않는다. 프런트엔드 API 기본값은
`http://localhost:8001/api/diagnosis`이고, 두 서버 간 요청은 CORS 허용
목록으로 연결한다.

아키텍처:

```text
Browser
  └─ React SPA · Vite (:3001)
       └─ HTTP API
            └─ FastAPI (:8001)
                 └─ SQLite (dotori.db)
```

`/start`, `/survey`, `/` 화면 전환은 React SPA의 브라우저 History API로
처리한다.

## 21.3 문서와 메타데이터

`frontend/index.html` MUST 조건:

```html
<html lang="ko">
  <body>
    <div id="root"></div>
  </body>
</html>
```

기본 메타데이터:

```yaml
title: 도토리 금융 DNA 결과
description: 나의 금융 DNA를 보여주는 모바일 결과 화면
```

`html` 또는 `body`에 기본 브라우저 여백이 남으면 안 된다.

## 21.4 전역 CSS 초기화

다음 선언은 의미상 동등한 형태로 반드시 존재해야 한다.

```css
* {
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  min-height: 100%;
  background: #fff7df;
  color: #173f32;
  font-family: "Noto Sans KR", sans-serif;
}

body {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  place-items: start center;
  min-width: 100%;
}

button,
a {
  color: inherit;
  font: inherit;
}
```

브라우저 기본 버튼 글꼴이나 링크 색상이 노출되면 실패다.

## 21.5 필수 디자인 토큰

아래 값은 MUST 정확히 일치해야 한다.

```css
:root {
  --ink: #173f32;
  --cream: #fff7df;
  --paper: #fffdf4;
  --sky: #9edaf1;
  --grass: #8fc77a;
  --green: #397c55;
  --pine: #245943;
  --brown: #7c4829;
  --tan: #d9a86c;
  --outline: 3px solid var(--ink);
  --screen-min-height: 1000px;
}
```

색상 대체 금지 예시:

```text
#173F32 → #164032 변경 금지
#FFF7DF → white 변경 금지
#9EDAF1 → 일반 blue 변경 금지
```

## 21.6 폰트 로딩 계약

MUST 불러와야 하는 Google Fonts:

```text
Black Han Sans
Noto Sans KR: 500, 600, 700, 800, 900
```

CSS:

```css
@import url("https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@500;600;700;800;900&display=swap");
```

용도:

```yaml
Black_Han_Sans:
  start_title: true
  survey_question: true
  result_type_heading: true
  body_text: false
Noto_Sans_KR:
  all_other_text: true
```

폰트 네트워크 로딩 실패 시 레이아웃 차이가 발생할 수 있으므로 시각 회귀 테스트 환경에서는 폰트를 먼저 로드한 뒤 캡처한다.

## 21.7 공통 모바일 셸의 정확한 박스 모델

```css
.mobile-screen,
.result-screen {
  width: 100%;
  max-width: 390px;
  min-height: var(--screen-min-height);
  padding-top: 18px;
  padding-right: 16px;
  padding-bottom: 24px;
  padding-left: 16px;
  background: #fff7df;
  position: relative;
}
```

계산:

```yaml
outer_width: 390px
horizontal_padding_total: 32px
content_width: 358px
```

반응형:

```css
```

390px 이상의 뷰포트에서 콘텐츠 자체를 비례 확대하면 안 된다.

## 21.8 공통 헤더의 정확한 구조

DOM:

```tsx
<header className="result-header">
  <a className="mini-brand" href="/start" aria-label="도토리 금융 DNA">
    <span className="brand-acorn" aria-hidden="true" />
    DOTORI DNA
  </a>
  <span className="result-step">{화면별 메타 문구}</span>
</header>
```

CSS:

```css
.result-header {
  height: 38px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  font-size: 10px;
  font-weight: 900;
  letter-spacing: 0.12em;
}

.mini-brand {
  display: flex;
  align-items: center;
  gap: 7px;
  text-decoration: none;
}

.brand-acorn {
  width: 18px;
  height: 18px;
  display: grid;
  place-items: center;
  border: 2px solid #173f32;
  border-radius: 50% 50% 46% 46%;
  color: #7c4829;
  font-size: 11px;
  line-height: 1;
  transform: rotate(-8deg);
}

.result-step {
  padding-top: 4px;
  color: #547365;
}
```

화면별 오른쪽 문구:

```yaml
start: "3 MIN · 7 QUESTIONS"
survey: "QUESTION {current_2digit} / {total_2digit}"
result: "RESULT 01"
```

## 21.9 `/start` 정확한 구현

### 21.9.1 상태

```ts
const [nickname, setNickname] = useState("");
const canStart = nickname.trim().length > 0;
```

입력 규칙:

```yaml
maximum_length: 12
trim_before_save: true
storage_key: dotori-nickname
submit_by_enter: true
empty_value_disables_cta: true
navigation_after_submit: /survey
```

### 21.9.2 DOM 순서

순서를 바꾸면 안 된다.

```text
main.mobile-screen.start-screen
├─ header.result-header
├─ section.start-hero
│  ├─ div.start-cloud.cloud-a
│  ├─ div.start-cloud.cloud-b
│  ├─ div.start-cloud.cloud-c
│  ├─ div.start-cloud.cloud-d
│  ├─ div.start-cloud.cloud-e
│  ├─ div.start-cloud.cloud-f
│  ├─ div.start-cloud.cloud-g
│  ├─ div.start-grass.grass-a … grass-g
│  ├─ span.start-sticker
│  ├─ div.start-title
│  │  ├─ p
│  │  ├─ h1
│  │  │  ├─ text "도토리"
│  │  │  ├─ br
│  │  │  └─ strong "금융 DNA"
│  │  └─ span "TEST"
│  ├─ img.start-character-image
│  ├─ div.start-transition-lens
│  └─ div.start-hill
├─ section.start-note
│  ├─ span "CHECK POINT"
│  ├─ div.signal-guide
│  │  ├─ img.signal-illustration
│  │  └─ div
│  │     ├─ strong
│  │     └─ p.checkpoint-copy
│  └─ div.nickname-field
│     ├─ input[aria-label="닉네임"]
│     └─ small
├─ button.start-cta
│  ├─ text
│  └─ span.cta-sub
├─ div.start-bottom-detail[aria-hidden="true"]
│  └─ span × 14
├─ div.start-bottom-flowers[aria-hidden="true"]
│  └─ span × 5
├─ img.start-squirrel[aria-hidden="true"]
└─ span.animation-status[aria-live="polite"]
```

### 21.9.3 정확한 문구

```yaml
sticker: "나의 돈 성향은?"
eyebrow: "자립을 준비하는 나를 위한"
title_line_1: "도토리"
title_line_2: "금융 DNA"
test_label: "TEST"
checkpoint_label: "CHECK POINT"
signal_title: "안정 · 주의 · 위험"
signal_copy: "단계에 맞춰 필요한 도움을 안내해 드려요."
nickname_placeholder: "닉네임을 입력해 주세요"
cta_main: "내 도토리 찾기"
cta_sub: "시작하기 ↗"
```

제목과 체크포인트 헤딩의 강제 줄바꿈은 반드시 유지한다.

### 21.9.4 시작 전체 배경과 히어로

```css
.start-screen {
  background: var(--sky);
  overflow: hidden;
  isolation: isolate;
}

.start-hero {
  height: 480px;
  background: transparent;
  position: relative;
  overflow: visible;
}
```

`1000px`은 결과 화면의 실측 높이 약 `999px`을 올림한 공통 캔버스
기준값이다. `/start`, `/survey`, `/`는 모두 이 최소 높이를 사용한다.
콘텐츠가 `1000px`을 초과하면 고정 높이로 자르지 않고 화면이 아래로
자연스럽게 늘어난다. 기준 뷰포트 `390×844px`은 반응형 검증 환경으로
유지하며, 캔버스의 세로 스크롤을 허용한다.

잔디 언덕:

```css
.start-screen::before {
  content: "";
  position: absolute;
  top: 414px;
  left: -96px;
  width: 582px;
  height: 180px;
  border-top: 3px solid #173f32;
  border-radius: 50% 50% 0 0;
  background: #8fc77a;
}

.start-screen::after {
  content: "";
  position: absolute;
  top: 505px;
  right: 0;
  bottom: 0;
  left: 0;
  background: #8fc77a;
}
```

#### 하늘 구름 픽셀 배치

모든 좌표는 `.start-hero`의 좌측 상단을 `(0, 0)`으로 삼는다. 구름 본체는
캡슐형이며 `::before`, `::after` 원형 도트로 봉우리를 만든다.

| 구름 | top | 가로 기준 | width | height | opacity |
|---|---:|---|---:|---:|---:|
| `cloud-a` | `18px` | `right: 36px` | `70px` | `28px` | 기본 |
| `cloud-b` | `72px` | `right: 12px` | `50px` | `20px` | `0.40` |
| `cloud-c` | `126px` | `right: 72px` | `44px` | `16px` | `0.30` |
| `cloud-d` | `184px` | `right: 20px` | `62px` | `21px` | `0.42` |
| `cloud-e` | `248px` | `left: 16px` | `38px` | `14px` | `0.26` |
| `cloud-f` | `286px` | `right: 106px` | `52px` | `18px` | `0.34` |
| `cloud-g` | `330px` | `left: 82px` | `30px` | `11px` | `0.24` |

#### 언덕 풀 도트 픽셀 배치

풀 군집의 기본 크기는 `7×17px`, 색상은 `#5F9F5B`이다. 각 군집은 중앙
캡슐형 잎과 `::before`, `::after`의 좌우 잎으로 구성한다.

| 풀 | top | 가로 기준 | 회전 |
|---|---:|---|---:|
| `grass-a` | `374px` | `left: 24px` | `-5deg` |
| `grass-b` | `396px` | `left: 78px` | `7deg` |
| `grass-c` | `423px` | `left: 130px` | `-3deg` |
| `grass-d` | `450px` | `left: 46px` | `4deg` |
| `grass-e` | `404px` | `right: 18px` | `-7deg` |
| `grass-f` | `448px` | `right: 88px` | `6deg` |
| `grass-g` | `435px` | `left: 178px` | `-5deg` |

### 21.9.5 시작 제목

```css
.start-title {
  position: absolute;
  z-index: 4;
  left: 18px;
  top: 77px;
}

.start-title p {
  margin: 0 0 6px;
  font-size: 11px;
  font-weight: 900;
}

.start-title h1 {
  margin: 0;
  font-family: "Black Han Sans", "Noto Sans KR", sans-serif;
  font-size: 55px;
  line-height: 0.9;
  font-weight: 400;
  letter-spacing: -0.05em;
  color: #fff7df;
  -webkit-text-stroke: 2px #173f32;
}

.start-title h1 strong {
  font: inherit;
  color: #d8efc8;
}
```

### 21.9.6 시작 캐릭터

```yaml
source: /acorns/PEAI.png
alt: 돋보기로 금융 생활을 살펴보는 탐구 도토리
```

```css
.start-character-image {
  position: absolute;
  z-index: 4;
  right: -10px;
  bottom: -3px;
  width: 225px;
  height: 225px;
  object-fit: contain;
  filter: drop-shadow(2px 4px 0 rgba(23, 63, 50, 0.15));
}
```

### 21.9.7 체크포인트 종이 카드

```css
.start-note {
  min-height: 0;
  margin: 19px 4px 0 0;
  padding: 20px 18px 16px;
  background: #fffdf4;
  border: 3px solid #173f32;
  border-radius: 12px 18px 12px 16px;
  box-shadow: 7px 8px 0 #6ea56a;
  position: relative;
}
```

### 21.9.8 신호등 카드

이모지 원형 나열을 사용하면 안 된다. 반드시 제공된 신호등 PNG를 사용한다.

```tsx
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
```

정확한 CSS:

```css
.signal-guide {
  min-height: 78px;
  margin: 0 0 13px;
  padding: 7px 12px 7px 8px;
  border: 2px solid #173f32;
  border-radius: 12px;
  background: #d8efc8;
  box-shadow: 3px 4px 0 #abc89c;
  display: grid;
  grid-template-columns: 58px 1fr;
  gap: 10px;
  align-items: center;
}

.signal-illustration {
  width: 56px;
  height: 68px;
  object-fit: contain;
  filter: drop-shadow(2px 2px 0 rgba(23, 63, 50, 0.12));
  transform: rotate(-2deg);
}

.signal-guide strong {
  display: block;
  margin-bottom: 3px;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: #173f32;
}

.checkpoint-copy {
  margin: 0;
  font-size: 12px;
  line-height: 1.45;
  font-weight: 700;
  color: #547365;
}
```

### 21.9.9 닉네임 필드

```css
.nickname-field {
  position: relative;
  padding-top: 10px;
  border-top: 2px dashed #b7c6b7;
}

.nickname-field input {
  width: 100%;
  height: 58px;
  padding: 0 48px 0 16px;
  border: 2px solid #173f32;
  border-radius: 29px;
  background: #d9a86c;
  color: #173f32;
  font-size: 15px;
  font-weight: 800;
  outline: none;
}

.nickname-field input::placeholder {
  color: #7c4829;
  opacity: 0.9;
}

.nickname-field input:focus {
  box-shadow: 0 0 0 4px rgba(124, 72, 41, 0.22);
}

.nickname-field small {
  position: absolute;
  right: 16px;
  bottom: 20px;
  font-size: 9px;
  font-weight: 900;
  color: #7c4829;
}
```

### 21.9.10 시작 버튼

```css
.start-cta {
  width: calc(100% - 4px);
  height: 92px;
  margin-top: 17px;
  padding: 13px 16px;
  border: 3px solid #173f32;
  border-radius: 10px;
  background: #faf2c0;
  color: #173f32;
  box-shadow: 6px 7px 0 #173f32;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 900;
  font-size: 20px;
  text-align: left;
  cursor: pointer;
}

.start-cta:disabled {
  cursor: not-allowed;
  opacity: 0.5;
  box-shadow: 3px 4px 0 #173f32;
}
```

### 21.9.10.1 시작 화면 하단 풀 디테일

결과 화면 기준 `1000px` 공통 캔버스 적용 후 시작 화면 하단에 생기는
여백에는 `.start-bottom-detail`을 배치한다. CTA와 겹치지 않도록 화면
하단에서 `7px`, 좌우에서 `14px` 떨어진 영역 안에 풀 군집 14개를 둔다.

```yaml
container_height: 62px
cluster_count: 14
base_color: "#5F9F5B"
opacity_range: 0.50..0.72
cluster_height_range: 13px..52px
pointer_events: none
aria_hidden: true
```

각 군집은 중앙 줄기와 `::before`, `::after`의 좌우 잎으로 구성한다.
크기·회전·불투명도를 서로 다르게 설정해 규칙적인 반복을 피한다. 장식은
버튼보다 아래에 머물러야 하며, 입력·CTA의 클릭 영역이나 텍스트 대비에
영향을 주면 안 된다.

풀숲 사이에는 `.start-bottom-flowers`로 작은 꽃 5개를 배치한다. 각 꽃은
3px 초록 줄기, 잎 한 장, 노란 꽃잎 5장과 갈색 중심으로 구성하며 CSS
`radial-gradient`로 그린다. 짝수 꽃은 채도와 밝기를 낮춰 크림빛 변주를
준다.

```yaml
flower_count: 5
container_height: 48px
stem_color: "#397C55"
leaf_color: "#5F9F5B"
petal_color: "#F6C84A"
center_color: "#7C4829"
render_order:
  grass: 1
  flowers: 2
  squirrel: 3
```

풀과 꽃은 화면 전체에 균일하게 반복하지 않고 좌우 높이와 회전을 다르게
한다. 오른쪽 꽃 일부가 다람쥐와 겹치는 경우에도 다람쥐의 `z-index: 3`이
가장 높아 얼굴, 몸통, 꼬리 윤곽이 가려지지 않아야 한다.

### 21.9.10.2 하단 다람쥐 장식과 탐색 동작

하단 풀숲 오른쪽에는 `start-squirrel`이라는 명칭의 작은 다람쥐 장식을
배치한다. 이 다람쥐는 도토리를 찾는 세계관을 보조하지만 CTA나 입력의 의미를
대체하지 않는 순수 장식 요소다.

```yaml
asset_name: start-squirrel
source: /illustrations/start-squirrel.png
file: frontend/public/illustrations/start-squirrel.png
format: RGBA PNG
pixel_size: 448x512
render_size: 82x82px
position:
  right: 31px
  bottom: 10px
stacking_order: 3
alt: ""
aria_hidden: true
pointer_events: none
```

에셋의 직접적인 스타일 기준은 `/acorns/PEAI.png`로 고정한다. 도토리와
동일하게 매끈한 디지털 그라데이션 채색, 광택 하이라이트, 두껍고 부드러운
다크 초콜릿 브라운 외곽선, 둥근 검갈색 눈동자와 흰색 이중 하이라이트를
사용한다. 수채화 번짐, 종이 질감, 연필선, 거친 잉크선은 사용하지 않는다.
몸통은 PEAI의 모자와 연결되는 밤색, 얼굴과 배는 PEAI 몸통과 연결되는
탄색·크림색으로 맞춘다. 배경을 제거한 투명 PNG만 런타임에서 사용하며
생성용 크로마키 원본은 저장소에 포함하지 않는다.

움직임 명칭은 `start-squirrel-curious`로 고정한다.

```css
animation:
  start-squirrel-curious
  5.6s
  cubic-bezier(0.42, 0, 0.24, 1)
  infinite;
transform-origin: 50% 100%;
```

동작은 바닥에 발을 붙인 상태에서 주변을 살피는 흐름으로 구성한다.

| 구간 | 움직임 |
|---:|---|
| `0–18%` | 정지 |
| `25–32%` | 왼쪽으로 `2–4px`, 위로 `3–5px` 이동하며 `-2deg…-3deg` 기울임 |
| `39–48%` | 제자리로 돌아오며 `scale(1.02, 0.98)`의 작은 착지 반동 |
| `58–68%` | 오른쪽으로 `1px`, 위로 `2px` 움직여 반대편을 살핀 뒤 정착 |
| `68–100%` | 휴지 구간 |

큰 점프나 빠른 무한 흔들림은 사용하지 않는다. 사용자가 CTA를 읽는 동안
시선을 과도하게 빼앗지 않도록 한 주기 중 절반 이상을 정지·감쇠 구간으로
유지한다. `prefers-reduced-motion: reduce`에서는 공통 모션 규칙에 따라
반복 동작을 중단한다.

### 21.9.11 도토리 시작 전환 애니메이션

애니메이션은 `StartPage` 내부의 고정 상태 머신으로 구현한다. 난수, 서버
응답 시간, 이미지 로딩 시간에 따라 타임라인을 바꾸지 않는다.

```ts
type AnimationPhase = "idle" | "centering" | "inspecting" | "zooming";

const CENTER_DURATION = 840;
const INSPECT_DURATION = 1080;
const ZOOM_DURATION = 880;
```

| 경과 시간 | 상태 | 화면 동작 | 이징 |
|---:|---|---|---|
| `0–840ms` | `centering` | 느낌표 알림 후 도토리가 가로 `-66px` 이동해 가운데로 접근 | `cubic-bezier(0.2, 0.72, 0.24, 1)` |
| `840–1920ms` | `inspecting` | 중심 위치에서 `-8px…1px` 상하 이동과 `-4.5deg…3deg` 회전으로 돋보기 탐색 표현 | `cubic-bezier(0.45, 0, 0.25, 1)` |
| `1920–2800ms` | `zooming` | 실제 렌즈 중심의 원형 마스크를 `24px`에서 `1120px`로 확대하고 기존 콘텐츠가 `300ms` 동안 사라짐 | `cubic-bezier(0.58, 0, 0.18, 1)` |
| `2800ms` | 이동 | History API로 `/survey` 이동 후 첫 질문 렌더링 | 해당 없음 |

도토리 애니메이션의 기준 변환은 다음과 같다.

```css
/* centering 종료 */
transform: translateX(-66px) translateY(0) rotate(0);

/* inspecting 중간 핵심 포즈 */
transform: translateX(-69px) translateY(-7px) rotate(-4deg);
transform: translateX(-63px) translateY(2px) rotate(3deg);
```

돋보기 확대 원 `.start-transition-lens`는 `.start-hero` 기준
`left: 80px`, `top: 328px`, `52×52px`, `4px` 잉크색 테두리로 배치한다.
이는 중앙으로 이동한 `PEAI.png`의 돋보기 렌즈 위치와 겹쳐야 한다. 확대
중 배경은 `--paper`, 내부 보조 테두리는 하늘색 `rgba(158, 218, 241,
0.7)`을 사용한다. 렌즈 안에는 별도 안내 문구를 표시하지 않으며, 확대가
완료된 다음 프레임에서 설문 첫 질문으로 전환한다.

실행 중 CTA는 다시 눌리지 않도록 비활성화하며 문구를
`도토리가 찾는 중 / 잠시만요`로 바꾼다. 닉네임은 애니메이션 시작 직전에
`sessionStorage["dotori-nickname"]`에 저장한다.

브라우저 콘솔 실행 로그 형식은 다음으로 고정한다.

```text
[DOTORI_START_ANIMATION] phase=centering elapsed_ms=0
[DOTORI_START_ANIMATION] phase=inspecting elapsed_ms=840
[DOTORI_START_ANIMATION] phase=zooming elapsed_ms=1920
[DOTORI_START_ANIMATION] phase=navigate-survey elapsed_ms=2800
```

실제 스케줄링 오차로 `elapsed_ms`는 수 밀리초 달라질 수 있지만 단계 순서와
목표 시간은 유지한다. 컴포넌트가 사라지면 등록된 모든 `setTimeout`을
정리한다. `prefers-reduced-motion: reduce`에서는 이동 효과를 실행하지 않고
`phase=reduced-motion-skip` 로그를 남긴 뒤 즉시 `/survey`로 이동한다.
화면 읽기 도구에는 `aria-busy`와 `aria-live` 상태 문구로 같은 단계를
전달한다.

### 21.9.12 시작 화면 도토리 자연스러운 동작 및 고해상도 돋보기 전환

2026-07-29부터 시작 화면의 도토리 동작은 단순한 직선 이동이 아니라
`idle → centering → inspecting → zooming`의 연속된 무게 중심 이동으로
표현한다. React 상태 이름은 유지하며 단계별 시간은 다음 값으로 고정한다.

```ts
const CENTER_DURATION = 840;
const INSPECT_DURATION = 1080;
const ZOOM_DURATION = 880;
```

| 경과 시간 | 상태 | 동작 명세 |
|---:|---|---|
| 대기 | `idle` | `3.4s ease-in-out infinite` 주기로 최대 `5px` 떠오르고 `-0.35deg`에서 `0.8deg`까지 기울어진다. |
| `0–185ms` | `centering` | 도토리는 정지한다. 머리 위 느낌표가 `10px` 아래에서 나타나 `8px` 위로 튀었다가 사라지는 `420ms` 알림 동작을 먼저 시작한다. |
| `185–840ms` | `centering` | 우측으로 `5px` 예비동작 후 좌측·위쪽 포물선으로 이동한다. 목표 위치 `translateX(-66px)`에 도착하기 전 `-70px`까지 넘긴 뒤 `-63px` 반동을 거쳐 정착한다. 이동 중 `scale(1.015, 0.985)` 범위의 미세한 눌림을 사용한다. |
| `840–1920ms` | `inspecting` | 두 번의 서로 다른 탐색 동작을 수행한다. 위치 범위는 `translateX(-70px..-61px)`, `translateY(-8px..1px)`, 회전 범위는 `-4.5deg..3deg`이다. 마지막 `10%` 구간에서 작은 반동을 감쇠해 기준 위치로 돌아온다. |
| `1920–2800ms` | `zooming` | 도토리는 렌즈를 따라 `-3px..2px` 범위에서 미세 이동한 뒤 `opacity: 0`으로 사라지고, 원형 전환 면이 화면을 덮는다. |
| `2800ms` | 이동 | `/survey`로 이동한다. |

단계가 바뀔 때 이전 단계의 CSS 애니메이션을 중복 적용하지 않는다.
`animation-centering`, `animation-inspecting`, `animation-zooming` 각각이
`.start-character-image`의 `animation` 전체 값을 교체한다. 따라서
`transform` 애니메이션 간 충돌 없이 직전 단계의 종료 위치와 다음 단계의
시작 위치가 동일하게 유지된다.

돋보기 확대에는 작은 DOM 요소의 `transform: scale(...)`을 사용하지 않는다.
작은 `52×52px` 합성 레이어를 19배 확대하면 브라우저가 저해상도 래스터
표면을 재사용해 확대 초반에 계단 현상과 픽셀 깨짐이 보일 수 있기 때문이다.
확대 단계에서는 `.start-transition-lens`를
`390px × max(var(--screen-min-height), 100vh)`의
전환 면으로 즉시 전환하고 다음 원형 마스크를 애니메이션한다.

```css
/* 화면 좌상단 기준 PEAI 이미지의 실제 렌즈 중심: x=118px, y=412px */
clip-path: circle(24px at 118px 412px);   /* 0~24%, 돋보기 형태 유지 */
clip-path: circle(31px at 118px 412px);   /* 34%, 확대 시작 */
clip-path: circle(180px at 118px 412px);  /* 52% */
clip-path: circle(1120px at 118px 412px); /* 100% */
```

전환 면은 처음부터 최종 해상도로 그려지고 `clip-path`의 반경만 바뀌므로
확대 전 구간에서 배경과 테두리가 현재 DPR에 맞춰 다시 래스터화된다.
렌즈 중심은 기존 PEAI 이미지의 돋보기 위치와 같은 화면 좌표
`(118px, 412px)`를 유지한다. `inspecting` 단계에서는 별도 전환 원을
표시하지 않고 PEAI 원본 이미지에 그려진 돋보기만 사용한다. 따라서 캐릭터가
흔들릴 때 렌즈와 별도 원의 위치가 어긋나는 현상이 없다.

`zooming` 시작 후 첫 `24%` 동안은 `48×48px` 돋보기 테두리와 `24px`
마스크 반경을 그대로 유지한다. `24%` 이후에만 마스크를 확장하며 테두리는
`48%`까지 `scale(1.24)`와 함께 자연스럽게 사라진다. 확대 중 레이아웃
콘텐츠보다 항상 위에 표시되도록 `.animation-zooming .start-hero`와 전환
면의 `z-index`를 `30`으로 설정한다. 렌즈 내부 안내 문구는 렌더링하지 않는다.

느낌표는 `.start-alert-mark`로 구현한다. `centering` 시작과 동시에
`840ms cubic-bezier(0.18, 0.9, 0.24, 1.2)` 등장 애니메이션을 실행하고,
도토리 본체는 첫 `22%` 동안 정지해 알림이 이동보다 먼저 인지되도록 한다.
느낌표는 `centering` 종료 상태에서 사라지지 않고 `inspecting`으로
이어진다. `inspecting`의 첫 `72%`까지 `translateY(-8px)` 위치를 유지하고,
`72~82%`에서 한 번 작게 반동한 뒤 마지막 `18%` 동안 위로 `9px` 이동하면서
`scale(0.55)`, `opacity: 0`으로 사라진다. 따라서 돋보기 확대가 시작되는
`1920ms` 이전에 소멸이 완료된다.

### 21.9.13 시작 도토리 동작 효과음

시작 버튼을 누르면 도토리 애니메이션과 함께 두 번의 짧은
`띠용 → 띠용` 효과음을 재생한다.

```yaml
asset: /sounds/start-dotori-boing.wav
source_file: frontend/public/sounds/start-dotori-boing.wav
generator: frontend/scripts/generate_start_motion_sound.mjs
duration: 1.82s
sample_rate: 44100Hz
channels: mono
encoding: PCM 16-bit WAV
playback_trigger: 사용자가 활성화된 시작 버튼을 클릭하거나 Enter로 실행
loop: false
preload: auto
```

첫 소리는 `0.06s`에 시작해 `690Hz → 260Hz`로 내려가고, 두 번째 소리는
`0.84s`에 시작해 `610Hz → 205Hz`로 내려간다. 각 음에는 기본음과 약한
2배음, 감쇠 곡선을 합성해 가볍고 둥근 애니메이션 효과를 만든다.

`StartPage`는 `<audio preload="auto">` 요소를 `useRef`로 관리한다. 시작
버튼의 사용자 제스처 안에서 `currentTime = 0`으로 초기화한 뒤 `play()`를
호출한다. 브라우저 정책으로 재생이 거부되어도 화면 진행을 막지 않고
`[DOTORI_START_AUDIO] playback=blocked` 로그만 남긴다. 컴포넌트가
언마운트되면 재생을 중지한다.

`prefers-reduced-motion: reduce`에서는 도토리 애니메이션을 건너뛰므로
효과음도 재생하지 않는다.

협업자는 저장된 WAV 파일을 그대로 사용한다. 음원을 다시 생성해야 할 때만
다음 명령을 실행한다.

```bash
cd frontend
npm run generate:start-sound
```

생성 스크립트는 외부 패키지나 네트워크 없이 동일한 WAV 파일을
`frontend/public/sounds/start-dotori-boing.wav`에 덮어쓴다. Git에는 WAV와
생성 스크립트를 모두 포함한다.

`prefers-reduced-motion: reduce`에서는 위 동작을 모두 생략하고 기존과 같이
즉시 `/survey`로 이동한다.

## 21.10 `/survey` 정확한 구현

### 21.10.1 데이터 및 진행

```yaml
loading_initial: true
answer_array_initial_value: -1
answer_value_range: 0..3
api_choice_index_range: 0..3
current_question_index: zero_based
display_question_number: one_based
auto_advance: true
previous_button_on_first_question: disabled
submit_on_last_answer: true
result_storage_key: dotori-result
result_route: /
```

화면과 백엔드 `AnswerItem.choice_index`, 진단 계산기는 모두 0부터 시작하는
배열 인덱스 `0..3`을 사용한다. 미응답 상태만 `-1`로 구분한다.

```ts
const value = optionIndex; // 0..3
choice_index: finalAnswers[i]
```

UI를 `1..4`, API를 `0..3`으로 이중 관리하면 변환 누락 시 네 번째 선택지
값 `4`가 전송되어 `Value error, choice_index는 0~3 사이의 값이어야
합니다.`가 발생한다. 따라서 별도 `-1` 미응답 sentinel과 0 기반 선택값을
사용하며 제출 전 모든 값이 정수 `0..3`인지 검사한다. 유효하지 않은 값이
하나라도 있으면 API를 호출하지 않는다.

진행률 공식:

```ts
Math.round(((current + 1) / total) * 100)
```

### 21.10.2 정확한 상태 문구

```yaml
loading: "질문을 불러오는 중이에요…"
load_error: "질문을 불러오지 못했습니다. 백엔드 서버를 확인해 주세요."
creating_result: "결과를 만드는 중이에요…"
submit_error: "결과를 계산하지 못했습니다. 잠시 후 다시 시도해 주세요."
auto_advance_default: "답을 고르면 다음 질문으로 바로 넘어가요."
auto_advance_last: "답을 고르면 바로 결과를 보여드려요."
previous: "← 이전 질문"
```

### 21.10.3 질문 카드

```css
.question-card {
  height: 258px;
  padding: 54px 18px 18px;
  border: 3px solid #173f32;
  border-radius: 17px 11px 19px 13px;
  background: #9edaf1;
  box-shadow: 7px 8px 0 #245943;
  position: relative;
  overflow: hidden;
}
```

질문 제목:

```css
.question-card h1 {
  margin: 0;
  font-family: "Black Han Sans", "Noto Sans KR", sans-serif;
  font-size: 27px;
  line-height: 1.25;
  font-weight: 400;
  letter-spacing: -0.045em;
  word-break: keep-all;
  overflow-wrap: normal;
}
```

질문 제목에만 위 줄바꿈 규칙을 적용하여 한글 단어 내부가 아닌 띄어쓰기
위치에서 줄을 바꾼다. 답변 선택지의 줄바꿈 규칙은 변경하지 않는다.

하늘은 `#9EDAF1`, 언덕은 `#8FC77A`를 유지한다. 하늘과 언덕을 별도
사각형으로 나누지 않고 시작 화면 전체 캔버스에서 곡선 경계로 연결한다.
헤더 주변과 좌우 화면 끝에는 하늘색이, 도토리 아래와 체크포인트 카드의
바깥 여백에는 초록색이 보여야 한다.
하늘에는 흰색 불투명도 `0.24–0.55`의 둥근 구름 군집 7개를 배치하며
제목, 질문 스티커, 도토리와 겹치지 않게 한다. 언덕에는 `#5F9F5B`
도트형 풀 군집 7개를 배치한다.

질문 카드에는 `가장 나와 가까운 답 하나를 골라주세요.` 문구를 렌더링하지
않는다.

### 21.10.4 답변 선택지

DOM:

```tsx
<button
  className={`answer-option ${selected ? "selected" : ""}`}
  type="button"
>
  <span>{알파벳 인덱스}</span>
  <strong>{답변 문구}</strong>
  <i>{selected ? "✓" : ""}</i>
</button>
```

그리드:

```yaml
columns: 34px 1fr 23px
gap: 9px
minimum_height: 72px
list_gap: 9px
```

선택 상태 MUST:

- 배경 `#D8EFC8`
- 그림자 `5px 6px 0 #245943`
- 전체 버튼 `translateX(2px)`
- 왼쪽 인덱스 원 배경 `#245943`
- 오른쪽 체크 원 배경 `#245943`
- 선택 체크 `✓`

### 21.10.5 자동 진행 규칙

1. 선택한 값을 현재 인덱스에 저장한다.
2. 마지막 질문이 아니면 즉시 `current + 1`로 이동한다.
3. 마지막 질문이면 전체 답변 배열을 API에 제출한다.
4. 성공하면 결과를 `sessionStorage["dotori-result"]`에 JSON 문자열로 저장한다.
5. `/`로 `replace` 이동한다.
6. 제출 중 추가 클릭을 무시한다.

## 21.11 `/` 결과 화면 정확한 구현

### 21.11.1 결과 데이터 우선순위

1. `sessionStorage["dotori-result"]`가 유효하면 해당 값을 사용한다.
2. 저장값이 없거나 JSON 파싱에 실패하면 기본 `PEAI` 결과를 사용한다.
3. 파싱 실패 시 잘못된 저장값을 제거한다.
4. 닉네임은 `sessionStorage["dotori-nickname"]`에서 읽는다.

기본 결과:

```yaml
mbti_code: PEAI
type_name: 새싹을 꿈꾸는 탐구 도토리
summary: 계획을 세워 차곡차곡 모으고, 더 큰 가능성은 꼼꼼히 탐색하는 타입이에요.
risk_color: GREEN
```

### 21.11.2 결과 히어로

```css
.hero-card {
  height: 374px;
  border: 3px solid #173f32;
  border-radius: 18px 12px 20px 14px;
  background: #9edaf1;
  box-shadow: 8px 9px 0 #245943;
  position: relative;
  overflow: hidden;
}
```

캐릭터:

```css
.result-character {
  position: absolute;
  z-index: 4;
  right: 4px;
  bottom: 3px;
  width: 235px;
  height: 235px;
  object-fit: contain;
  object-position: center bottom;
  filter: drop-shadow(2px 3px 0 rgba(23, 63, 50, 0.18));
}
```

### 21.11.3 유형 코드와 파일 매핑

아래 매핑은 MUST 정확히 유지한다.

| 코드 | 화면 유형명 | 캐릭터 파일 |
|---|---|---|
| PEAS | 금고 속 튼튼 도토리 | `/acorns/PEAS.png` |
| PEAI | 새싹을 꿈꾸는 탐구 도토리 | `/acorns/PEAI.png` |
| PERS | 선배 둥지 따뜻 도토리 | `/acorns/PERS.png` |
| PERI | 가이드 탑승 모험 도토리 | `/acorns/PERI.png` |
| PVRS | 포근한 모자 도토리 | `/acorns/PVRS.png` |
| PVRI | 꿈나무 열매 도토리 | `/acorns/PVRI.png` |
| PVAS | 반짝이는 왕관 도토리 | `/acorns/PVAS.png` |
| PVAI | 트랜디한 힙스터 도토리 | `/acorns/PVAI.png` |
| FEAS | 굴러가는 실속 도토리 | `/acorns/FEAS.png` |
| FEAI | 번개 탄 스피드 도토리 | `/acorns/FEAI.png` |
| FERS | 둥글둥글 순한 도토리 | `/acorns/FERS.png` |
| FERI | 호기심 퐁퐁 도토리 | `/acorns/FERI.png` |
| FVRS | 솜이불 덮은 도토리 | `/acorns/FVRS.png` |
| FVRI | 풍선 탄 낭만 도토리 | `/acorns/FVRI.png` |
| FVAS | 달콤한 디저트 도토리 | `/acorns/FVAS.png` |
| FVAI | 마이웨이 욜로 도토리 | `/acorns/FVAI.png` |

### 21.11.4 결과 도토리 더블 점프 애니메이션

결과 화면의 16개 캐릭터는 모두 `.result-character` 한 클래스를 사용한다.
결과 화면 마운트 시 즉시 애니메이션을 시작하며, `5초` 주기 안에서 두 번
점프하고 정확히 `2회` 주기만 실행한다. 따라서 총 실행 시간은 `10초`,
실제 점프 횟수는 `4회`이다. 무한 반복은 금지한다.

```css
.result-character {
  transform-origin: center bottom;
  will-change: transform;
  animation: result-double-jump 5s ease-in-out 2 both;
}
```

한 주기의 키프레임과 `5초` 기준 절대 시간은 다음과 같다.

| 비율 | 주기 내 시간 | Y 이동 | 회전 | 스케일 | 의미 |
|---:|---:|---:|---:|---|---|
| `0%` | `0ms` | `0` | `0` | `1` | 바닥 대기 |
| `4%` | `200ms` | `2px` | `0` | `1.03, 0.97` | 첫 점프 준비 압축 |
| `10%` | `500ms` | `-18px` | `-1.5deg` | `0.99, 1.01` | 첫 점프 최고점 |
| `16%` | `800ms` | `0` | `0` | `1.04, 0.96` | 첫 착지 |
| `20%` | `1000ms` | `1px` | `0` | `1.025, 0.975` | 두 번째 점프 준비 |
| `26%` | `1300ms` | `-14px` | `1.2deg` | `0.995, 1.005` | 두 번째 점프 최고점 |
| `32%` | `1600ms` | `0` | `0` | `1.03, 0.97` | 두 번째 착지 |
| `34%` | `1700ms` | `-3px` | `-0.4deg` | `1` | 착지 반동 |
| `36%` | `1800ms` | `0` | `0` | `1` | 안정 |
| `100%` | `5000ms` | `0` | `0` | `1` | 다음 주기까지 정지 |

전체 결과 화면 진입 시점 기준 점프 최고점은 `500ms`, `1300ms`,
`5500ms`, `6300ms`이다. 두 번째 주기가 끝나는 `10000ms`에는 원래
위치와 크기로 정지한다. `transform`만 사용하므로 주변 텍스트나 카드의
레이아웃 위치를 변경하면 안 된다. `transform-origin: center bottom`으로
발이 언덕에 닿은 느낌을 유지한다.

결과 데이터는 `useEffect`에서 세션 값으로 교체될 수 있으므로 이미지에
`key={code}`를 둔다. 실제 코드가 확정되어 PNG가 바뀌면 해당 이미지가
다시 마운트되며 그 시점부터 온전한 `10초` 애니메이션을 시작한다.

```tsx
<img
  key={code}
  className="result-character"
  data-character-code={code}
  src={`/acorns/${code}.png`}
  alt={typeName}
/>
```

`PEAS`, `PEAI`, `PERS`, `PERI`, `PVRS`, `PVRI`, `PVAS`, `PVAI`,
`FEAS`, `FEAI`, `FERS`, `FERI`, `FVRS`, `FVRI`, `FVAS`, `FVAI`
모두 위 클래스와 키프레임을 공유해야 한다. 유형별 별도 애니메이션이나
좌표 예외를 만들지 않는다.

실행 로그 형식:

```text
[DOTORI_RESULT_ANIMATION] code=FVRI cycle=1 phase=start
[DOTORI_RESULT_ANIMATION] code=FVRI cycle=2 phase=start
[DOTORI_RESULT_ANIMATION] code=FVRI cycles=2 phase=complete elapsed_ms=10000
```

`animationstart`, 첫 `animationiteration`, `animationend` 이벤트에 각각
로그를 남긴다. `prefers-reduced-motion: reduce`에서는 공통 모션 규칙에
따라 지속시간을 `0.01ms`, 반복 횟수를 `1회`로 축소한다.

교차 검증 조건:

1. `TYPE_NAMES` 키가 정확히 16개이며 중복이 없어야 한다.
2. 각 키에 대응하는 `/public/acorns/{code}.png`가 존재해야 한다.
3. 16개 파일 모두 PNG이고 `1254×1254`, RGBA여야 한다.
4. 결과 이미지 16종 모두 `result-character` 클래스와 `key={code}`를
   사용해야 한다.
5. CSS 선언은 `5s`, 반복 횟수 `2`, `infinite` 미사용이어야 한다.
6. 두 주기가 끝난 뒤 최종 변환은 `translateY(0) rotate(0) scale(1)`이어야
   한다.

### 21.11.5 추천 영역

고정 추천 데이터:

```yaml
- category: 정부지원
  title: 청년 자산형성 지원
  description: 자립준비청년이 활용할 수 있는 정부지원금과 자산형성 제도를 확인해 보세요.
- category: 은행권
  title: 청년 우대 금융상품
  description: 우대금리 적금과 수수료 혜택 등 은행권의 청년 맞춤 상품을 비교해 보세요.
```

핵심 키워드:

```text
#자립적립
#성장투자
#목표저축
```

2열 그리드:

```css
grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
gap: 10px;
```

### 21.11.6 위험 신호

정확한 매핑:

| API 값 | 단계명 | 카드 클래스 | 배경 | 현재 표시 |
|---|---|---|---|---|
| `GREEN` | 안정 신호 | `risk-green` | `#D7EBC6` | 신호등 일러스트 |
| `YELLOW` | 주의 신호 | `risk-yellow` | `#FFF0B8` | 신호등 일러스트 |
| `RED` | 위험 신호 | `risk-red` | `#F6C5B8` | 신호등 일러스트 |

결과 카드에서는 원형 색상 이모지를 사용하지 않는다. 모든 단계에
`/illustrations/traffic-light.png`를 표시하고 `안정 신호`, `주의 신호`,
`위험 신호` 텍스트를 함께 제공한다.

결과 유형 제목 `.hero-type-name`은 짙은 외곽선을 유지하되 `text-shadow`를
적용하지 않는다.

유형명 끝의 `도토리`는 단어 중간에서 줄바꿈하면 안 된다. 유형명 본문과
`도토리`를 각각 블록 요소로 렌더링해 다음 형태를 보장한다.

```text
풍선 탄 낭만
도토리
```

```tsx
<h1 className="hero-type-name">
  <span>{typeNameWithoutSuffix}</span>
  <span className="hero-type-suffix">도토리</span>
</h1>
```

`.hero-type-name`은 `word-break: keep-all`을 사용하고
`.hero-type-suffix`는 `white-space: nowrap`을 사용한다.

DNA 리포트 `.summary-card`의 배경은 `#D7FAF7`을 유지한다. 정부지원과
은행권 추천 영역에는 사각형 카드 배경과 카드 테두리를 사용하지 않는다.
API의 `summary` 값에 포함될 수 있는 `[여유로운 감성파] 풍선 탄 낭만
도토리 — 고위험 등급` 같은 조합 문구는 DNA 리포트에 렌더링하지 않는다.
해시태그 칩은 `13px/900`, 상하 `7px`·좌우 `15px` 여백과 `9px` 간격을
사용하고 행 전체를 중앙 정렬한다.

추천 항목 DOM은 다음 순서를 따른다.

```tsx
<div className="rec-item">
  <div className="rec-panel">
    <p className="rec-desc">
      <strong>청년 자산형성 지원</strong>
      부가 설명
    </p>
  </div>
</div>
```

`.rec-item`에는 별도의 `.rec-category` 요소를 렌더링하지 않는다.
`정부지원`, `은행권` 문구가 차지하던 라벨 높이와 하단 여백을 제거하고,
`.rec-panel`은 `margin-top: 0`으로 그리드 상단부터 바로 시작한다.

`.rec-panel`은 `12px` 둥근 모서리를 가진 사각형으로 만든다. 배경은
베이지 `#F2DFC0`, 윤곽은 `2px` 잉크색 선을 사용하며 추천 제목과 설명만
포함한다. 추천 제목은 설명 문단 안의 `<strong>` 요소로 표시한다.
추천 제목과 설명 모두 `word-break: keep-all`, `overflow-wrap: normal`을
사용하여 한글 음절 중간이 아니라 띄어쓰기 위치에서만 줄을 바꾼다.
두 `.rec-item`은 같은 그리드 행 높이를 모두 사용하고 `.rec-panel`에
`flex: 1 1 auto`를 적용하여 내용 길이가 달라도 양쪽 사각형의 너비와
높이가 동일해야 한다.

위험 카드의 `RISK SIGNAL` 라벨과 `안정 신호`·`주의 신호`·`위험 신호`는
같은 상단 행에 나란히 배치한다. 신호등 일러스트는 단계명 앞에 둔다.
추가 설명 영역은 사각형 카드의 가로 중앙에 정렬하며 제목은 `14px/900`,
행동 안내는 `12px/800`, 행간 `1.6`을 사용한다.

결과 부주제 `.risk-concern`은 현재 위험 단계의 신호등 색을 사용한다.

```css
.risk-green .risk-concern  { color: #62A86D; }
.risk-yellow .risk-concern { color: #EFBD3E; }
.risk-red .risk-concern    { color: #DF6A55; }
```

## 21.12 에셋 무결성 명세

모든 PNG 원본 크기는 `1254 × 1254px`이다. 구현자는 이미지 파일을 임의로 재압축하거나 교체하지 않아야 한다.

| 파일 | 바이트 | SHA-256 |
|---|---:|---|
| `acorns/FEAI.png` | 957905 | `4e85f6f584104a0c0ed008a6c8828f1840ddd561d4760e730bdf99f3c184eccb` |
| `acorns/FEAS.png` | 1133410 | `e3e951fa5aaedac9831e4e745a5f197136fb210df0bc9a9ac7b99f56551bffc2` |
| `acorns/FERI.png` | 1005025 | `52fb4c90dca715019752384a618e3dbe3e16844ef11ab4cdf7cbeafcb38de5ff` |
| `acorns/FERS.png` | 1011628 | `5cc737ad226a73209a34445ac96bd7f76ff953ccc08ee0a20f75f3f40caaefdf` |
| `acorns/FVAI.png` | 1117186 | `9e15f33d4f02b12213e79ccba16fe5c4506532acd814eac425c6abeb2520d855` |
| `acorns/FVAS.png` | 1094413 | `485b6253299ed66507b9bb3cf2a7daf7a759c565ede0c83e728b38341cde0887` |
| `acorns/FVRI.png` | 813757 | `ddaf9c47f688b7ca9efd6bfe230d83ac9e16db94c07b23a75512b408e8e236b6` |
| `acorns/FVRS.png` | 1154993 | `0a9bcd61fc191a73619eb10f1e1f971463af4ea2da6f48c8c61b56afac9cde95` |
| `acorns/PEAI.png` | 990040 | `7b3f3faca10b0ba1cc68cbe8f82404b2e96344ee7a2c1d93c6c3485240fc0b6d` |
| `acorns/PEAS.png` | 1223399 | `b5c63b58699fc80ac3129de52540ee6c5d83b4d5f57ad6b6cf858c433767aba9` |
| `acorns/PERI.png` | 1221351 | `9f0d52bce84aa1641a6c5dd70ee4a03b5401d511ca4e568254fa4deab2d78858` |
| `acorns/PERS.png` | 1041245 | `ecf58d8d2e6d3b84fe4039dc982826975bfa9e479d359add6c6523b1c7c826da` |
| `acorns/PVAI.png` | 1261820 | `da8669ef44ea115709da949cc873479e2b24b2260e380d8bdb541f177dfe88d7` |
| `acorns/PVAS.png` | 1541005 | `595e7a7f582bf0bba4a7253b37dea24352a65c0249e42fdfdd817f6068f4a684` |
| `acorns/PVRI.png` | 1144849 | `9b89916b72814328d8f06b50b2047f512c34af1107fd39367edf7c1715eea523` |
| `acorns/PVRS.png` | 1136657 | `db8e290ee4d80eb8db4582c1b5d2526f81baa148af5eaa71c91cba154b777b98` |
| `illustrations/traffic-light.png` | 917561 | `c1f8d639c11253096f3b839ce438dbe959631d7709c81444cca8f25cedd5ad23` |

SHA가 다르면 동일 에셋으로 간주하지 않는다.

## 21.13 접근성 구현 계약

MUST:

- `<html lang="ko">`
- 의미 있는 이미지에 정확한 `alt`
- 장식 요소에 `aria-hidden="true"` 또는 의미 없는 요소로 처리
- 모든 클릭 행동은 `button` 또는 `a` 사용
- 버튼은 `type="button"` 명시
- 입력과 `label[for]` 연결
- 선택지 묶음에 `aria-label="응답 선택지"`
- 추천 묶음에 `aria-label="맞춤 금융 추천"`
- 비활성 상태는 실제 `disabled` 속성 사용
- 키보드 Enter로 닉네임 제출 가능

MUST NOT:

- 클릭 가능한 `div`
- 이미지 안에만 존재하는 핵심 문구
- 색상만으로 전달되는 선택 상태
- `outline: none`만 적용하고 대체 포커스 표시를 누락

## 21.14 시각 회귀 테스트 기준

### 기준 뷰포트

```yaml
width: 390
height: 844
device_scale_factor: 1
font_ready: required
browser_zoom: 100%
```

### 캡처 대상

1. `/start` 빈 닉네임
2. `/start` 닉네임 12자 입력
3. `/survey` 첫 질문 무선택
4. `/survey` 선택 직후
5. `/survey` 마지막 질문
6. `/` GREEN 결과
7. `/` YELLOW 결과
8. `/` RED 결과

### 허용 오차

```yaml
geometry:
  primary_cards: 0px
  text_wrap: 0_lines
  illustration_box: 0px
  antialiasing_only: allowed
pixel_diff_recommendation: <= 1.0%
```

폰트 안티앨리어싱 차이는 허용하지만 카드 크기, 줄바꿈, 이미지 위치 차이는 허용하지 않는다.

## 21.15 기능 인수 테스트

### 시작 화면

```gherkin
Given 사용자가 /start에 접속했을 때
Then 시작 버튼은 disabled여야 한다
And 신호등 이미지는 /illustrations/traffic-light.png여야 한다
And "안정 · 주의 · 위험" 문구가 보여야 한다

When 닉네임에 공백만 입력했을 때
Then 시작 버튼은 disabled여야 한다

When 유효한 닉네임을 입력하고 시작 버튼을 눌렀을 때
Then trim된 닉네임이 sessionStorage["dotori-nickname"]에 저장되어야 한다
And /survey로 이동해야 한다

When 13자 이상 입력을 시도했을 때
Then 실제 입력값은 12자여야 한다
And 글자 수 표시는 12/12여야 한다
```

### 설문 화면

```gherkin
Given 질문 데이터가 로드됐을 때
Then 현재 질문과 진행률이 표시되어야 한다

When 답변을 선택했을 때
Then 해당 선택지는 selected 클래스를 가져야 한다
And 체크 표시가 보여야 한다
And 마지막 질문이 아니라면 다음 질문으로 이동해야 한다

When 첫 질문일 때
Then 이전 질문 버튼은 disabled여야 한다

When 마지막 답변 제출이 성공했을 때
Then 결과 JSON이 sessionStorage["dotori-result"]에 저장되어야 한다
And /로 이동해야 한다
```

### 결과 화면

```gherkin
Given 저장된 결과가 없을 때
Then PEAI 기본 결과를 보여야 한다

Given 저장된 mbti_code가 PVAS일 때
Then /acorns/PVAS.png를 보여야 한다
And alt는 "반짝이는 왕관 도토리"여야 한다

Given risk_color가 YELLOW일 때
Then 위험 카드에 risk-yellow 클래스가 있어야 한다
And 단계명은 "주의 신호"여야 한다
```

## 21.16 구현 완료 체크리스트

개발자는 PR을 올리기 전에 모두 확인해야 한다.

### 저장소

- [ ] `frontend/public/acorns`에 16개 PNG가 모두 있다.
- [ ] `frontend/public/illustrations/traffic-light.png`가 있다.
- [ ] 에셋 SHA-256이 21.12와 일치한다.
- [ ] `design.md`가 저장소 루트에 있다.

### 화면

- [ ] `/start`, `/survey`, `/`가 모두 렌더링된다.
- [ ] 기준 뷰포트에서 가로 스크롤이 없다.
- [ ] 시작 히어로가 `480px`이다.
- [ ] 질문 카드가 `258px`이다.
- [ ] 결과 히어로가 `374px`이다.
- [ ] 신호등이 이모지가 아닌 PNG 일러스트다.
- [ ] 모든 외곽선과 그림자가 명세와 일치한다.

### 동작

- [ ] 닉네임 저장과 12자 제한이 작동한다.
- [ ] 답변 선택 후 자동 진행한다.
- [ ] 마지막 질문에서 API를 호출한다.
- [ ] 결과를 세션 저장소에서 복구한다.
- [ ] 잘못된 결과 JSON을 안전하게 제거한다.

### 접근성

- [ ] 모든 이미지 대체 텍스트를 확인했다.
- [ ] Tab 키로 모든 인터랙션에 접근 가능하다.
- [ ] 포커스 표시가 보인다.
- [ ] 실제 `disabled` 속성을 사용한다.
- [ ] 색상 없이도 상태명과 선택 여부를 알 수 있다.

### 검증 명령

```powershell
cd frontend
npm run build
```

빌드 오류와 TypeScript 오류가 없어야 한다.

## 21.17 구현자에게 전달할 단일 지시문

GitHub 이슈, PR 설명 또는 코딩 에이전트 프롬프트에는 아래 문장을 그대로 사용할 수 있다.

```text
저장소 루트의 design.md를 구현 계약서로 사용하세요.
특히 0장과 21장은 필수 명세이며, 명시된 치수·색상·문구·DOM 순서·에셋 경로를 임의로 변경하지 마세요.
frontend/public의 PNG를 그대로 사용하고 대체 이미지나 이모지로 바꾸지 마세요.
390×844 CSS 픽셀을 기준으로 /start, /survey, / 화면을 구현하고,
21.15의 기능 인수 테스트와 21.16의 완료 체크리스트를 모두 통과시키세요.
문서와 구현이 충돌하면 21장, 실제 에셋, 화면별 명세 순으로 우선합니다.
```

---

## 22. 투명 배경(누끼) 이미지 계약

이 절은 이 프로젝트에서 이후 생성하거나 편집하는 모든 래스터 이미지에
적용한다. 이 절의 투명 배경과 검증 규칙은 21.12의 기존 파일 바이트 및
SHA-256 명세보다 우선한다.

### 22.1 생성 및 편집 원칙

- GPT로 생성한 캐릭터·사물 일러스트는 배경이 없는 RGBA PNG여야 한다.
- 캐릭터와 소품의 기존 진한 외곽선, 내부 색, 표정, 비율은 그대로 보존한다.
- 흰 캔버스, 회색 체크무늬, 흰 외곽 프린지, 흰 후광을 최종 파일에 남기면 안 된다.
- 모든 흰색을 일괄 삭제하면 안 된다. 외곽선 안쪽의 눈동자 하이라이트,
  치아, 휴대폰 화면, 지도, 크림, 담요 등 의도된 흰색은 보존한다.
- 풍선 사이, 풍선 줄 사이, 체인 고리 사이, 팔과 소품 사이처럼 외부
  배경과 이어지는 내부 틈도 투명해야 한다.
- 신호등은 몸체와 램프만 남기고 바깥 체크무늬와 흰 테두리를 모두
  제거한다. 램프 내부의 의도된 흰 하이라이트는 보존한다.

### 22.2 적용 범위

- `frontend/public/acorns/*.png`의 16개 유형 전체
- `frontend/public/illustrations/traffic-light.png`
- 이후 이 프로젝트에 추가되는 GPT 생성 래스터 캐릭터와 소품

일부 유형만 처리한 상태로 병합하면 안 된다. 16개 유형은 항상 동일한 누끼
규칙과 검증 기준을 적용한다.

### 22.3 `ex.po` 별도 보관

```text
frontend/public/ex.po/
├─ originals/
│  ├─ acorns/
│  └─ illustrations/
└─ cutouts/
   ├─ acorns/
   └─ illustrations/
```

- `originals`에는 배경 제거 전 원본을 보존한다.
- `cutouts`에는 앱에서 사용하는 누끼 결과와 동일한 파일을 보존한다.
- 앱의 기존 URL 계약(`/acorns/{TYPE_CODE}.png`,
  `/illustrations/traffic-light.png`)은 변경하지 않는다.
- 같은 파일명으로 재처리할 때 `originals`를 덮어쓰면 안 된다.

### 22.4 교차 검증

1. 밝은 하늘색과 진한 초록색 배경에 각각 합성해 흰 프린지를 확인한다.
2. 네 모서리 알파값이 모두 `0`인지 확인한다.
3. 풍선·줄·체인·팔·소품 사이의 외부 연결 공간을 확대 확인한다.
4. 의도된 내부 흰색이 보존되었는지 원본과 비교한다.
5. 16개 캐릭터와 신호등의 파일 수, 크기, RGBA 채널을 확인한다.
6. 앱 사용본과 `ex.po/cutouts` 보관본이 동일한지 확인한다.

상세 판정과 자산별 SHA-256은 `docs/nukki-analysis.md`를 구현 검증 기록으로
사용한다. 재현 가능한 처리는
`frontend/scripts/extract_transparent_assets.py`로 수행한다.
