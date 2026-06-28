import re
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Функция, которая будет принимать список словарей с данными о банковских операциях и
    строку поиска, а возвращать список словарей, у которых в описании есть данная строка"""

    if not search:
        return data

    # Компилируем регулярное выражение с флагом IGNORECASE (регистронезависимо)
    pattern = re.compile(
        search, re.IGNORECASE
    )  # Cоздаёт объект паттерна,чтобы постоянно не писать search,re.IGNORECASE

    result = []
    for operation in data:
        description = operation.get(
            "description", ""
        )  # Безопасное получение поля: если ключа "description" нет, вернётся пустая строка, а не ошибка KeyError
        # Проверяем, есть ли совпадение
        if pattern.search(description):
            result.append(operation)

    return result


def count_operations_by_category(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Функция, которая будет принимать список словарей с данными о банковских операциях и список категорий операций,
    а возвращать словарь, в котором ключи — это названия категорий, а значения — это количество операций в каждой
    категории, где param data - список словарей с данными об операцияхб param categories - список названий категорий
    для подсчёта.
    """
    result = {category: 0 for category in categories}

    for operation in data:
        description = (operation.get("description") or "").lower()
        for category in categories:
            if category.lower() in description:  # Ищем частичное совпадение категории в описании (регистронезависимо)
                result[category] += 1
                break

    return result
