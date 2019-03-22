import dicts_opa
import pytest

def test_dicts_contain_value():
    contain_result = dicts_opa.dicts_contain_value({0: "zero", 1: "one"}, "one")
    assert contain_result == "one"

def test_dicts_contain_key_modify():
    contain_modify_result = dicts_opa.dicts_contain_key_modify({"name": "Alexi", "surname": "Liho"}, "surname")
    assert contain_modify_result == None