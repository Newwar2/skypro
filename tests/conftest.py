import pytest


@pytest.fixture
def test_my_list():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def test_gen():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]


@pytest.fixture
def expected():
    """Фикстура с ожидаемыми результатами для базовых тестов."""
    return {
        (1, 5): [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ],
        (9999, 10002): ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001", "0000 0000 0001 0002"],
    }


@pytest.fixture
def test_gen_2():
    return {
        "date": "2018-06-30T02:08:58.425572",
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "id": 939719570,
        "operationAmount": {"amount": "9824.07", "currency": {"code": "USD", "name": "USD"}},
        "state": "EXECUTED",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture
def utils_json():
    return [
        [
            {
                "date": "2019-08-26T10:50:58.294041",
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "id": 441945886,
                "operationAmount": {"amount": "31957.58", "currency": {"code": "RUB", "name": "руб."}},
                "state": "EXECUTED",
                "to": "Счет 64686473678894779589",
            },
            {
                "date": "2019-07-03T18:35:29.512364",
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "id": 41428829,
                "operationAmount": {"amount": "8221.37", "currency": {"code": "USD", "name": "USD"}},
                "state": "EXECUTED",
                "to": "Счет 35383033474447895560",
            },
        ]
    ] != [
        {
            "date": "2019-08-26T10:50:58.294041",
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "id": 441945886,
            "operationAmount": {"amount": "31957.58", "currency": {"code": "RUB", "name": "руб."}},
            "state": "EXECUTED",
            "to": "Счет 64686473678894779589",
        },
        {
            "date": "2019-07-03T18:35:29.512364",
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "id": 41428829,
            "operationAmount": {"amount": "8221.37", "currency": {"code": "USD", "name": "USD"}},
            "state": "EXECUTED",
            "to": "Счет 35383033474447895560",
        },
    ]


@pytest.fixture
def utils_conversion():
    return {
        "Date": "2026-06-18T11:30:00+03:00",
        "PreviousDate": "2026-06-17T11:30:00+03:00",
        "PreviousURL": "//www.cbr-xml-daily.ru/archive/2026/06/17/daily_json.js",
        "Timestamp": "2026-06-18T14:00:00+03:00",
        "Valute": {
            "USD": {
                "ID": "R01010",
                "NumCode": "036",
                "CharCode": "AUD",
                "Nominal": 1,
                "Name": "Австралийский доллар",
                "Value": 5,
                "Previous": 50.8434,
            }
        },
    }
