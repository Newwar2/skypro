import pytest
from src.decorators import log


@log()
def add(a, b):
    return a + b


def test_log_success(capsys):
    result = add(2, 3)

    captured = capsys.readouterr()

    assert result == 5
    assert "add ok" in captured.out


@log()
def fail_function():
    raise ValueError("Invalid input")


def test_log_error(capsys):
    with pytest.raises(ValueError):
        fail_function()

    captured = capsys.readouterr()

    assert "fail_function error: ValueError" in captured.out
