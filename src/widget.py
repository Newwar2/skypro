from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(mai_string: str) -> str:
    """Функция обработки введенных данных Счет или Карта
    и вывода замаскированной информации"""

    card = get_mask_card_number(mai_string)
    account = get_mask_account(mai_string)

    if "Счет" in mai_string:
        return f"Счет {account}"
    else:
        return card


def get_date(date: str) -> str:
    """Функция возврата времени в формате ДД.ММ.ГГГГ"""

    new_date = datetime.fromisoformat(date).strftime("%d.%m.%Y")
    return new_date
