"""
These tests are for the site with breweries
(https://api.openbrewerydb.org/breweries)
"""


import pytest


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
    count = brew.get_count_by_state()[state]
    print(count)
    assert count

@pytest.mark.parametrize("ending", ENDINGS)
def test_brew_filter_pages(brew, ending):
    """
    Tests if all filters given in documentation are available
    :param brew: base URL from fizture
    :param ending: URL ending for each filter given in parametrize mark
    :return: asserts status code is 200
    """
    assert brew.get_responce_status_by_endings() == 200

@pytest.mark.parametrize("name", NAMES)
def test_brew_find_name_give_id(brew, name):
    """
    Tests search by different names
    :param brew: base URL from a fixture
    :param name: list of names for search
    :return: list of id for each name
    """
    print('{} named ids: {}'.format(name, brew.get_id_by_name()[name]))

@pytest.mark.brew
@pytest.mark.parametrize("search", SEARCH_PARAMS)
def test_brew_search_animals(brew, search):
    """
    Searches by the given animal types and counts results
    :param brew: base URL for a fixture
    :param search: list of words from parametrize mark
    :return: prints count of results for each name
    """
    print("{} count : {}".format(search, brew.search_animals()[search]))
