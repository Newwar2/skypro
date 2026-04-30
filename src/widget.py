from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(mai_string: str) ->str:
    """Функция обработки введенных данных Счет или Карта
    и вывода замаскированной информации"""

    card = get_mask_card_number(mai_string)
    account = get_mask_account(mai_string)

    if "Счет" in mai_string:
        return f"Счет {account}"
    else:
        return card

if __name__ == '__main__':
    print(mask_account_card("Maestro 1596837868705199"))
    print(mask_account_card("Счет 64686473678894779589"))