"""
This is the conftest for first_selenium_tests
Here are commandline options and fixtures
"""

import pytest
import psutil
import datetime
import os
import socket
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener

DEF_CITY = "ufa"
DEF_GROUP = "Children of Bodom"
DEFAULT_IMPLICITLY_WAIT = 60
CITIES = {"ufa": "Уфа", "msk": "Москва", "vlm": "Владимир", "vologda": "Вологда", "kgd": "Калининград",
          "rzn": "Рязань", "smr": "Самара", "saratov": "Саратов", "sochi": "Сочи", "cher": "Череповец",
          "yar": "Ярославль"}

class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("".join(["\nOpen page by URL:", url]))
    def after_navigate_to(self, url, driver):
        print("".join([url, " page opened"]))
    def after_quit(self, driver):
        print("\nQuit")
    def on_exception(self, exception, driver):
        driver.save_screenshot('screenshots/exception.png')
        print(exception)

def pytest_addoption(parser):
    """
    Adds a commandline option "--browser" to choose browser for tests
    :param parser:
    :return:
        """
    parser.addoption(
        "--implicit", action="store", dest="implicit", type=int, default=DEFAULT_IMPLICITLY_WAIT,
        help="manually define implicity wait for testing"
    )
    parser.addoption(
        "--browser", action="store", dest="browser", type=str, default="firefox",
        help="choose one of browsers (chrome, firefox or ie)"
        )
    parser.addoption(
        "--city", action="store", dest="city", type=str, default=DEF_CITY,
        help="print city for search"
    )
    parser.addoption(
        "--group", action="store", dest="group", type=str, default=DEF_GROUP,
        help="print group for search"
    )

@pytest.fixture(scope="module")
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
        driver = EventFiringWebDriver(webdriver.Chrome(chrome_options=options), MyListener())
    elif parameter == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-fullscreen")
        # options.add_argument("--headless")
        driver = EventFiringWebDriver(webdriver.Firefox(firefox_options=options),
                                      MyListener())
    elif parameter == "ie":
        options = IeOptions()
        options.add_argument("--start-fullscreen")
        options.add_argument("--headless")
        driver = EventFiringWebDriver(webdriver.Ie(ie_options=options), MyListener())
    else:
        print("No browser chosen! Choose chrome, firefox or ie")
        pytest.xfail("No browser chosen")
    implicit_timeout = request.config.getoption("--implicit")
    driver.implicitly_wait(implicit_timeout)
    driver.set_page_load_timeout(60)
    driver.desired_capabilities["unexpectedAlertBehavior"] = "dismiss"
    request.addfinalizer(driver.quit())
    return driver

@pytest.mark.usefixtures("host_ip")
@pytest.mark.usefixtures("proc_number")
@pytest.fixture(scope='session', autouse=True)
def extra_json_environment(request, host_ip, proc_number):
    request.config._json_environment.append(("host ip", host_ip))
    request.config._json_environment.append(("processors number", proc_number))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        # only add this during call instead of during any stage
        report.test_metadata = {
            "CPU usage (%)": psutil.cpu_percent(),
            "Virtual memory usage (%)": dict(psutil.virtual_memory()._asdict())
        }
        # edit stage metadata
        report.stage_metadata = {
            "Call time": str(datetime.datetime.now())
        }
    elif report.when == 'setup':
        report.stage_metadata = {
            'Setup time': str(datetime.datetime.now())
        }
    elif report.when == 'teardown':
        report.stage_metadata = {
            'Teardown time': str(datetime.datetime.now())
        }


@pytest.fixture(scope="session")
def host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

@pytest.fixture(scope="session")
def proc_number():
    proc_num = psutil.cpu_count()
    return proc_num


@pytest.fixture
def city(request):
    if request.config.getoption("--city") in CITIES:
        return request.config.getoption("--city")
    else:
        pytest.skip("city is not in available CITIES list")

@pytest.fixture
def city_rus(city):
    return CITIES[city]

@pytest.fixture
def group(request):
    return request.config.getoption("--group")

# Code below is for pytest-html report
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin('allure')
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, 'extra', [])
#     if report.when == 'call':
#         # always add url to report
#         extra.append(pytest_html.extras.url('http://www.example.com/'))
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             # only add additional allure on failure
#             extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
#         report.extra = extra
#
# # @pytest.mark.usefixtures("proc_number")
# # @pytest.mark.usefixtures("host_ip")
# @pytest.fixture(scope='session', autouse=True)
# def configure_html_report_env(request, host_ip, proc_number):
#     request.config._metadata.update(
#         {"hostname": socket.gethostname(),
#          "browser": request.config.getoption("--browser"),
#          "implicit_timeout": request.config.getoption("--implicit"),
#          "PATH variable": os.environ['PATH'],
#          "host_ip": host_ip,
#          "number of processors": proc_number,
#          "test made by:": "asayapova@testmail.com"
#          })
#     yield
