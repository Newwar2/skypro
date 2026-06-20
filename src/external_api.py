import requests


def operation(code: str) -> int:
    """Функция, получения курса валют на сегодняшний день."""

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    result = int(
        data["Valute"][code]["Value"]
    )  # проваливаемся в словарь,выбираем валюту,code-EUR,RUB,и тд.,Value-курс на сегодня
    return result
