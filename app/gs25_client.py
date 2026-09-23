from __future__ import annotations

import time

import requests


STOCK_URL = "https://b2c-bff.woodongs.com/api/bff/v2/store/stock"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 15; SM-S928N) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/124.0 Mobile Safari/537.36"
        ),
        "Origin": "https://woodongs.com",
        "Referer": "https://woodongs.com/",
    }
)


def get_stock(
    item_code: str,
    latitude: float,
    longitude: float,
    radius: int = 500,
) -> list[dict]:
    params = {
        "serviceCode": "01",
        "itemCode": item_code,
        "myPositionXCoordination": longitude,
        "myPositionYCoordination": latitude,
        "centerPositionXCoordination": longitude,
        "centerPositionYCoordination": latitude,
        "radiusCondition": radius,
        "pickupStoreYn": "N",
        "realTimeStockYn": "Y",
        "isSuperDlvyStoreSelected": "N",
        "isGs25DlvyStoreSelected": "N",
        "pageNumber": 0,
        "pageCount": 100,
    }

    response = SESSION.get(
        STOCK_URL,
        params=params,
        timeout=10,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        try:
            delay = max(1, min(int(retry_after), 300)) if retry_after else 60
        except ValueError:
            delay = 60

        print(f"[RATE LIMIT] 429 received; sleeping {delay}s")
        time.sleep(delay)

        raise RuntimeError(
            f"GS25 API rate limited (HTTP 429); retry_after={delay}s"
        )

    if response.status_code == 403:
        body = response.text.strip().replace("\n", " ")
        if len(body) > 500:
            body = body[:500] + "..."

        raise RuntimeError(
            "GS25 API returned HTTP 403. "
            "The request is being denied before normal inventory response. "
            f"Response body: {body or '<empty>'}"
        )

    response.raise_for_status()

    data = response.json()
    return data.get("stores", [])
