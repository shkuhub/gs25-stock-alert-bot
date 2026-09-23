from __future__ import annotations

import argparse

from app.config import GS25_LAT, GS25_LON, GS25_RADIUS, GS25_SOURCE
from app.gs25_client import get_stock
from app.inventory import normalize_stocks
from app.product_discovery import find_exact_product


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve one GS25 product and perform one stock lookup."
    )
    parser.add_argument("product_name", help="Exact GS25 product name")
    args = parser.parse_args()

    print(f"[SEARCH] {args.product_name}")
    product = find_exact_product(args.product_name)

    if not product:
        raise SystemExit("[FAIL] itemCode could not be resolved.")

    print(f"[FOUND] itemCode={product['item_code']}")
    print(f"[FOUND] itemName={product['item_name']}")
    print(f"[SOURCE] {GS25_SOURCE}")

    product["name"] = product["item_name"]

    print(
        f"[STOCK] lat={GS25_LAT}, lon={GS25_LON}, "
        f"radius={GS25_RADIUS}m"
    )

    stores = get_stock(
        item_code=product["item_code"],
        latitude=GS25_LAT,
        longitude=GS25_LON,
        radius=GS25_RADIUS,
        source=GS25_SOURCE,
    )

    stocks = normalize_stocks(product, stores)

    print(f"[RESULT] stores={len(stocks)}")

    in_stock = [stock for stock in stocks if stock["quantity"] > 0]

    if not in_stock:
        print("[RESULT] No stores with reported stock.")
        return

    print(f"[RESULT] stores_with_stock={len(in_stock)}")

    for stock in in_stock:
        print(
            f"- {stock['store_name']} | "
            f"qty={stock['quantity']} | "
            f"{stock['store_address']}"
        )


if __name__ == "__main__":
    main()
