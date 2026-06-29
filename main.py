# from src.masks import get_mask_account, get_mask_card_number
# # from src.utils import transactions_csv, transactions_excel
# from src.widget import mask_account_card
#
# if __name__ == "__main__":
#     # result_1 = transactions_csv("data/transactions.csv")
#     # print(result_1)
#
#     # result_2 = transactions_excel("data/transactions_excel.xlsx")
#     # print(result_2)
#
#     print(mask_account_card("Maestro 1596837868705199"))
#     print(mask_account_card("Счет 64686473678894779589"))
#     print(mask_account_card("MasterCard 7158300734726758"))
#     print(mask_account_card("Visa Classic 6831982476737658"))
#     print(mask_account_card("Visa Platinum 8990922113665229"))
#     print(mask_account_card("Visa Gold 5999414228426353"))
#     print(mask_account_card("Счет 73654108430135874305"))
#     print(get_mask_card_number("0111123412341234"))
#     print(get_mask_account("73654108430135874305"))

import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.utils import read_json, conversion, transactions_csv, transactions_excel

# Если filter_by_status и другие фильтры нужны — импортируй из src.transactions
# from src.transactions import filter_by_status, process_bank_search, count_operations_by_category

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}

logger = __import__("logging").getLogger("utils")  # используем логгер из utils (там уже настроен)


def get_valid_status() -> str:
    """Запрашивает у пользователя корректный статус из VALID_STATUSES."""
    while True:
        user_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные статусы: {', '.join(sorted(VALID_STATUSES))}\n> "
        ).strip()

        if not user_input:
            print("Статус не может быть пустым. Попробуйте снова.")
            continue

        normalized = user_input.upper()
        if normalized in VALID_STATUSES:
            return normalized
        else:
            print(f'Статус операции "{user_input}" недоступен. Попробуйте ещё раз.')


def ask_yes_no(question: str) -> bool:
    """Спрашивает Да/Нет, принимает разные варианты ввода."""
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        elif answer in ("нет", "н", "no", "n"):
            return False
        else:
            print("Пожалуйста, ответьте «да» или «нет».")


def parse_date(date_str: Any) -> Optional[datetime]:
    """Пытается распарсить дату из строки в нескольких форматах."""
    if not date_str:
        return None

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


def sort_transactions(
        data: List[Dict[str, Any]],
        ascending: bool
) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате. Если дата невалидна — относит к самому старому."""

    def key_func(item: Dict[str, Any]) -> datetime:
        dt = parse_date(item.get("date"))
        return dt if dt is not None else datetime.min

    return sorted(data, key=key_func, reverse=not ascending)


def filter_rub_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Оставляет только RUB-транзакции (по полю currency)."""
    result: List[Dict[str, Any]] = []
    for item in data:
        currency = (item.get("currency") or "").strip().upper()
        if currency == "RUB":
            result.append(item)
    return result


def filter_by_description(
        data: List[Dict[str, Any]],
        search_word: str
) -> List[Dict[str, Any]]:
    """Фильтрует по подстроке в description (регистронезависимо)."""
    search = search_word.lower()
    result: List[Dict[str, Any]] = []
    for item in data:
        desc = (item.get("description") or "").lower()
        if search in desc:
            result.append(item)
    return result


def convert_to_rub(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Конвертирует суммы всех транзакций в рубли с помощью conversion()."""
    converted: List[Dict[str, Any]] = []
    for tx in data:
        # Создаём копию, чтобы не менять оригинал
        tx_copy = dict(tx)
        try:
            tx_copy["amount_rub"] = conversion(tx)
            converted.append(tx_copy)
        except Exception as e:
            logger.exception("Ошибка конвертации транзакции: %s", e)
            # Пропускаем или оставляем как есть — на твой выбор. Сейчас пропускаем.
            continue
    return converted


def format_amount(amount: Any, currency: Any) -> str:
    try:
        amt = float(amount)
    except (TypeError, ValueError):
        amt = amount

    cur = (currency or "").strip()
    if not cur:
        return f"Сумма: {amt}"
    return f"Сумма: {amt} {cur}"


def print_transactions(data: List[Dict[str, Any]]) -> None:
    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print(f"\nВсего банковских операций в выборке: {len(data)}\n")
    for op in data:
        date_val = op.get("date") or ""
        description = op.get("description", "Нет описания")
        amount = op.get("amount")
        currency = op.get("currency")

        if date_val:
            dt = parse_date(date_val)
            if dt:
                date_str = dt.strftime("%d.%m.%Y")
            else:
                date_str = str(date_val)
        else:
            date_str = ""

        line_1 = f"{date_str} {description}".strip()
        print(line_1)

        details = op.get("details")
        if details:
            print(details)

        # Если есть конвертированная сумма — показываем её
        if "amount_rub" in op:
            print(format_amount(op["amount_rub"], "RUB"))
        else:
            print(format_amount(amount, currency))
        print()


def load_data_by_choice(choice: str, file_path: str) -> List[Dict[str, Any]]:
    if choice == "1":
        # JSON: путь относительный или абсолютный, read_json ожидает полный путь
        return read_json(file_path)
    elif choice == "2":
        return transactions_csv(file_path)
    elif choice == "3":
        return transactions_excel(file_path)
    else:
        raise ValueError("Неверный выбор типа файла")


def main() -> None:
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    print("> ", end="")

    choice = input().strip()

    load_functions_info = {
        "1": "JSON-файл",
        "2": "CSV-файл",
        "3": "XLSX-файл",
    }

    if choice not in load_functions_info:
        print("Ошибка: выбран неверный пункт меню. Запустите программу заново.")
        sys.exit(1)

    file_type = load_functions_info[choice]
    print(f"Программа: Для обработки выбран {file_type}.")

    file_path = input("Пожалуйста, введите путь к файлу: ").strip()
    if not file_path:
        print("Ошибка: путь к файлу не может быть пустым.")
        sys.exit(1)

    try:
        data = load_data_by_choice(choice, file_path)
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        sys.exit(1)

    if not data:
        print("Предупреждение: файл прочитан, но транзакций не найдено.")
        return

    logger.info("Загружено транзакций: %d", len(data))

    # 1. Фильтр по статусу
    status = get_valid_status()
    print(f'Программа: Операции отфильтрованы по статусу "{status}".')
    # Здесь можно подключить filter_by_status из transactions.py, если нужно
    # filtered = filter_by_status(data, status)
    filtered = [tx for tx in data if tx.get("status", "").upper() == status]

    if not filtered:
        print("Программа: Не найдено ни одной транзакции с указанным статусом.")
        return

    # 2. Сортировка по дате
    sort_by_date = ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\n> ")
    if sort_by_date:
        order = input("Программа: Сортировать по возрастанию или по убыванию?\n> ").strip().lower()
        ascending = order in ("возрастанию", "asc", "по возрастанию", "вверх")
        filtered = sort_transactions(filtered, ascending)

    # 3. Только RUB
    rub_only = ask_yes_no("Программа: Выводить только рублёвые транзакции? Да/Нет\n> ")
    if rub_only:
        filtered = filter_rub_only(filtered)

    # 4. Поиск по описанию
    search_desc = ask_yes_no(
        "Программа: Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n> "
    )
    if search_desc:
        word = input("Введите слово для поиска в описании:\n> ").strip()
        if word:
            filtered = filter_by_description(filtered, word)

    # 5. Конвертация в RUB (если не отфильтровали только RUB)
    # Если пользователь выбрал «только RUB», конвертация всё равно может быть полезна,
    # если в данных есть RUB, но хочется унифицировать поле суммы.
    convert = ask_yes_no(
        "Программа: Конвертировать суммы всех транзакций в рубли (с использованием API курсов)? Да/Нет\n> "
    )
    if convert:
        filtered = convert_to_rub(filtered)

    print("Программа: Распечатываю итоговый список транзакций...\n")
    print_transactions(filtered)


if __name__ == "__main__":
    main()