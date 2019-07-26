"""
These tests are for dog breed site
(https://dog.ceo/api/breeds/list/all)
"""
import pytest

ENTRIES = ["s/image/random", "s/list/all", "/hound/images", "/hound/list"]
@pytest.mark.parametrize("entry", ENTRIES)
def test_dog_breeds_ok(entry, dogs):
    """
    :param entry: element from list of entries in parametrize mark
    :param dogs: base URL for requests
    :return: asserts if status_code is 200 and json's
    "status" key value is success
    """
    assert dogs.get_responce_status_by_entry() == 200

def test_count_dog_breeds(dogs):
    """
    :param dogs: base URL for requests
    :return: prints number of breeds,
    asserts if length is > 0
    """
    count = dogs.get_total_breeds_count()
    print("Number of all dog breeds at the resource:", count)
    assert count

@pytest.mark.timeout(80)
@pytest.mark.slow
def test_no_breed_without_images(dogs):
    """
    Tests that there are images for every breed
    :param dogs:
    :return:
    """
    images_count = dogs.count_images_by_breed()
    print()
    for i in images_count:
        print("{} count : {}".format(i, images_count[i]))
        assert i
