import pytest

from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "type_card, real_result", [("1234567891234567", "1234 56** **** 4567"), (" ", "Не корректный номер карты")]
)
def test_get_mask_card_number(type_card, real_result):
    assert get_mask_card_number(type_card) == real_result


@pytest.mark.parametrize(
    "test_account, result_account", [("7000792289606361", "**6361"), ("123", "Не корректный номер счета")]
)
def test_get_mask_account(test_account, result_account):
    assert get_mask_account(test_account) == result_account
