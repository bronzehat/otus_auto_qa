"""
Base class to initialize the base page that will be called from all pages"
"""
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import MySQLdb
from datetime import datetime

db = MySQLdb.connect(host="localhost", user="ocuser", passwd="PASSWORD", db="log")
cursor = db.cursor()
loglevel = 'DEBUG'

class BasePage:
    """Class to initialize the products page"""

    def __init__(self, driver):
        self.driver = driver

    def _get_all_attributes_(self, element):
        """
        returns all properties of an element
        here: not
        :param element:
        :return:
        """
        return self.driver.execute_script(
            'var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index)'
            ' { items[arguments[0].attributes[index].name] = '
            'arguments[0].attributes[index].value }; '
            'return items;',
            element)

    def _get_attribute_(self, element, attribute):
        """
        returns value of an element's property
        :param element:
        :param attribute:
        :return:
        """
        return element.get_attribute(attribute)

    def _get_css_attribute_(self, element, prop):
        """
        returns value of an element's css property
        :param element:
        :param prop:
        :return:
        """
        return element.value_of_css_property(prop)

    def _find_and_clear_element_(self, by, value):
        """
        finds an element and clears it as a user (Ctrl+A, Backspace)
        :param by:
        :param value:
        :return:
        """
        element = self.driver.find_element(by, value)
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)

    def _clear_element_(self, element):
        """
        Clears the field as a user (Ctrl+A, Backspace)
        :param element:
        :return:
        """
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACK_SPACE)

    def _wait_element_(self, by, value, delay=10):
        """
        waits for an element to be present at the page
        here: code is used in Products page object, but not as this method implementation,
        I think it's more interesting
        :param by:
        :param value:
        :param delay:
        :return:
        """
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((by, value)))
            element = self.driver.find_element(by, value)
            return element
        except (NoSuchElementException, TimeoutException):
            return False

    def _wait_element_in_other_element_(self, element, by, value, delay=25):
        """
        waits for an element to be present in other element
        :param element:
        :param by:
        :param value:
        :param delay:
        :return:
        """
        try:
            WebDriverWait(element, delay).until(EC.presence_of_element_located((by, value)))
            el = element.find_element(by, value)
            return el
        except TimeoutException:
            return False

    def _wait_visibility_(self, element, by, value, delay=25):
        """
        waits while element becomes visible
        :param element:
        :param by:
        :param value:
        :return:
        """
        try:
            WebDriverWait(element, delay).until(EC.visibility_of_element_located((by, value)))
            el = element.find_element(by, value)
            return el
        except TimeoutException:
            return False

    def _get_url(self):
        """
        checks current page's url
        :return:
        """
        return self.driver.current_url

    def _back_(self):
        """
        sends the browser a "back" command
        :return:
        """
        self.driver.back()

    def error_alert(self):
        """
        returns text of a failure alert after modification of an element
        :return:
        """
        return self.driver.find_element_by_class_name("alert-danger").text

    def success_alert(self):
        """
        returns text of a success alert after modification of an element
        :return:
        """
        return self.driver.find_element_by_class_name("alert-success").text

    def screen(self, screenshot_name):
        path_to_screenshot = "".join([os.getcwd(), "/screenshots", screenshot_name])
        self.driver.get_screenshot_as_file(path_to_screenshot)

    def log_in_db(self, message):
        """
        Writes events in log database
        :return:
        """
        cursor.execute("""insert into log.main (datetime, loglevel, info) values
                        ('{}', '{}', '{}')""".format(datetime.now(), loglevel, message))
        db.commit()