"""
Here are fixtures used in first_restapi_tests
"""
import pytest


URLS = ["https://dog.ceo/api/breeds/list/all",
        "https://api.openbrewerydb.org/breweries",
        "https://api.cdnjs.com/libraries"]


@pytest.fixture
def url(request):
    """
    Gives a list of given URLs for test
    :param request:
    :return: returns a list of given URLs for test
    """
    result = []
    parameter = request.config.getoption("--url")
    if parameter == "all":
        result = URLS
    elif parameter == "dogs":
        result = URLS[0]
    elif parameter == "brew":
        result = URLS[1]
    elif parameter == "cdnjs":
        result = URLS[2]
    else:
        print("No suitable URL! Print 'all' or dogs of brew or cdnjs")
        pytest.xfail("No suitable URL")
    return result


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
    parser.addoption(
        "--url", action="store", dest="url", type=str, help="choose one of given addresses or all"
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
