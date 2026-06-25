import os

import pytest

from config import ROOT_DIR
from src.decorators import log


@log()
def add(a, b):
    return a + b


@log("file.log")
def add_(a, b):
    return a + b


def test_file_log():
    add_(a=1, b=2)
    file_name = f"{ROOT_DIR}//logs//file.log"
    with open(file_name, "r", encoding="utf-8") as f:
        data = f.read()
        assert "add_ ok" in data
    os.remove(file_name)


def test_log_success(capsys):
    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert "add ok\n" in captured.out


@log()
def fail_function():
    raise ValueError("Invalid input")


def test_log_error(capsys):
    with pytest.raises(ValueError, match="Invalid input"):
        fail_function()

    captured = capsys.readouterr()
    # Проверяем формат сообщения
    assert "fail_function: Invalid input." in captured.out or "fail_function" in captured.err
