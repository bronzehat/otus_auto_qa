import strings_ops
import pytest

def test_strings_concat():
    concat_result = strings_ops.strings_concat("su", "per")
    assert concat_result == "super"

def test_strings_common_symbols():
    common_result = strings_ops.strings_common_symbols("hi", "hello")
    assert common_result == "h"

def test_strings_first_symbol():
    first_result = strings_ops.strings_first_symbol("otus", "october")
    assert first_result == "o"