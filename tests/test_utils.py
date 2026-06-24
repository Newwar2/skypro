import json
import os
from json import JSONDecodeError
import pandas
# from pygments.lexers.webassembly import builtins

from config import ROOT_DIR
from src.utils import convertetion, read_json, transactions_csv, transactions_excel
from unittest.mock import Mock, patch


def test_read_json(utils_json):
    test = Mock(return_value=utils_json)
    json.load = test
    way_file = os.path.join(ROOT_DIR, "data", "operations.json")
    assert read_json(way_file) == utils_json


@patch("builtins.open")
def test_error(mock_open):
    mock_open.side_effect = FileNotFoundError
    assert read_json("") == []

    mock_open.side_effect = JSONDecodeError(" ", "", 0)
    assert read_json("") == []


def test_convertetion_rub():
    rub_test = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }
    assert convertetion(rub_test) == 31957.58


def test_conversion_usd(utils_convertation):
    usd_test = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }

    mock_requests = Mock()
    mock_requests.get.return_value.json.return_value = utils_convertation

    with patch("src.external_api.requests", mock_requests):
        assert convertetion(usd_test) == 41106.850000000006


@patch("pandas.read_csv")
def test_read_csv(mock_df):
    mock_df.return_value = pandas.DataFrame(
        [
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            }
        ]
    )
    result_1 = transactions_csv("data/transactions.csv")
    assert result_1[0]["id"] == 41428829


@patch("pandas.read_csv")
def test_read_excel(mock_df):
    mock_df.return_value = pandas.DataFrame(
        [
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            }
        ]
    )
    result_2 = transactions_excel("data/transactions_excel.xlsx")
    assert result_2[0]["id"] == 650703.0
