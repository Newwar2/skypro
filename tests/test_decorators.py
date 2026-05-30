import pytest
import os
from src.decorators import log

@log()
def test_log(a, b):
    return a + b


@log()
def test_log(a, b):
    raise ValueError("Invalid input")

