from __future__ import annotations

import time

import requests


STOCK_URL = "https://b2c-bff.woodongs.com/api/bff/v2/store/stock"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "gs25-stock-alert-bot/0.1",
        "Accept": "application/json",
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
        "pageNumber": 0,
        "pageCount": 100,
    }

    response = SESSION.get(
        STOCK_URL,
        params=params,
        timeout=10,
    )

    # Never hammer the endpoint after an explicit rate-limit response.
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
        raise RuntimeError(
            "GS25 API returned HTTP 403. Stop polling and review access/rate-limit behavior."
        )

    response.raise_for_status()

    data = response.json()
    return data.get("stores", [])