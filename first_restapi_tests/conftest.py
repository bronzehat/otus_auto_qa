"""
Here are fixtures used in first_restapi_tests
"""

import pytest


@pytest.fixture(params=["https://dog.ceo/api/breeds/list/all",
                        "https://api.openbrewerydb.org/breweries",
                        "https://api.cdnjs.com/libraries"],
                ids=["dogs", "breweries", "cdnjs"])
def base_url(request):
    """
    Gives a list of given URLs for test
    :param request:
    :return: returns a list of given URLs for test
    """
    return request.param


@pytest.fixture(params=["https://api.openbrewerydb.org/breweries"], ids=["breweries"])
def brew(request):
    """
    Allows to use in tests a single word instead of the whole url
    :param request:
    :return:
    """
    return request.param


@pytest.fixture(params=["https://dog.ceo/api/breed"], ids=["breed"])
def dogs(request):
    """
    Allows to use in tests a single word instead of the whole url
    :param request:
    :return:
    """
    return request.param


@pytest.fixture(params=["https://api.cdnjs.com/libraries"], ids=["cdnjs"])
def cdnjs(request):
    """
    Allows to use in tests a single word instead of the whole url
    :param request:
    :return:
    """
    return request.param


def pytest_addoption(parser):
    """
    Adds a commandline option "--runslow" to include slow tests in current execution
    :param parser:
    :return:
    """
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Gives any test a default timeout if it doesn't already exist.
    Also here is the code for pytest-addoption "--runslow" given earlier. Allows to run slow tests
    only if this option is used
    :param config: means cmd
    :param items: here - test functions
    :return:
    """
    for item in items:
        if item.get_closest_marker('timeout') is None:
            item.add_marker(pytest.mark.timeout(10))

    if config.getoption("--runslow"):
        # --runslow given in cli: run slow tests too
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


"""
********************************************
This is an attempt to integrate argparse to the tests (I could not)
Help to find a mistake please!
There is a test in test_parse.py
"""
# import argparse
#
# parser = argparse.ArgumentParser()
# parser.add_argument("-address", action="store", dest="address", help="run test for certain URL",
#                         default="http://ya.ru")
# args = parser.parse_args()
# url = args.address
#
#
# @pytest.fixture
# def parsing():
#     if url:
#         return url

"""
The end of argparse problem code
********************************************
"""
