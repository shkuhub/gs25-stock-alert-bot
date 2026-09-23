from __future__ import annotations

import requests


STOCK_URL = "https://b2c-bff.woodongs.com/api/bff/v2/store/stock"


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

    response = requests.get(
        STOCK_URL,
        params=params,
        timeout=10,
        headers={
            "User-Agent": "gs25-stock-alert-bot/0.1",
            "Accept": "application/json",
        },
    )
    response.raise_for_status()

    data = response.json()
    return data.get("stores", [])
