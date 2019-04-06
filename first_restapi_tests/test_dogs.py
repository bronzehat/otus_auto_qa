"""
These tests are for dog breed site
(https://dog.ceo/api/breeds/list/all)
"""
import pytest
import requests

ENTRIES = ["s/image/random", "s/list/all", "/hound/images", "/hound/list"]
@pytest.mark.parametrize("entry", ENTRIES)
def test_dog_breeds_ok(entry, dogs):
    """
    :param entry: element from list of entries in parametrize mark
    :param dogs: base URL for requests
    :return: asserts if status_code is 200 and json's
    "status" key value is success
    """
    responce = requests.get(dogs + entry)
    assert responce.status_code == 200
    assert responce.json()["status"] == "success"

def test_count_dog_breeds(dogs):
    """
    :param dogs: base URL for requests
    :return: prints number of breeds,
    asserts if length is > 0
    """
    responce = requests.get(dogs + "s/list/all")
    rson = responce.json()
    breeds = rson["message"].keys()
    print("Number of all dog breeds at the resource: " + str(len(breeds)))
    count = len(breeds)
    assert count > 0

@pytest.mark.timeout(80)
@pytest.mark.slow
def test_no_breed_without_images(dogs):
    """
    Tests that there are images for every breed
    :param dogs:
    :return:
    """
    print("Count of images for every breed:")
    responce_all = requests.get(dogs + "s/list/all")
    r_all = list(responce_all.json()["message"].keys())
    dict_breeds = {}
    for i in r_all:
        responce = requests.get(dogs + "/" + i + "/images")
        rson = responce.json()["message"]
        dict_breeds[i] = len(rson)
        count = len(rson)
        assert count > 0
    print("", dict_breeds)
