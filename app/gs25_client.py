from __future__ import annotations

import time
from typing import Any

import requests


DIRECT_STOCK_URL = "https://b2c-bff.woodongs.com/api/bff/v2/store/stock"
RELAY_INVENTORY_URL = "https://mcp.aka.page/api/gs25/inventory"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Origin": "https://woodongs.com",
        "Referer": "https://woodongs.com/",
    }
)


def _get_direct_stock(
    item_code: str,
    latitude: float,
    longitude: float,
    radius: int,
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
        DIRECT_STOCK_URL,
        params=params,
        timeout=10,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        try:
            delay = max(1, min(int(retry_after), 300)) if retry_after else 60
        except ValueError:
            delay = 60

        print(f"[RATE LIMIT] direct API 429; sleeping {delay}s")
        time.sleep(delay)
        raise RuntimeError(
            f"GS25 direct API rate limited (HTTP 429); retry_after={delay}s"
        )

    if response.status_code == 403:
        body = response.text.strip().replace("\n", " ")
        if len(body) > 500:
            body = body[:500] + "..."
        raise RuntimeError(
            "GS25 direct API returned HTTP 403. "
            f"Response body: {body or '<empty>'}"
        )

    response.raise_for_status()

    data = response.json()
    return data.get("stores", [])


def _extract_relay_stores(data: dict[str, Any]) -> list[dict]:
    inventory = data.get("inventory")
    if isinstance(inventory, dict):
        stores = inventory.get("stores")
        if isinstance(stores, list):
            return stores

    # Some relay responses may expose data directly.
    stores = data.get("stores")
    if isinstance(stores, list):
        return stores

    return []


def _get_relay_stock(
    item_code: str,
    latitude: float,
    longitude: float,
) -> list[dict]:
    params = {
        "itemCode": item_code,
        "lat": latitude,
        "lng": longitude,
        "storeLimit": 100,
    }

    response = SESSION.get(
        RELAY_INVENTORY_URL,
        params=params,
        timeout=20,
    )

    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        try:
            delay = max(1, min(int(retry_after), 300)) if retry_after else 60
        except ValueError:
            delay = 60

        print(f"[RATE LIMIT] relay API 429; sleeping {delay}s")
        time.sleep(delay)
        raise RuntimeError(
            f"GS25 relay API rate limited (HTTP 429); retry_after={delay}s"
        )

    response.raise_for_status()

    data = response.json()

    if data.get("success") is False:
        raise RuntimeError(
            f"GS25 relay returned an unsuccessful response: {data}"
        )

    return _extract_relay_stores(data)


def get_stock(
    item_code: str,
    latitude: float,
    longitude: float,
    radius: int = 500,
    source: str = "relay",
) -> list[dict]:
    source = source.lower().strip()

    if source == "relay":
        return _get_relay_stock(
            item_code=item_code,
            latitude=latitude,
            longitude=longitude,
        )

    if source == "direct":
        return _get_direct_stock(
            item_code=item_code,
            latitude=latitude,
            longitude=longitude,
            radius=radius,
        )

    raise ValueError("GS25 source must be 'relay' or 'direct'")
