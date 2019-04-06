"""
These tests are for the site with breweries
(https://api.openbrewerydb.org/breweries)
"""


import pytest
import requests


STATES = ["new_york", "california", "arizona", "alabama", "ohio"]
ENDINGS = ["city=rome", "name=cooper", "state=new_york", "type=micro",
           "tag=patio", "tags="]
NAMES = ["dog", "cooper", "sisters"]
SEARCH_PARAMS = ["dog", "cat", "fish"]


@pytest.mark.parametrize("state", STATES)
def test_brew_count_by_state(brew, state):
    """
    Checks how many breweries are in each of the given states
    :param brew: base URL of the site
    :param state: list of given states is in parametrize mark
    :return:
    """
    responce = requests.get(brew + "?by_state=" + state)
    rson = responce.json()
    # print(state + " breweries count: " + str(len(rson)))
    count = len(rson)
    assert count

@pytest.mark.parametrize("ending", ENDINGS)
def test_filter_pages(brew, ending):
    """
    Tests if all filters given in documentation are available
    :param brew: base URL from fizture
    :param ending: URL ending for each filter given in parametrize mark
    :return: asserts status code is 200
    """
    responce = requests.get(brew + "?by_" + ending)
    assert responce.status_code == 200


@pytest.mark.parametrize("name", NAMES)
def test_find_name_give_id(brew, name):
    """
    Tests search by different names
    :param brew: base URL from a fixture
    :param name: list of names for search
    :return: list of id for each name
    """
    responce = requests.get(brew + "/autocomplete?query=" + name)
    rson = responce.json()
    list_ids = []
    for i in rson:
        list_ids.append(i["id"])
    print('"' + name + '" named ids: ' + str(list_ids))


@pytest.mark.parametrize("search", SEARCH_PARAMS)
def test_search_animals(brew, search):
    """
    Searches by the given animal types and counts results
    :param brew: base URL for a fixture
    :param search: list of words from parametrize mark
    :return: prints count of results for each name
    """
    responce = requests.get(brew + "/search?query=" + search)
    rson = responce.json()
    print('"' + search + '" search parameter\'s results count: ' + str(len(rson)))
    count = len(rson)
    assert count > 0
