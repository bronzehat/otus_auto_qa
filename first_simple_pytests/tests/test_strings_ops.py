"""
These tests are for testing functions in ../src/strings_ops.py file
"""

import first_simple_pytests.src.strings_ops as strings_ops

def test_strings_concat():
    """
    2 strings' concatenation
    :return: a string made of 2 given strings' concatenation
    """

    concat_result = strings_ops.strings_concat("su", "per")
    assert concat_result == "super"

def test_strings_common_symbols():
    """
    find common symbols in 2 strings
    :return: the symbol that is in both given strings
    """

    common_result = strings_ops.strings_common_symbols("hi", "hello")
    assert common_result == "h"

def test_strings_first_symbol():
    """
    if the 1st symbol in 2 strings match (no matter of uppercase or lowercase),
    True should be returned
    :return: True oif the 1st symbol in both strings matches, if not - returns False
    """

    first_result = strings_ops.strings_first_symbol("Otus", "october")
    assert first_result is True
