"""
These tests are for testing functions in ../src/numbers_ops.py file
"""

import first_simple_pytests.src.numbers_ops as numbers_ops

def test_numbers_isint():
    """
    check if the number's type is int
    :return: True if the number's type is int. if not - returns False
    """

    isint_result = numbers_ops.numbers_isint(4)
    assert isint_result is True

def test_numbers_max():
    """
    find the maximum of 2 numbers
    :return: the maximum of 2 given numbers
    """

    max_result = numbers_ops.numbers_max(100, 564)
    assert max_result == 564

def test_numbers_func():
    """
    find the result of the function
    :return: the result of the funxtion (((x ** 2) - (x + 2)) * 2) where x is the given number
    """
    func_result = numbers_ops.numbers_func(2)
    assert func_result == 0
