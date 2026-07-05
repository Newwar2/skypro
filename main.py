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
from pathlib import Path
from typing import Any, Dict, List, Optional

import logging

from mypy.state import state

from src.utils import read_json, conversion, transactions_csv, transactions_excel
from src.transactions import process_bank_search, count_operations_by_category, filter_rub_only
VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}

# Используем тот же логгер, что и в utils (чтобы все логи были в одном файле)
logger = logging.getLogger("utils")


def get_valid_status() -> str:
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
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        elif answer in ("нет", "н", "no", "n"):
            return False
        else:
            print("Пожалуйста, ответьте «да» или «нет».")


def parse_date(date_str: Any) -> Optional[datetime]:
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
    def key_func(item: Dict[str, Any]) -> datetime:
        dt = parse_date(item.get("date"))
        return dt if dt is not None else datetime.min

    return sorted(data, key=key_func, reverse=not ascending)


def filter_rub_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for item in data:
        currency = (item.get("currency_code") or "").strip().upper()
        if currency == "RUB":
            result.append(item)
    return result


def filter_by_description(
        data: List[Dict[str, Any]],
        search_word: str
) -> List[Dict[str, Any]]:
    search = search_word.lower()
    result: List[Dict[str, Any]] = []
    for item in data:
        desc = (item.get("description") or "").lower()
        if search in desc:
            result.append(item)
    return result


def convert_to_rub(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    converted: List[Dict[str, Any]] = []
    for tx in data:
        tx_copy = dict(tx)
        try:
            tx_copy["amount_rub"] = conversion(tx)
            converted.append(tx_copy)
        except Exception as e:
            logger.exception("Ошибка конвертации транзакции: %s", e)
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

        if "amount_rub" in op:
            print(format_amount(op["amount_rub"], "RUB"))
        else:
            print(format_amount(amount, currency))
        print()


def load_data_by_choice(choice: str, file_path_raw: str) -> List[Dict[str, Any]]:
    path = Path(file_path_raw).resolve()
    print(path)
    logger.info("Попытка загрузки данных. Тип: %s, абсолютный путь: %s", choice, path)

    if not path.exists():
        logger.error("Файл не найден по абсолютному пути: %s", path)
        raise FileNotFoundError(f"Файл не найден: {path}")

    if path.is_dir():
        logger.error("Указан каталог вместо файла: %s", path)
        raise ValueError("Путь должен указывать на файл, а не на директорию.")

    try:
        if choice == "1":
            data = read_json(str(path))
        elif choice == "2":
            data = transactions_csv(str(path))
        elif choice == "3":
            data = transactions_excel(str(path))
        else:
            raise ValueError("Неверный выбор типа файла")

        logger.info("Файл успешно прочитан. Загружено транзакций: %d", len(data))
        return data
    except Exception as e:
        logger.exception("Критическая ошибка при чтении файла: %s", e)
        raise


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
        print(f"Ошибка: файл не найден. Проверьте путь и попробуйте снова.\nДетали: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в параметрах: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        sys.exit(1)

    if not data:
        # Это не обязательно ошибка: файл может быть валидным, но пустым
        logger.warning("Файл прочитан, но список транзакций пуст.")
        print("Предупреждение: файл прочитан, но транзакций не найдено.")
        return

    logger.info("Загружено транзакций: %d", len(data))

    # 1. Фильтр по статусу
    user_state = get_valid_status()
    print(f'Программа: Операции отфильтрованы по статусу "{user_state}".')
    filtered = [tx for tx in data if str(tx.get("state", "")).upper() == user_state]
    logger.info("После фильтра по статусу осталось транзакций: %d", len(filtered))
    if not filtered:
        print("Программа: После фильтрации по статусу список пуст. Дальнейшие фильтры не имеют смысла.")
        return

    # 2. Поиск по описанию
    search_desc = ask_yes_no(
        "Программа: Отфильтровать список транзакций по определённому слову/фразе в описании? Да/Нет\n> ")
    if search_desc:
        word = input("Введите слово или регулярное выражение для поиска в описании:\n> ").strip()
        if word:
            filtered = process_bank_search(filtered, word)
            logger.info("После поиска по описанию осталось транзакций: %d", len(filtered))

    # 3. Только RUB
    rub_only = ask_yes_no("Программа: Выводить только рублёвые транзакции? Да/Нет\n> ")
    if rub_only:
        filtered = filter_rub_only(filtered)
        logger.info("После фильтрации RUB осталось транзакций: %d", len(filtered))
        if not filtered:
            print("Программа: После фильтрации RUB список пуст.")
            # Можно сразу выйти, чтобы не делать лишние шаги
            # return

    # 4. Сортировка по дате
    sort_by_date = ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\n> ")
    if sort_by_date:
        order = input("Программа: Сортировать по возрастанию или по убыванию?\n> ").strip().lower()
        ascending = order in ("возрастанию", "asc", "по возрастанию", "вверх")
        filtered = sort_transactions(filtered, ascending)
        logger.info("После сортировки осталось транзакций: %d", len(filtered))

    # 5. Подсчёт категорий
    count_by_cat = ask_yes_no(
        "Программа: Подсчитать количество операций по заданным категориям? Да/Нет\n> "
    )
    if count_by_cat:
        cats_input = input("Введите названия категорий через запятую:\n> ").strip()
        categories = [c.strip() for c in cats_input.split(",") if c.strip()]
        if categories:
            counts = count_operations_by_category(filtered, categories)
            print("\n--- Подсчёт операций по категориям ---")
            for cat, cnt in counts.items():
                print(f"{cat}: {cnt}")
            print("-------------------------------------\n")

    # 6. Конвертация
    convert = ask_yes_no(
        "Программа: Конвертировать суммы всех транзакций в рубли (с использованием API курсов)? Да/Нет\n> "
    )
    if convert:
        filtered = convert_to_rub(filtered)
        logger.info("После конвертации осталось транзакций: %d", len(filtered))

    print("Программа: Распечатываю итоговый список транзакций...\n")
    print_transactions(filtered)

if __name__ == "__main__":
    main()