import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Предыдущий вариант теста
# def test_filter_by_currency(test_gen):
#     result = filter_by_currency(test_gen, "USD")
#     assert next(result) == {
#           "id": 939719570,
#           "state": "EXECUTED",
#           "date": "2018-06-30T02:08:58.425572",
#           "operationAmount": {
#               "amount": "9824.07",
#               "currency": {
#                   "name": "USD",
#                   "code": "USD"
#               }
#           },
#           "description": "Перевод организации",
#           "from": "Счет 75106830613657916952",
#           "to": "Счет 11776614605963066702"
#       }
#     assert next(result) == {
#               "id": 142264268,
#               "state": "EXECUTED",
#               "date": "2019-04-04T23:20:05.206878",
#               "operationAmount": {
#                   "amount": "79114.93",
#                   "currency": {
#                       "name": "USD",
#                       "code": "USD"
#                   }
#               },
#               "description": "Перевод со счета на счет",
#               "from": "Счет 19708645243227258542",
#               "to": "Счет 75651667383060284188"
#        }
@pytest.mark.parametrize(
    "test_gen, test_gen_2",
    [
        ("test_gen", "test_gen_2"),
    ],
    indirect=True,
)
def test_filter_by_currency(test_gen, test_gen_2):
    assert next(filter_by_currency(test_gen, "USD")) == test_gen_2


def test_transaction_descriptions(test_gen):
    result = transaction_descriptions(test_gen)
    assert next(result) == "Перевод организации"


def test_card_generator():
    # Генерируем один номер карты для числа 1234
    gen = card_number_generator(1234, 1234)
    result = next(gen)  # Берём первый (и единственный) элемент генератора

    # Ожидаемый результат: 16‑значное число с ведущими нулями, разбитое на группы по 4 цифры
    expected = "0000 0000 0000 1234"

    # Проверяем, что результат совпадает с ожидаемым
    assert result == expected
