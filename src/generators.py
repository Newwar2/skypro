from typing import Generator


def filter_by_currency(my_list: list[dict], code: str) -> Generator:
    """Принимаем список словарей , возвращаем итератор."""
    for x in my_list:
        if x.get("currency_code", "") == code:
            yield x


def transaction_descriptions(my_list: list[dict]) -> Generator:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""
    for x in my_list:
        if x.get("description", {}):
            yield x["description"]


def card_number_generator(start: int = 1, stop: int = 999999999999999) -> Generator:
    """Генератор, который выдаёт номера банковских карт в формате XXXX XXXX XXXX XXXX."""
    for num_card in range(start, stop + 1):
        num_str = f"{num_card:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:]}"
