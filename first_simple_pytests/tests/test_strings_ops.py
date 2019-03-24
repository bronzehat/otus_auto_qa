import first_simple_pytests.src.strings_ops as strings_ops

# 2 strings' concatenation
def test_strings_concat():
    concat_result = strings_ops.strings_concat("su", "per")
    assert concat_result == "super"

# find common symbols in 2 strings
def test_strings_common_symbols():
    common_result = strings_ops.strings_common_symbols("hi", "hello")
    assert common_result == "h"

# if the 1st symbol in 2 strings match, it should be returned
def test_strings_first_symbol():
    first_result = strings_ops.strings_first_symbol("otus", "october")
    assert first_result == "o"
