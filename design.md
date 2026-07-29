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
framework: Next.js 16 App Router
language: TypeScript + React
styling: global CSS
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
- 카드 외곽선 두께 `3px`
- 카드 그림자 방향: 오른쪽 아래
- 시작 화면 히어로 높이 `398px`
- 질문 카드 높이 `258px`
- 제공된 16개 도토리 이미지
- 신호등 이미지 `traffic-light.png`
- 위험 신호 API 값 `GREEN`, `YELLOW`, `RED`
- 닉네임 최대 길이 12자
- 질문 응답값: 선택지 순서 기준 `1`부터 시작하는 정수

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
| 최소 화면 높이 | `844px` |
| 좌우 기본 패딩 | `16px` |
| 상단 패딩 | `18px` |
| 하단 패딩 | `24px` |
| 콘텐츠 기준 너비 | `358px` |

현재 `.mobile-screen`, `.result-screen`은 고정 너비 `390px`을 사용한다. 화면 폭이 `389px` 이하일 때는 `100vw`로 축소한다.

```css
.mobile-screen,
.result-screen {
  width: 390px;
  min-height: 844px;
  padding: 18px 16px 24px;
}

@media (max-width: 389px) {
  .mobile-screen,
  .result-screen {
    width: 100vw;
  }
}
```

### 4.2 정렬 원칙

- 데스크톱에서도 모바일 캔버스 비율을 유지한다.
- 현재 구현은 캔버스를 화면 왼쪽 위에 배치한다.
- 서비스 배포 시 데스크톱 중앙 정렬이 필요하다면 전체 페이지 셸에서만 처리하고, 모바일 캔버스 내부 치수는 유지한다.
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

모바일 캔버스 바깥 영역은 `#DBE8DF`를 사용한다. 이 색은 앱 캔버스와 분리되면서도 전체 자연 계열 팔레트에 포함된다.

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

### 6.2 권장 타입 스케일

| 용도 | 크기 | 행간 | 굵기 |
|---|---:|---:|---:|
| 시작 화면 브랜드 제목 | `55px` | `0.9` | Black Han Sans |
| 결과 유형 강조 | `35–48px` | `1.05` | Black Han Sans |
| 설문 질문 | `34px` | `1.15` | Black Han Sans |
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
- 연두 배경 `#D8EFC8`
- 2px 테두리
- 입력 텍스트 `15px / 800`
- 오른쪽에 글자 수 표시
- 포커스 시 반투명 녹색 링

검증 메시지가 추가될 경우 입력 바로 아래에 배치하며, 빨강만 사용하지 말고 문구와 아이콘을 함께 제공한다.

### 8.8 종이 카드

예: `.start-note`, `.summary-card`

- 배경 `--paper`
- 3px 외곽선
- 비대칭 모서리
- 녹색 오프셋 그림자
- 상단에 테이프 또는 라벨 부착 가능

### 8.9 추천 카드

- 2열 그리드
- 짙은 녹색 배경과 흰색 텍스트
- 카테고리는 연두색 작은 칩
- 제목, 설명, 키워드 순서
- 작은 화면에서도 각 카드의 최소 너비가 깨지지 않게 `minmax(0, 1fr)` 사용

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
2. 파란색 히어로 카드
3. `CHECK POINT` 종이 카드
4. 닉네임 입력
5. 주요 CTA

### 히어로 카드

- 높이 `398px`
- 파란 하늘 배경
- 아래쪽에 잔디 언덕
- 왼쪽에 큰 브랜드 제목
- 오른쪽 아래에 탐구 도토리
- 상단에 노란 질문 스티커

제목은 `도토리 / 금융 DNA` 두 줄로 구성하고, 크림색 채움·짙은 외곽선·단단한 텍스트 그림자를 사용한다.

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

- 흰 종이 카드
- 상단 노란 `DNA REPORT` 테이프
- 한 문단 요약
- 정부지원 및 은행권 추천을 2열로 배치
- 핵심 키워드는 캡슐형 칩으로 표시

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
- `389px` 이하: 화면 폭을 `100vw`로 변경

### 추가 권장 규칙

#### 360px 이하

- 큰 제목을 약 5–8% 축소
- 추천 카드가 지나치게 좁아지면 1열로 전환
- 신호등 안내 카드의 텍스트 줄바꿈 확인

#### 데스크톱

- 모바일 캔버스를 페이지 중앙에 배치
- 외부 배경은 `#DBE8DF` 유지
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
- Next.js의 `Image` 컴포넌트 도입 시 레이아웃 크기를 명시해 이동을 방지한다.

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
├─ next.config.ts
├─ src/
│  ├─ app/
│  │  ├─ globals.css
│  │  ├─ layout.tsx
│  │  ├─ page.tsx
│  │  ├─ start/page.tsx
│  │  └─ survey/page.tsx
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

프런트엔드 실행 명령:

```powershell
cd frontend
npm install
npm run dev
```

기본 URL:

```text
http://localhost:3000/start
```

포트가 이미 사용 중일 때만 다른 포트를 허용한다.

```powershell
npm run dev -- -p 3100
```

백엔드 API 기본 URL:

```text
http://localhost:8000
```

## 21.3 문서와 메타데이터

루트 레이아웃 MUST 조건:

```tsx
<html lang="ko">
  <body>{children}</body>
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
  background: #dbe8df;
  color: #173f32;
  font-family: "Noto Sans KR", sans-serif;
}

body {
  display: grid;
  place-items: start start;
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
  width: 390px;
  min-height: 844px;
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
@media (max-width: 389px) {
  .mobile-screen,
  .result-screen {
    width: 100vw;
  }
}
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
│  ├─ span.start-sticker
│  ├─ div.start-title
│  │  ├─ p
│  │  ├─ h1
│  │  │  ├─ text "도토리"
│  │  │  ├─ br
│  │  │  └─ strong "금융 DNA"
│  │  └─ span "TEST"
│  ├─ img.start-character-image
│  └─ div.start-hill
├─ section.start-note
│  ├─ span "CHECK POINT"
│  ├─ h2
│  ├─ div.signal-guide
│  │  ├─ img.signal-illustration
│  │  └─ div
│  │     ├─ strong
│  │     └─ p.checkpoint-copy
│  └─ div.nickname-field
│     ├─ label
│     ├─ input
│     └─ small
└─ button.start-cta
   ├─ text
   └─ span
```

### 21.9.3 정확한 문구

```yaml
sticker: "나의 돈 성향은?"
eyebrow: "자립을 준비하는 나를 위한"
title_line_1: "도토리"
title_line_2: "금융 DNA"
test_label: "TEST"
checkpoint_label: "CHECK POINT"
checkpoint_heading_line_1: "나의 금융 위험 신호를"
checkpoint_heading_line_2: "신호등으로 한눈에 확인해요"
signal_title: "안정 · 주의 · 위험"
signal_copy: "단계에 맞춰 필요한 도움을 안내해 드려요."
nickname_label: "결과에서 사용할 닉네임을 알려주세요"
nickname_placeholder: "닉네임을 입력해 주세요"
cta_main: "내 도토리 찾기"
cta_sub: "시작하기 ↗"
```

제목과 체크포인트 헤딩의 강제 줄바꿈은 반드시 유지한다.

### 21.9.4 시작 히어로 박스

```css
.start-hero {
  height: 398px;
  border: 3px solid #173f32;
  border-radius: 16px 11px 20px 14px;
  background: #9edaf1;
  box-shadow: 8px 9px 0 #245943;
  position: relative;
  overflow: hidden;
}
```

잔디 언덕:

```css
.start-hero::after {
  content: "";
  position: absolute;
  left: -28px;
  right: -28px;
  bottom: -43px;
  height: 134px;
  border: 3px solid #173f32;
  border-radius: 50% 50% 0 0;
  background: #8fc77a;
  z-index: 1;
}
```

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
  text-shadow: 5px 5px 0 #173f32;
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
  min-height: 286px;
  margin: 19px 4px 0 0;
  padding: 24px 18px 18px;
  background: #fffdf4;
  border: 3px solid #173f32;
  border-radius: 12px 18px 12px 16px;
  box-shadow: 7px 8px 0 #6ea56a;
  position: relative;
}

.start-note h2 {
  margin: 0 0 8px;
  font-size: 20px;
  line-height: 1.4;
  letter-spacing: -0.04em;
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
  font-size: 12px;
  font-weight: 900;
  letter-spacing: -0.02em;
  color: #173f32;
}

.checkpoint-copy {
  margin: 0;
  font-size: 10px;
  line-height: 1.45;
  font-weight: 700;
  color: #547365;
}
```

### 21.9.9 닉네임 필드

```css
.nickname-field {
  position: relative;
  padding-top: 14px;
  border-top: 2px dashed #b7c6b7;
}

.nickname-field label {
  display: block;
  margin-bottom: 8px;
  font-size: 11px;
  font-weight: 900;
}

.nickname-field input {
  width: 100%;
  height: 58px;
  padding: 0 48px 0 16px;
  border: 2px solid #173f32;
  border-radius: 29px;
  background: #d8efc8;
  color: #173f32;
  font-size: 15px;
  font-weight: 800;
  outline: none;
}

.nickname-field input:focus {
  box-shadow: 0 0 0 4px rgba(57, 124, 85, 0.2);
}

.nickname-field small {
  position: absolute;
  right: 16px;
  bottom: 20px;
  font-size: 9px;
  font-weight: 900;
  color: #547365;
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
  background: #245943;
  color: white;
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

## 21.10 `/survey` 정확한 구현

### 21.10.1 데이터 및 진행

```yaml
loading_initial: true
answer_array_initial_value: 0
answer_value_range: 1..option_count
current_question_index: zero_based
display_question_number: one_based
auto_advance: true
previous_button_on_first_question: disabled
submit_on_last_answer: true
result_storage_key: dotori-result
result_route: /
```

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
question_guide: "가장 나와 가까운 답 하나를 골라주세요."
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
  font-size: 34px;
  line-height: 1.15;
  font-weight: 400;
  letter-spacing: -0.045em;
}
```

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

### 21.11.4 추천 영역

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

### 21.11.5 위험 신호

정확한 매핑:

| API 값 | 단계명 | 카드 클래스 | 배경 | 현재 표시 |
|---|---|---|---|---|
| `GREEN` | 안정 신호 | `risk-green` | `#D7EBC6` | `🟢` |
| `YELLOW` | 주의 신호 | `risk-yellow` | `#FFF0B8` | `🟡` |
| `RED` | 위험 신호 | `risk-red` | `#F6C5B8` | `🔴` |

주의: 시작 화면에서는 이모지 나열을 금지하지만, 결과 카드의 단계 아이콘은 현재 구현 보존을 위해 위 표대로 유지한다. 결과 카드도 신호등 이미지로 변경하려면 별도 디자인 변경으로 취급한다.

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
| `acorns/FVRI.png` | 817900 | `0f8427ef9c11443ebe4e9defc3b8b75e7f93b678598a3eb71e50db3811314716` |
| `acorns/FVRS.png` | 1154993 | `0a9bcd61fc191a73619eb10f1e1f971463af4ea2da6f48c8c61b56afac9cde95` |
| `acorns/PEAI.png` | 990040 | `7b3f3faca10b0ba1cc68cbe8f82404b2e96344ee7a2c1d93c6c3485240fc0b6d` |
| `acorns/PEAS.png` | 1223399 | `b5c63b58699fc80ac3129de52540ee6c5d83b4d5f57ad6b6cf858c433767aba9` |
| `acorns/PERI.png` | 1221351 | `9f0d52bce84aa1641a6c5dd70ee4a03b5401d511ca4e568254fa4deab2d78858` |
| `acorns/PERS.png` | 1041245 | `ecf58d8d2e6d3b84fe4039dc982826975bfa9e479d359add6c6523b1c7c826da` |
| `acorns/PVAI.png` | 1261820 | `da8669ef44ea115709da949cc873479e2b24b2260e380d8bdb541f177dfe88d7` |
| `acorns/PVAS.png` | 1544585 | `0e37eb4451d9f1229e2b2c75a3f22298822ca8315bc11f1c0a461a652c01b2ad` |
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
- [ ] 시작 히어로가 `398px`이다.
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
