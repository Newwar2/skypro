import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config import ROOT_DIR
from src.external_api import operation

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "utils.log"  # путь до папки
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)

utils_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")  # log_file путь до файла
utils_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s %(funcName)s %(levelname)s: %(message)s")
utils_handler.setFormatter(file_formatter)
logger_utils.addHandler(utils_handler)
logger_utils.propagate = False


def read_json(path_json: str) -> Any:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях."""
    logger_utils.debug("Функция read_json, которая принимает на вход путь до JSON-файла - запустилась.")
    try:
        logger_utils.info("Попытка открыть и прочитать JSON-файл.")
        with open(path_json) as file:
            data = json.load(file)
            logger_utils.info("JSON-файл успешно прочитан.")
    except FileNotFoundError:
        logger_utils.error("Файл не найден. Возвращается пустой список.")
        data = []
    except JSONDecodeError:
        logger_utils.error("Ошибка декодирования JSON в файле. Возвращается пустой список.")
        data = []

    return data


def conversion(transaction: dict) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях."""
    logger_utils.debug("Функция convertetion запущена, начинаем обработку транзакций")
    code: str = transaction["operationAmount"]["currency"]["code"]  # показывает, что используется другая валюта
    logger_utils.info("Определён код валюты")
    rub_pay: float = float(transaction["operationAmount"]["amount"])
    logger_utils.info("Сумма в исходной валюте")
    if code == "RUB":
        logger_utils.info("Валюта уже в рублях, конвертация не требуется. Возвращаем сумму rub_pay")
        return rub_pay
    else:
        logger_utils.info("Требуется конвертация")
        kurs: float = round(operation(code))
        logger_utils.info("Получен курс для code, kurs")
        result: float = rub_pay * kurs
        logger_utils.info("Конвертация выполнена")
        return result


def transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    # 1. Превращаем строку пути в удобный объект Path
    file_path = f"{ROOT_DIR}//{file_path}"
    path = Path(file_path)

    # 2. Проверяем: существует ли файл и является ли он файлом (а не папкой)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # 3. Пробуем прочитать файл. Сначала UTF-8, если не вышло — пробуем CP1251 (для русских файлов)
    try:
        df = pd.read_csv(path, encoding="utf-8", delimiter=";")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp1251", delimiter=";")

    # 4. Превращаем таблицу в список словарей и возвращаем
    return df.to_dict(orient="records")


def transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    # 1. Превращаем строку пути в удобный объект Path
    file_path = f"{ROOT_DIR}//{file_path}"
    path = Path(file_path)

    # 2. Проверяем: существует ли файл и является ли он файлом (а не папкой)
    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # 3. Пробуем прочитать файл.
    df = pd.read_excel(path)

    # 4. Превращаем таблицу в список словарей и возвращаем
    return df.to_dict(orient="records")
