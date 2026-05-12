import pytest
from src.masks import get_mask_card_number

@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("fa34567890123456", "Введен не корректный номер карты"),
        ("12345678901234567", "Введен не корректный номер карты"),
        ("123456789012345", "Введен не корректный номер карты"),
        ("1234567890123456", "1234 56** **** 3456")
    ]
)

def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Функция для проверки маскировки карты"""
    assert get_mask_card_number(card_number) == expected
