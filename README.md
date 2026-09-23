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

## 주의

이 프로젝트는 GS25 공식 공개 API SDK가 아니라 공개적으로 관찰·재현된 우리동네GS 앱 API 엔드포인트를 사용하는 MVP입니다. 서비스 이용약관과 호출 정책을 확인한 뒤 테스트/운영해야 합니다.

기본 polling interval은 60초이며, 호출 빈도를 높이기 전에 응답 상태코드와 오류율을 확인하세요.

## 실행

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

python scripts/search_products.py
python -m app.main
```
