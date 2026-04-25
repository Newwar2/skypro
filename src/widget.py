def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты по шаблону: XXXX XXXX XXXX XXXX,
    где X — видимые цифры (первые 6 и последние 4),
    остальные заменяются на *.
    """
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр")

    return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} **** {card_number[-4:]}"



def mask_account_number(account_number: str) -> str:
    """
    Маскирует номер счёта по шаблону: *************XX,
    где видны только последние 2 цифры, остальные заменяются на *.
    """
    if not account_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    if len(account_number) < 2:
        raise ValueError("Номер счёта слишком короткий")

    masked = "*" * (len(account_number) - 2) + account_number[-2:]
    # Разбиваем на группы по 4 символа для читаемости
    chunks = [masked[i:i + 4] for i in range(0, len(masked), 4)]
    return " ".join(chunks)

def get_date_manual(iso_date_string: str) -> str:
    date_part = iso_date_string.split('T')[0]  # Берём часть до 'T'
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"
