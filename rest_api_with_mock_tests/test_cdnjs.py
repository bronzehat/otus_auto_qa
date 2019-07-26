"""
These tests are for cdnjs site
"""
import pytest

ENTRIES = ["", "/academicons", "/academicons?output=human",
           "/?search=[bootstrap]", "/?search=[bootstrap]&fields=assets"]
SEARCHES = ["bootstrap", "alert"]
FIELDS = ["version", "description", "homepage", "keywords", "license",
          "repository", "autoupdate", "author", "assets"]

@pytest.mark.parametrize("entry", ENTRIES)
def test_cdnjs_entries_ok(entry, cdnjs):
    """
    Tests if different endings from documentation work
    (status code 200)
    :param entry: a list of endings from parametrize mark
    :param cdnjs: base URL from a fixture
    :return: asserts if page status code is 200
    """
    assert cdnjs.get_responce_code_by_entry() == 200

@pytest.mark.parametrize("search", SEARCHES)
def test_search(cdnjs, search):
    """
    Tests searches with params from a given list
    :param cdnjs: base URL from a fixture
    :param search: list of params from parametrize mark
    :return: prints search results count for each param
    """
    print("Total of {} : ".format(search, cdnjs.search_by_text()[search]))

@pytest.mark.parametrize("field", FIELDS)
def test_search_results_matchnumber(cdnjs, field):
    """
    Tests if a search page with different fields to show
    gives an equal number of objects
    :param cdnjs: base URL from a fixture
    :param field: list of fields to show from parametrize mark
    :return: asserts if length of
    """
    matchnumber = set()
    matchnumber.add(cdnjs.match_number_by_field()[field])
    count = len(matchnumber)
    assert count == 1
