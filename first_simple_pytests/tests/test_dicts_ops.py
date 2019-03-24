import first_simple_pytests.src.dicts_ops as dicts_ops

# check if value is in the dict
def test_dicts_contain_value():
    contain_result = dicts_ops.dicts_contain_value({0: "zero", 1: "one"}, "one")
    assert contain_result == "one"

# modify key in dict
def test_dicts_contain_key_modify():
    contain_modify_result = dicts_ops.dicts_contain_key_modify({"name": "Alexi", "surname": "Liho"}, "surname")
    assert contain_modify_result == None
