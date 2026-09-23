def normalize_stocks(product: dict, stores: list[dict]) -> list[dict]:
    normalized = []

    for store in stores:
        try:
            quantity = int(store.get("realStockQuantity", 0) or 0)
        except (TypeError, ValueError):
            quantity = 0

        normalized.append(
            {
                "product_name": product["name"],
                "item_code": product["item_code"],
                "store_code": store.get("storeCode"),
                "store_name": store.get("storeName"),
                "store_address": store.get("storeAddress"),
                "quantity": quantity,
                "latitude": store.get("storeYCoordination"),
                "longitude": store.get("storeXCoordination"),
            }
        )

    return normalized
