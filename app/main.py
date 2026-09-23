from __future__ import annotations

import time

from app.config import (
    GS25_LAT,
    GS25_LON,
    GS25_RADIUS,
    POLL_SECONDS,
)
from app.gs25_client import get_stock
from app.inventory import normalize_stocks
from app.notifier import notify_restock
from app.product_discovery import find_exact_product
from app.products import PRODUCTS
from app.state import (
    get_previous_quantity,
    init_db,
    save_quantity,
)


def resolve_product_codes_once() -> None:
    for product in PRODUCTS:
        if product["item_code"]:
            continue

        try:
            result = find_exact_product(product["name"])
        except Exception as exc:
            print(f"[PRODUCT ERROR] {product['name']}: {exc}")
            continue

        if result:
            product["item_code"] = result["item_code"]
            print(
                f"[PRODUCT] {product['name']} -> "
                f"{product['item_code']}"
            )
        else:
            print(f"[PRODUCT] itemCode not resolved: {product['name']}")


def run_once() -> None:
    for product in PRODUCTS:
        item_code = product["item_code"]

        if not item_code:
            print(f"[SKIP] itemCode missing: {product['name']}")
            continue

        try:
            stores = get_stock(
                item_code=item_code,
                latitude=GS25_LAT,
                longitude=GS25_LON,
                radius=GS25_RADIUS,
            )
        except Exception as exc:
            print(f"[STOCK ERROR] {product['name']}: {exc}")
            continue

        stocks = normalize_stocks(product, stores)

        for stock in stocks:
            store_code = stock["store_code"]

            if not store_code:
                continue

            current = stock["quantity"]
            previous = get_previous_quantity(item_code, store_code)

            # First observation seeds state without notifying.
            if previous == 0 and current > 0:
                notify_restock(stock)

            save_quantity(
                item_code=item_code,
                store_code=store_code,
                quantity=current,
            )


def main() -> None:
    init_db()
    resolve_product_codes_once()

    print(
        f"[START] polling every {POLL_SECONDS}s | "
        f"lat={GS25_LAT}, lon={GS25_LON}, radius={GS25_RADIUS}m"
    )

    while True:
        started = time.monotonic()

        try:
            run_once()
        except Exception as exc:
            print(f"[FATAL LOOP ERROR] {exc}")

        elapsed = time.monotonic() - started
        sleep_for = max(0, POLL_SECONDS - elapsed)

        print(
            f"[LOOP] elapsed={elapsed:.2f}s, "
            f"next_run_in={sleep_for:.2f}s"
        )

        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
