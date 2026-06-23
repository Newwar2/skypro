import logging
from pathlib import Path

current_file = Path(__file__)
project_root = current_file.parent.parent
log_dir = project_root / "logs"
log_dir.mkdir(exist_ok=True)

log_file = log_dir / "masks.log"  # путь до папки
logger_masks = logging.getLogger("masks")
logger_masks.setLevel(logging.DEBUG)

masks_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")  # log_file путь до файла
masks_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s %(funcName)s %(levelname)s: %(message)s")
masks_handler.setFormatter(file_formatter)
logger_masks.addHandler(masks_handler)
logger_masks.propagate = False


def get_mask_card_number(card: str) -> str:
    """Функция скрытие номера карты"""
    logger_masks.debug("Функция скрытие номера карты запустилась")
    if len(card) < 16:
        logger_masks.warning("Функция скрытие номера карты отработала с ошибкой")
        return "Некорректный номер карты"
    else:
        logger_masks.debug("Функция скрытие номера карты отработала корректно")
        return f"{card[:-12]} {card[-12:-10]}** **** {card[-4:]}"


def get_mask_account(account: str) -> str:
    """Функция скрытия номера счета"""
    logger_masks.debug("Функция скрытие номера счета запустилась")
    if len(account) < 4:
        logger_masks.warning("Функция скрытие номера счета отработала с ошибкой")
        return "Некорректный номер счета"
    else:
        logger_masks.debug("Функция скрытие номера счета отработала корректно")
        return f"**{account[-4:]}"
