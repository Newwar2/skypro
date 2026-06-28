import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.transactions import filter_by_status, load_csv, load_json, load_xlsx

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def get_valid_status() -> str:
    """Запрашивает статус до корректного ввода."""
    prompt = (
        "Введите статус, по которому необходимо выполнить фильтрацию.\n"
        "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
        "> "
    )

    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Статус не может быть пустым. Попробуйте снова.")
            continue

        normalized = user_input.upper()
        if normalized in VALID_STATUSES:
            return normalized
        else:
            print(f'Статус операции "{user_input}" недоступен.')


def ask_yes_no(question: str) -> bool:
    """Универсальный запрос Да/Нет с нормализацией ввода."""
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        elif answer in ("нет", "н", "no", "n"):
            return False
        else:
            print("Пожалуйста, ответьте «да» или «нет».")


def parse_date(date_str: Any) -> Optional[datetime]:
    """
    Пытается распарсить дату из строки.
    Поддерживает распространённые форматы.
    Возвращает None, если не удалось.
    """
    if not date_str:
        return None

    # Приводим к строке и убираем лишнее
    date_str = str(date_str).strip()

    formats = [
        "%d.%m.%Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def sort_transactions(data: List[Dict[str, Any]], ascending: bool) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате (если поле date есть)."""

    def key_func(item: Dict[str, Any]) -> datetime:
        dt = parse_date(item.get("date"))
        # Если даты нет — ставим очень старое время, чтобы такие записи шли в конец
        return dt if dt is not None else datetime.min

    return sorted(data, key=key_func, reverse=not ascending)


def filter_rub_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только транзакции с валютой RUB (регистронезависимо)."""
    result = []
    for item in data:
        currency = (item.get("currency") or "").strip().upper()
        if currency == "RUB":
            result.append(item)
    return result


def filter_by_description(data: List[Dict[str, Any]], search_word: str) -> List[Dict[str, Any]]:
    """Фильтрует по подстроке в description (регистронезависимо)."""
    search = search_word.lower()
    result = []
    for item in data:
        desc = (item.get("description") or "").lower()
        if search in desc:
            result.append(item)
    return result


def format_amount(amount: Any, currency: Any) -> str:
    """Форматирует сумму и валюту для вывода."""
    try:
        amt = float(amount)
    except (TypeError, ValueError):
        amt = amount

    cur = (currency or "").strip()
    if not cur:
        return f"Сумма: {amt}"
    return f"Сумма: {amt} {cur}"


def print_transactions(data: List[Dict[str, Any]]) -> None:
    """Красиво печатает список транзакций."""
    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}\n")
    for op in data:
        date_val = op.get("date") or ""
        description = op.get("description", "Нет описания")
        amount = op.get("amount")
        currency = op.get("currency")

        # Дата
        if date_val:
            # Пытаемся привести к формату ДД.ММ.ГГГГ, если это дата
            dt = parse_date(date_val)
            if dt:
                date_str = dt.strftime("%d.%m.%Y")
            else:
                date_str = str(date_val)
        else:
            date_str = ""

        line_1 = f"{date_str} {description}".strip()
        print(line_1)

        # Детали счёта/карты (если есть)
        details = op.get("details")
        if details:
            print(details)

        # Сумма
        print(format_amount(amount, currency))
        print()  # пустая строка между операциями


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    print("> ", end="")

    choice = input().strip()

    load_functions = {
        "1": ("JSON-файл", load_json),
        "2": ("CSV-файл", load_csv),
        "3": ("XLSX-файл", load_xlsx),
    }

    if choice not in load_functions:
        print("Ошибка: выбран неверный пункт меню. Запустите программу заново.")
        sys.exit(1)

    file_type, load_func = load_functions[choice]
    print(f"Программа: Для обработки выбран {file_type}.")

    file_path = input("Пожалуйста, введите путь к файлу: ").strip()
    if not file_path:
        print("Ошибка: путь к файлу не может быть пустым.")
        sys.exit(1)

    try:
        data: List[Dict[str, Any]] = load_func(file_path)
    except FileNotFoundError:
        print(f"Ошибка: файл '{file_path}' не найден. Проверьте путь и попробуйте снова.")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        sys.exit(1)

    if not data:
        print("Предупреждение: файл прочитан, но транзакций не найдено.")
        return

    # 1. Фильтр по статусу
    status = get_valid_status()
    print(f'Программа: Операции отфильтрованы по статусу "{status}"')
    filtered = filter_by_status(data, status)

    if not filtered:
        print("Программа: Не найдено ни одной транзакции с указанным статусом.")
        return

    # 2. Сортировка по дате?
    sort_by_date = ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\n> ")
    if sort_by_date:
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        ascending = order in ("возрастанию", "asc", "по возрастанию", "вверх")
        filtered = sort_transactions(filtered, ascending)

    # 3. Только рублёвые?
    rub_only = ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\n> ")
    if rub_only:
        filtered = filter_rub_only(filtered)

    # 4. Поиск по слову в описании?
    search_desc = ask_yes_no(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n> "
    )
    if search_desc:
        word = input("Введите слово для поиска в описании:\n> ").strip()
        if word:
            filtered = filter_by_description(filtered, word)

    print("Программа: Распечатываю итоговый список транзакций...\n")
    print_transactions(filtered)
