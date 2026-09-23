from app.product_discovery import find_exact_product
from app.products import PRODUCTS


for product in PRODUCTS:
    result = find_exact_product(product["name"])

    print(f"\n### {product['name']}")

    if result:
        print(f"itemCode: {result['item_code']}")
        print(f"itemName: {result['item_name']}")
    else:
        print("itemCode: NOT_FOUND")
