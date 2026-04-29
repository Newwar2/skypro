from src.masks import get_mask_card_number  # предполагаем, что эта функция уже есть
from datetime import datetime, date


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта: оставляет последние 2 цифры, остальные заменяет на **."""
    if len(account_number) < 2:
        raise ValueError("Номер счёта должен содержать минимум 2 цифры")
    return f"**{account_number[-2:]}"

def get_date(date_string: str = None, date_format: str = '%Y-%m-%d') -> datetime | date:
    """
    Если передана строка — парсит дату из строки.
    Если строка не передана — возвращает текущую дату.
    """
    if date_string is None:
        return date.today()

    try:
        return datetime.strptime(date_string, date_format)
    except ValueError as e:
        raise ValueError(
            f"Некорректный формат даты: '{date_string}'. "
            f"Ожидаемый формат: '{date_format}'"
        ) from e

def mask_account_card(date: str) -> str:
    """Принимаем строку с типом и номером карты или счёта, возвращаем замаскированный результат."""
    # Проверка на пустую строку
    if not date or not date.strip():
        raise ValueError("Входная строка не может быть пустой")

    # Разделение строки на тип и номер
    parts = date.rsplit(sep=' ', maxsplit=1)

    # Проверка, что получилось ровно две части
    if len(parts) != 2:
        raise ValueError(f"Некорректный формат входной строки: '{date}'. Ожидаемый формат: 'Тип Номер'")

    name, number = parts

    # Приведение типа к нижнему регистру и удаление лишних пробелов
    account_type = name.lower().strip()

    if account_type in ('счёт', 'счет'):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f'{name} {masked_number}'

