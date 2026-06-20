import requests


def operation(code):
    """Функция, получения курса валют на сегодняшний день."""

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    result = data["Valute"][code][
        "Value"
    ]  # проваливаемся в словарь,выбираем валюту,code-EUR,RUB,и тд.,Value-курс на сегодня
    return result


if __name__ == "__main__":
    print(operation("USD"))
