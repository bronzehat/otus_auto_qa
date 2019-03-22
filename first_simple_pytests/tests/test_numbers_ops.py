import numbers_ops
import pytest

def test_numbers_isint():
    isint_result = numbers_ops.numbers_isint(4)
    assert isint_result == True

def test_numbers_max():
    max_result = numbers_ops.numbers_max(100, 564)
    assert max_result == 564

def test_numbers_func():
    func_result = numbers_ops.numbers_func(2)
    assert func_result == 0