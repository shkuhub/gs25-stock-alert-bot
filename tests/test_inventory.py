from app.inventory import normalize_stocks


def test_normalize_stocks():
    product = {
        "name": "test",
        "item_code": "123",
    }

    stores = [
        {
            "storeCode": "A",
            "storeName": "GS25 Test",
            "storeAddress": "Seoul",
            "realStockQuantity": "2",
        }
    ]

    result = normalize_stocks(product, stores)

    assert result[0]["store_code"] == "A"
    assert result[0]["quantity"] == 2
