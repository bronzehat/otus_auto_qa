"""
This is the conftest for first_selenium_tests
Here are commandline options and fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions

DEFAULT_IMPLICITLY_WAIT = 60


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
        "--city", action="store", dest="city", type=str, default="ufa",
        help="print city to find event"
    )
    parser.addoption(
        "--group", action="store", dest="group", type=str, default="Children of Bodom",
        help="print musicians to find event"
    )
    parser.addoption(
        "--implicit", action="store", dest="implicit", type=int, default=DEFAULT_IMPLICITLY_WAIT,
        help="manually define implicity wait for testing"
    )

@pytest.fixture(scope="session")
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
        driver = webdriver.Remote(command_executor="http://192.168.85.154:4446/wd/hub",
                                  desired_capabilities={
                                      "browsername":"chrome"},
                                  options=options)
    elif parameter == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = webdriver.Remote(command_executor="http://192.168.85.154:4446/wd/hub",
                                  desired_capabilities={
                                      "browsername":"firefox"},
                                  options=options)
    elif parameter == "ie":
        options = IeOptions()
        options.add_argument("--start-fullscreen")
        driver = webdriver.Ie(ie_options=options)
    else:
        print("No browser chosen! Choose chrome, firefox or ie")
        pytest.xfail("No browser chosen")
    implicit_timeout = request.config.getoption("--implicit")
    driver.implicitly_wait(implicit_timeout)
    driver.set_page_load_timeout(60)
    driver.desired_capabilities["unexpectedAlertBehavior"] = "dismiss"
    request.addfinalizer(driver.quit)
    return driver

@pytest.fixture
def city(request):
    return request.config.getoption("--city")

@pytest.fixture
def group(request):
    return request.config.getoption("--group")
