def get_mask_card_number(card: str) ->str:
    """Функция скрытие номера карты"""

    if len(card) < 16:
        return "Не корректный номер карты"
    else:
        return f"{card[:4]} {card[4:6]}** **** {card[-4:]}"