def notify_restock(stock: dict) -> None:
    print(
        "[RESTOCK]",
        stock["product_name"],
        "|",
        stock["store_name"],
        "|",
        stock["quantity"],
        "|",
        stock["store_address"],
    )
