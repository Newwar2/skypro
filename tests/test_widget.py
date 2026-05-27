import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "mai_string, my_result",
    [
        ("1234567891124567", "1234 56** **** 4567"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ],
)
def test_mask_account_card(mai_string, my_result):
    assert mask_account_card(mai_string) == my_result


@pytest.mark.parametrize(
    "date, new_date", [("2023-01-01", "01.01.2023"), ("2024-12-31", "31.12.2024"), ("2025-05-15", "15.05.2025")]
)
def test_get_date(date, new_date):
    assert get_date(date) == new_date
