import json
import os
from config import ROOT_DIR
from src.utils import convertetion, read_json
from unittest.mock import Mock, patch


def test_read_json(utils_json):
    test = Mock(return_value=utils_json)
    json.load = test
    way_file = os.path.join(ROOT_DIR, "data", "operations.json")
    assert read_json(way_file) == utils_json


def test_read_json_success():
    mock_data = [{"id": 99, "amount": 500}]
    with patch("builtins.open") as mock_open:
        # Эмулируем работу with open(...) as file:
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = json.dumps(mock_data)

        result = read_json("fake.json")

    assert result == mock_data


def test_read_json_file_not_found():
    from builtins import FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError()):
        result = read_json("missing.json")
    assert result == []

def test_convertetion_rub():
    rub_test = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
  }
    assert convertetion(rub_test) == "31957.58"


def test_convertetion_usd(utils_convertation):
    usd_test = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  }
    a = Mock()
    a.requests.get.return_value = utils_convertation
    assert convertetion(usd_test) == 600160.01

