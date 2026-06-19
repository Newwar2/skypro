import json
from json import JSONDecodeError

from src.external_api import operation


def read_json(path_json):
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


def convertetion(transaction):
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях."""

    if transaction["operationAmount"]["currency"]["code"] == "RUB":
        return transaction["operationAmount"]["amount"]
    else:
        code = transaction["operationAmount"]["currency"]["code"]  # показывает, что используется другая валюта
        kurs = round(operation(code))
        rub_pay = float(transaction["operationAmount"]["amount"])
        result = rub_pay * kurs
        return result
