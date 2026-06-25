from functools import wraps
from typing import Any, Callable

from config import ROOT_DIR


def log(filename: str | None = None) -> Callable:
    """Декоратор log, автоматически логирует начало и конец выполнения функции, ее результаты и возникшие ошибки."""

    def decarator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            mes = ""
            try:
                result = func(*args, **kwargs)
                mes = f"{func.__name__} ok\n"
                return result
            except Exception as err:
                mes = f"{func.__name__}: {err}. Inputs: {args}, {kwargs}\n"
                raise
            finally:
                if filename:
                    with open(f"{ROOT_DIR}//logs//{filename}", "a", encoding="utf-8") as file:
                        file.write(mes)
                else:
                    print(mes)

        return wrapper

    return decarator
