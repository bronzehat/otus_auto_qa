"""
Base class to initialize the base page that will be called from all pages"
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Class to initialize the products page"""

    def __init__(self, driver):
        self.driver = driver

    def _get_all_attributes_(self, element):
        return self.driver.execute_script(
            'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index)'
            ' { items[arguments[0].attributes[index].name] = '
            'arguments[0].attributes[index].value }; '
            'return items;',
            element)

    def _get_attribute_(self, element, attribute):
        return element.get_attribute(attribute)

    def _get_css_attribute_(self, element, prop):
        return element.value_of_css_property(prop)

    def _find_and_clear_element_(self, by, value):
        element = self.driver.find_element(by, value)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)

    def _clear_element_(self, element):
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)

    def _wait_element_(self, by, value, delay=25):
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((by, value)))
            element = self.driver.find_element(by, value)
            return element
        except (NoSuchElementException, TimeoutException):
            return False

    def _wait_element_in_other_element_(self, element, by, value, delay=25):
        try:
            WebDriverWait(element, delay).until(EC.presence_of_element_located((by, value)))
            el = element.find_element(by, value)
            return el
        except TimeoutException:
            return False

    def _wait_visibility_(self, element, by, value):
        pass

    def _get_url(self):
        return self.driver.current_url

    def _back_(self):
        self.driver.back()

    def _error_alert(self):
        return self.driver.find_element_by_class_name("alert-danger").text

    def _success_alert(self):
        return self.driver.find_element_by_class_name("alert-success").text
