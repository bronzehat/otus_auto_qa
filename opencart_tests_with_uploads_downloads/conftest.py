"""
This is the conftest for first_selenium_tests
Here are commandline options and fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from opencart_tests_with_uploads_downloads.models.page_objects.page_objects import \
    ProductsPage, LoginPage, DownloadPage

# Login Page test data
ADMIN_USERNAME = "root"
ADMIN_PASSWORD = "o9p0[-]="
BASE_URL = "http://localhost"
ADMIN_DASHBOARD_PATH = "/opencart/admin/"

# Products Page test data
TEST_PRODUCT_NAME = "TestProduct"
TEST_PRODUCT_TAG = "TestMetaTagTitle"
TEST_PRODUCT_MODEL = "TestModel"
MINIMAL_QUANTITY = "5"
PRODUCTS_SUCCESS = "Success: You have modified products!"
DEFAULT_IMPLICITLY_WAIT = 60
BG_COLOR = "#cbeacb"
IMAGES = ["/1.png", "/2.png", "/3.png"]

# Downloads Page test data
NEW_FILE_NAME = "TestFile"
NEW_FILE_MASK = "testfilemask"
NEW_FILE = "1.png"
DOWNLOAD_PAGE_SUCCESS_ALERT = "Success: You have modified downloads!"

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
        "--url", action="store", dest="url", type=str, default=BASE_URL,
        help="print url for testing"
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
        driver = webdriver.Chrome(chrome_options=options)
    elif parameter == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-fullscreen")
        # options.add_argument("--headless")
        driver = webdriver.Firefox(firefox_options=options)
    elif parameter == "ie":
        options = IeOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = webdriver.Ie(ie_options=options)
    else:
        print "No browser chosen! Choose chrome, firefox or ie"
        pytest.xfail("No browser chosen")
    implicit_timeout = request.config.getoption("--implicit")
    driver.implicitly_wait(implicit_timeout)
    driver.set_page_load_timeout(60)
    driver.desired_capabilities["unexpectedAlertBehavior"] = "dismiss"
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
    login_page.set_username(ADMIN_USERNAME)
    login_page.set_password(ADMIN_PASSWORD)
    login_page.login()


@pytest.fixture
def admin_username():
    """
    Returns admin username for the site
    (is set manually higher)
    :return: username string
    """
    return ADMIN_USERNAME

@pytest.fixture
def admin_password():
    """
    Returns admin password for the site
    (is set manually higher)
    :return: password string
    """
    return ADMIN_PASSWORD

@pytest.fixture
def products_success():
    """
    Returns a product modify suceess alert text
    :return: success modify alert string
    """
    return PRODUCTS_SUCCESS

@pytest.fixture
def product_name():
    """
    Returns a string for product name (for
    adding and search)
    :return: string for product name
    """
    return TEST_PRODUCT_NAME

@pytest.fixture
def product_tag():
    """
    Returns a string for product tag
    (for adding)
    :return: string for product tag
    """
    return TEST_PRODUCT_TAG

@pytest.fixture
def product_model():
    """
    Returns a string for product model
    (for adding)
    :return: string for product model
    """
    return TEST_PRODUCT_MODEL

@pytest.fixture
def min_quantity():
    """
    Returns minimal quantity for
    product edit test
    :return:
    """
    return MINIMAL_QUANTITY

@pytest.fixture(scope="module")
def open_login_page(chosen_browser, request):
    """
    Returns url of needed admin page
    :param chosen_browser:
    :param request:
    :return:
    """
    return chosen_browser.get("".join([request.config.getoption("--url"),
                                       ADMIN_DASHBOARD_PATH]))

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

@pytest.fixture(scope="module")
def downloads_page(chosen_browser):
    """
    Returns ProductsPage class element
    :param chosen_browser:
    :return:
    """
    return DownloadPage(chosen_browser)

@pytest.fixture(scope="module")
def open_downloads(downloads_page):
    """
    Opens products list page for tests
    :param products_page:
    :return:
    """
    downloads_page.open_downloads()

@pytest.fixture
def new_file_name():
    """
    returns a new file name for test
    :return:
    """
    return NEW_FILE_NAME


@pytest.fixture
def new_file_mask():
    """
    returns a new file mask for test
    :return:
    """
    return NEW_FILE_MASK

@pytest.fixture
def new_file():
    """
    returns new file name (path will be in the working directory)
    :return:
    """
    return NEW_FILE

@pytest.fixture
def downloads_success():
    """
    returns success alert for downloads page
    :return:
    """
    return DOWNLOAD_PAGE_SUCCESS_ALERT

@pytest.fixture
def bg_color():
    """
    Returns preferrable background color of the element
    :return:
    """
    return BG_COLOR
