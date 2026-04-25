def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты в формате 'XXX XX** **** XXXX'

    Аргументы:
        card_number: Номер карты (должен содержать 16 цифр без пробелов)

    Возвращает:
        str: Маскированный номер карты

    Пример:
        >>> get_mask_card_number("1234567812345678")
        '1234 56** **** 5678'
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате '*XXXX'

    Аргументы:
        account_number: Номер счета (должен содержать минимум 4 цифры)

    Возвращает:
        str: Маскированный номер счета

    Пример:
        >>> get_mask_account("12345678")
        '*5678'
    """
    if len(account_number) < 4 or not account_number.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"*{account_number[-4:]}"


# Пример использования
if __name__ == "__main__":
    print(get_mask_card_number("1234567812345678"))  # 1234 56** **** 5678
    print(get_mask_account("12345678"))  # *5678


