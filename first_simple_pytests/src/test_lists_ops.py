import lists_ops
import pytest

def test_lists_append():
    append_resuls = lists_ops.lists_append(8)
    assert append_resuls == [0, 1, 2, 3, 4, 5, 6, 7]

def test_lists_length():
    length_result = lists_ops.lists_length(["element"])
    assert length_result == 1

def test_lists_reverse(l):
    reverse_result = lists_ops.lists_reverse([0, 1, 2])
    assert reverse_result == [2, 1, 0]
