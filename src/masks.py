def get_mask_card_number(card: str) ->str:
    """Функция скрытие номера карты"""

    if len(card) < 16:
        return "Не корректный номер карты"
    else:
        return f"{card[:-12]} {card[-12:-10]}** **** {card[-4:]}"

def get_mask_account(account: str) ->str:
    """Функция скрытия номера счета"""

    if len(account) < 4:
        return "Не корректный номер счета"
    else:
        return f"**{account[-4:]}"