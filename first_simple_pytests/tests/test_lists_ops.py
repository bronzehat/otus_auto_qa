"""
These tests are for testing functions in ../src/lists_ops.py file
"""

import first_simple_pytests.src.lists_ops as lists_ops

def test_lists_append():
    """
    adds numbers in range of the given number to the list
    :return: the list of elements in range of the given number (0..x)
    """

    append_resuls = lists_ops.lists_append(8)
    assert append_resuls == [0, 1, 2, 3, 4, 5, 6, 7]

def test_lists_length():
    """
    :return: returns the length of the given list
    """

    length_result = lists_ops.lists_length(["element"])
    assert length_result == 1

def test_lists_reverse():
    """
    reverses the given list
    :return: the reversed version of the given list
    """

    reverse_result = lists_ops.lists_reverse([0, 1, 2])
    assert reverse_result == [2, 1, 0]
