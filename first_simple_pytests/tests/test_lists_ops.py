import first_simple_pytests.src.lists_ops as lists_ops

# adds numbers in range of the given number to the list
def test_lists_append():
    append_resuls = lists_ops.lists_append(8)
    assert append_resuls == [0, 1, 2, 3, 4, 5, 6, 7]

# returns the length of the given list
def test_lists_length():
    length_result = lists_ops.lists_length(["element"])
    assert length_result == 1

# reverses the given list
def test_lists_reverse():
    reverse_result = lists_ops.lists_reverse([0, 1, 2])
    assert reverse_result == [2, 1, 0]
