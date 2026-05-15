import pytest

from src.masks import get_mask_card_number

@pytest.mark.parametrize(
    "type_card, real_result",
    [
        ("1234567891234567", "1234 56** **** 4567"),
        (" ", "Не корректный номер карты")

    ]

)

def test_get_mask_card_number(type_card, real_result):
    assert get_mask_card_number(type_card) == real_result

