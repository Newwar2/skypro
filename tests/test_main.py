from src.transactions import filter_rub_only

data = [
    {"amount": 100, "currency": "RUB"},
    {"amount": 200, "currency": "USD"},
    {"amount": 300, "currency": "rub"},  # регистр разный
]

result = filter_rub_only(data)
print("Результат:", result)
print("Количество:", len(result))
