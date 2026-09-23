from __future__ import annotations

import requests


SEARCH_URL = "https://b2c-apigw.woodongs.com/search/v3/totalSearch"


def _walk_documents(value):
    if isinstance(value, dict):
        field = value.get("field")

        if isinstance(field, dict):
            item_name = field.get("itemName")
            item_code = field.get("itemCode")

            if item_name and item_code:
                yield {
                    "item_name": str(item_name),
                    "item_code": str(item_code),
                }

        for child in value.values():
            yield from _walk_documents(child)

    elif isinstance(value, list):
        for child in value:
            yield from _walk_documents(child)


def search_products(keyword: str) -> list[dict]:
    response = requests.post(
        SEARCH_URL,
        json={"query": keyword},
        timeout=10,
    )
    response.raise_for_status()

    results = list(_walk_documents(response.json()))

    deduped = {}
    for result in results:
        deduped[(result["item_code"], result["item_name"])] = result

    return list(deduped.values())


def find_exact_product(product_name: str) -> dict | None:
    candidates = search_products(product_name)

    for candidate in candidates:
        if candidate["item_name"] == product_name:
            return candidate

    return candidates[0] if len(candidates) == 1 else None
