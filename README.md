# GS25 Stock Alert Bot

GS25 상품 재고를 조회하고 재입고(0 → 1 이상) 이벤트를 감지하기 위한 Python MVP입니다.

## 대상 상품

- 민음사)모카번(커스타드)
- 민음사)모카번(우유크림)
- 민음사)깨찰빵(커스타드)
- 민음사)깨찰빵(솔티밀크)

## 현재 범위

1. GS25 상품 검색 API로 상품명 → itemCode 탐색
2. GS25 재고 조회 API로 좌표 주변 매장 재고 조회
3. SQLite에 이전 재고 상태 저장
4. 이전 0 → 현재 1 이상인 경우 재입고 이벤트 출력

Threads 자동 게시 기능은 API 자격증명 설정 후 별도 단계로 연결합니다.

## Polling 안전장치

기본 polling 주기는 **5분(300초)** 입니다.

30초 polling은 공식 rate limit이 확인된 기능이 아니므로 기본 활성화하지 않습니다. 실제 호출 패턴과 응답을 충분히 검증한 뒤에만 명시적으로 사용할 수 있습니다.

환경변수 예:

    POLL_SECONDS=30
    ALLOW_HIGH_FREQUENCY_POLLING=true

HTTP 429가 반환되면 추가 호출을 이어가지 않고 Retry-After를 참고해 대기한 뒤 해당 사이클을 중단합니다. HTTP 403이 반환되면 polling을 멈추고 접근/호출 정책을 재검토합니다.

## 주의

이 프로젝트는 GS25 공식 공개 API SDK가 아니라 공개적으로 관찰·재현된 우리동네GS 앱 API 엔드포인트를 사용하는 MVP입니다. 서비스 이용약관과 호출 정책을 확인한 뒤 테스트/운영해야 합니다.

공식 자료에서 외부 봇에 대한 구체적인 30초/분당/일일 rate limit을 확인하지 못했으므로, 호출 빈도를 보수적으로 시작합니다.

## 실행

    python -m venv .venv

Windows:

    .venv\Scripts\activate

macOS/Linux:

    source .venv/bin/activate

    pip install -r requirements.txt
    copy .env.example .env  # Windows
    # cp .env.example .env  # macOS/Linux

    python scripts/search_products.py
    python -m app.main