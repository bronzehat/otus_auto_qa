"""
This is the conftest for first_selenium_tests
Here are commandline options and fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from selenium_opencart_tests.models.page_objects.page_objects import ProductsPage, LoginPage


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
        "--url", action="store", dest="url", type=str, default="http://localhost",
        help="print url for testing"
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
    else:
        print "No browser chosen! Choose chrome, firefox or ie"
        pytest.xfail("No browser chosen")
    request.addfinalizer(driver.quit)
    return driver

# Further are fixtures fot LoginPage and ProductsPage testing
@pytest.fixture(scope="module")
def login_page(chosen_browser):
    """
    Returns LoginPage class element
    :param chosen_browser:
    :return:
    """
    return LoginPage(chosen_browser)

@pytest.fixture(scope="module")
def login(login_page):
    """
    Logins to the admin page
    :param login_page:
    :return:
    """
    login_page.set_username("root")
    login_page.set_password("o9p0[-]=")
    login_page.login()

@pytest.fixture(scope="module")
def open_login_page(chosen_browser, request):
    """
    Returns url of needed admin page
    :param chosen_browser:
    :param request:
    :return:
    """
    url = '/opencart/admin/'
    return chosen_browser.get("".join([request.config.getoption("--url"), url]))

@pytest.fixture(scope="module")
def products_page(chosen_browser):
    """
    Returns ProductsPage class element
    :param chosen_browser:
    :return:
    """
    return ProductsPage(chosen_browser)

@pytest.fixture(scope="module")
def open_products(products_page):
    """
    Opens products list page for tests
    :param products_page:
    :return:
    """
    products_page.open_products_list()
