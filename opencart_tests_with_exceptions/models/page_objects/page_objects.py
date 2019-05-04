"""
Page Objects for:
- Login Page
- Products Page
"""

from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from opencart_tests_with_exceptions.models.locator import ProductsPageLocators, LoginPageLocators
from opencart_tests_with_exceptions.models.page import BasePage


class LoginPage(BasePage):
    """
    Class for our test opencart site's Login Page testing
    """

    def set_username(self, username):
        """Prints username in username field"""
        self.driver.find_element(*LoginPageLocators.USERNAME).send_keys(username)

    def set_password(self, password):
        """Prints password in password field"""
        self.driver.find_element(*LoginPageLocators.PASSWORD).send_keys(password)

    def login(self):
        """Clicks Log In button"""
        self.driver.find_element(*LoginPageLocators.PRIMARY_BUTTON).click()

    def clear_password(self):
        """Clears password field"""
        self._clear_element_(self.driver.find_element(*LoginPageLocators.PASSWORD))

    def forgotten_password(self):
        """Clicks the 'Forgotten Password' link"""
        self.driver.find_element(*LoginPageLocators.FORGOTTEN).click()

    def enter_email(self, email):
        """Prints email at forgotten password page"""
        self.driver.find_element(*LoginPageLocators.FORGOTTEN_EMAIL).send_keys(email)

    def reset_password_button(self):
        """Clicks Reset password button"""
        self.driver.find_element(*LoginPageLocators.PASSWORD_RESET_BUTTON).click()

    def logout(self):
        """Clicks Log Out button"""
        self.driver.find_element(*LoginPageLocators.LOGOUT).click()

    def goto_opencart_site(self):
        """clicks the link of OpenCart off site"""
        self.driver.find_element(*LoginPageLocators.OFF_SITE).click()


class ProductsPage(BasePage):
    """Class for our test opencart site's Products Page testing"""

    def open_products_list(self):
        """Opens products list for test"""
        try:
            self.driver.find_element_by_link_text("Catalog").click()
            self.driver.find_element_by_link_text("Products").click()
        except NoSuchElementException:
            print "Can't find Products list!"
        except TimeoutException:
            print "Too long loading Products list!"

    def add_product(self, name, tag, model):
        """Adds a product, fills the required fields"""
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.ADD_NAME).send_keys(name)
        self.driver.find_element(*ProductsPageLocators.ADD_METATAG).send_keys(tag)
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        self.driver.find_element(*ProductsPageLocators.ADD_MODEL).send_keys(model)
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.SAVE))).click()
        except NoSuchElementException:
            print "There's no SAVE button! Maybe something has changed?"

    def find_product(self, name):
        """Finds a product by name"""
        self._clear_element_((self.driver.find_element(*ProductsPageLocators.SEARCH_BY_NAME)))
        self.driver.find_element(*ProductsPageLocators.SEARCH_BY_NAME).send_keys(name)
        try:
            WebDriverWait(self.driver, timeout=10).until \
                (EC.presence_of_element_located((ProductsPageLocators.SEARCH_BUTTON))).click()
        except NoSuchElementException:
            print "There's no Search Button!"

    def edit_product_min_quantity(self, min_quantity):
        """Edits first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.EDIT_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        minimum = self.driver.find_element(*ProductsPageLocators.CHANGE_MIN_QUANTITY)
        minimum.send_keys(Keys.CONTROL + "a")
        minimum.send_keys(Keys.BACKSPACE)
        minimum.send_keys(min_quantity)
        self.driver.find_element(*ProductsPageLocators.SAVE).click()

    def delete_product(self):
        """ Deletes first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.CHECKBOX).click()
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.DELETE_BUTTON))).click()
        except NoSuchElementException:
            print "There's no DELETE button! Maybe something has changed?"
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            print "There's no alert to switch to after deleting!"

    def alert_bg_color(self):
        """
        Checks if alert's background color is as wished
        :return: hex value of alert's background color
        """
        rgb = self._get_css_attribute_\
            (self.driver.find_element(*ProductsPageLocators.SUCCESS_ALERT), "background-color")
        return Color.from_string(rgb).hex
