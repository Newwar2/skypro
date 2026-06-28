from src.transactions import count_operations_by_category, process_bank_search


def test_process_bank_search_basic():
    data = [
        {"id": 1, "description": "Оплата в Пятёрочке"},
        {"id": 2, "description": "Перевод другу"},
        {"id": 3, "description": "Покупка в OZON"},
    ]
    # Ищи именно «пятёрочке» (с «ё»), как в данных
    result = process_bank_search(data, "пятёрочке")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_count_simple():
    data = [
        {"description": "Пятерочка: покупка"},
        {"description": "Перевод другу"},
        {"description": "Покупка в OZON"},
    ]
    categories = ["пятерочка", "перевод"]

    result = count_operations_by_category(data, categories)

    # ВРЕМЕННО: чтобы видеть, что происходит внутри
    print("DATA:", [d["description"] for d in data])
    print("CATEGORIES:", categories)
    print("RESULT:", result)

    assert result == {"пятерочка": 1, "перевод": 1}
