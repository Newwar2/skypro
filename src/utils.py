import json
from json import JSONDecodeError
from typing import Any

from src.external_api import operation


def read_json(path_json: str) -> Any:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях."""
    try:
        with open(path_json) as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except JSONDecodeError:
        data = []

    return data


def convertetion(transaction: dict) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях."""
    code: str = transaction["operationAmount"]["currency"]["code"]  # показывает, что используется другая валюта
    rub_pay: float = float(transaction["operationAmount"]["amount"])
    if code == "RUB":
        return rub_pay
    else:
        kurs: float = round(operation(code))
        result: float = rub_pay * kurs
        return result
