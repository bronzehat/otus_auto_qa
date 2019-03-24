"""
These tests are for testing functions in ../src/dicts_ops.py file
"""

import first_simple_pytests.src.dicts_ops as dicts_ops

def test_dicts_contain_value():
    """
    check if value is in the dict
    :return: True - if the value exists in the dictionary, if not - returns False
    """
    contain_result = dicts_ops.dicts_contain_value(
        {0: "zero", 1: "one"}, "one"
    )
    assert contain_result is True

def test_dicts_contain_key_modify():
    """
    modify key in dict
    :return: the new value (None) of the matching key
    """
    contain_modify_result = dicts_ops.dicts_contain_key_modify(
        {"name": "Louie", "surname": "C.K."}, "surname"
    )
    assert contain_modify_result is None
