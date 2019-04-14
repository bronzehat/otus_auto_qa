"""
This is the conftest for first_selenium_tests
Here are commandline options and fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions


def pytest_addoption(parser):
    """
    Adds a commandline option "--browser" to choose browser for tests
    :param parser:
    :return:
        """
    parser.addoption(
        "--browser", action="store", dest="browser", type=str,
        help="choose one of browsers (chrome, firefox or ie)"
        )
    parser.addoption(
        "--url", action="store", dest="url", type=str, default="http://localhost/opencart",
        help="print url for testing"
    )

@pytest.fixture
def chosen_browser(request):
    """
    Returns the webdriver depending on what browser was chosen with
    "--browser" commandline option
    :param request:
    :return:
    """
    parameter = request.config.getoption("--browser")
    if parameter == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
    elif parameter == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
    elif parameter == "ie":
        options = IeOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = webdriver.Ie(ie_options=options)
    # elif parameter == "ie":
    #
    else:
        print "No browser chosen! Choose chrome, firefox or ie"
        pytest.xfail("No browser chosen")
    driver.fullscreen_window()
    request.addfinalizer(driver.quit)
    return driver

@pytest.fixture
def base_url(request):
    """
    Sets the url for tests depending on value of commandline option "--url"
    :param request:
    :return: the value of commandline option "--url"
    """
    parameter = request.config.getoption("--url")
    return parameter
