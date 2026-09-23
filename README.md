## Android 앱 검증 경로

현재 직접 GS25 upstream은 HTTP 403, 공개 relay는 GS25_API_KEY 부재로 503을 반환합니다. 공식 우리동네GS Android 앱(com.gsr.gs25)을 ADB로 자동 조작하는 검증 경로를 추가했습니다. 자세한 내용은 docs/android-test.md를 참고하세요.

# GS25 Stock Alert Bot

GS25 상품 재고를 조회하고 재입고(0 → 1 이상) 이벤트를 감지하기 위한 Python MVP입니다.

## 대상 상품

- 민음사)모카번(커스타드) — 8809844305034
- 민음사)모카번(우유크림) — 8809844305027
- 민음사)깨찰빵(커스타드) — 8809844305010
- 민음사)깨찰빵(솔티밀크) — 8809844305003

## 데이터 소스

현재 MVP 기본값은 공개 GS25 재고 릴레이입니다.

- `GS25_SOURCE=relay`: `https://mcp.aka.page/api/gs25/inventory`
- `GS25_SOURCE=direct`: 우리동네GS의 관찰된 upstream endpoint 직접 호출

현재 사용자의 환경에서는 direct 호출이 HTTP 403(CloudFront)로 차단되므로 먼저 relay 경로로 기능을 검증합니다.

공개 릴레이 프로젝트는 GS25 inventory REST 응답에 약 2분 edge cache를 적용하고 있으며, 공개 서버에는 IP당 일일 3,000회 GET 제한이 운영됩니다. 이 제한은 GS25가 설정한 제한이 아니라 해당 릴레이 서버 운영 정책입니다.

## Polling 안전장치

기본 polling 주기는 **5분(300초)** 입니다.

30초 polling은 공식 GS25 rate limit이 확인된 기능이 아니므로 기본 활성화하지 않습니다.

예:

```env
POLL_SECONDS=30
ALLOW_HIGH_FREQUENCY_POLLING=true
```

HTTP 429가 반환되면 추가 호출을 이어가지 않고 Retry-After를 참고해 대기합니다.

## 실행

```powershell
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
Copy-Item .env.example .env

python -m scripts.search_products
python -m scripts.test_stock_once "민음사)모카번(커스타드)"
```

검색 결과의 itemCode는 다음과 같습니다.

- 민음사)모카번(커스타드): `8809844305034`
- 민음사)모카번(우유크림): `8809844305027`
- 민음사)깨찰빵(커스타드): `8809844305010`
- 민음사)깨찰빵(솔티밀크): `8809844305003`

재입고 polling:

```powershell
python -m app.main
```

Threads 자동 게시 기능은 재고 감지 검증 후 연결합니다.
