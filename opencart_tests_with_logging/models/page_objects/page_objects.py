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
import time
import os
import sys
import logging
from opencart_tests_with_logging.models.locator import ProductsPageLocators, LoginPageLocators
from opencart_tests_with_logging.models.page import BasePage


logger = logging.getLogger('logger')
log_file_path = "".join([os.getcwd(), '/logs/main.log'])  # wanted LOGIN_LOG but got error
logger.setLevel('INFO')  # wanted LOGIN_LOG_LEVEL but got error
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
fh = logging.FileHandler(filename=log_file_path)
fh.setLevel('INFO')
fh.setFormatter(formatter)
logger.addHandler(fh)

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
        logger.info("Logout")

    def goto_opencart_site(self):
        """clicks the link of OpenCart off site"""
        self.driver.find_element(*LoginPageLocators.OFF_SITE).click()
        logger.info("Off site is opened")


class ProductsPage(BasePage):
    """Class for our test opencart site's Products Page testing"""

    def logging_browser_performance(self):
        """

        :return:
        """
        browser_log = self.driver.get_log("browser")
        for i in browser_log:
            logger.debug(i)
        browser_performance_log = self.driver.get_log("performance")
        for l in browser_performance_log:
            logger.debug(l)

    def write_log(self, message):
        logger.info(message)

    def open_products_list(self):
        """Opens products list for test"""
        try:
            self.driver.find_element_by_link_text("Catalog").click()
            self.driver.find_element_by_link_text("Products").click()
            logger.debug("Successful Products page opening")
        except NoSuchElementException:
            print "Can't find Products list!"
            logger.info("Can't find Products list!")
            self.logging_browser_performance()
        except TimeoutException:
            print "Too long loading Products list!"
            logger.info("Too long loading Products list!")
            self.logging_browser_performance()

    def add_product(self, name, tag, model, images_list):
        """Adds a product, fills the required fields"""
        logger.info("***Start adding product***")
        logger.info("New product name is: {}".format(name))
        logger.info("New product tag is: {}".format(tag))
        logger.info("New product model is: {}".format(model))
        logger.info("New product image is: {}".format(images_list))
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.ADD_NAME).send_keys(name)
        self.driver.find_element(*ProductsPageLocators.ADD_METATAG).send_keys(tag)
        logger.info("Name and tag are filled")
        time.sleep(2)
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        self.driver.find_element(*ProductsPageLocators.ADD_MODEL).send_keys(model)
        logger.info("Model is filled")
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        for i in images_list:
            self.add_image(i)
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.SAVE))).click()
            logger.info("***Changes are saved***")
        except NoSuchElementException:
            print "There's no SAVE button! Maybe something has changed?"
            logger.info("There's no SAVE button! Maybe something has changed?")
            self.logging_browser_performance()

    def add_image(self, image):
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()  # time.sleep(2)
        self.driver.find_element(*ProductsPageLocators.IMAGE_UPLOAD_BUTTON).click()
        time.sleep(2)
        image_path = "".join([os.getcwd(), image])
        self.driver.find_element(*ProductsPageLocators.INPUT_FILE).send_keys(image_path)
        logger.info("Image is found")
        time.sleep(4)
        self.driver.switch_to.alert.accept()
        logger.info("Alert is accepted")
        time.sleep(2)
        uploaded_image = "".join([str(ProductsPageLocators.UPLOADED_IMAGE[1]), str(image), "')]"])
        self.driver.find_element(ProductsPageLocators.UPLOADED_IMAGE[0],
                                 uploaded_image).click()

    def find_product(self, name):
        """Finds a product by name"""
        self._clear_element_((self.driver.find_element(*ProductsPageLocators.SEARCH_BY_NAME)))
        self.driver.find_element(*ProductsPageLocators.SEARCH_BY_NAME).send_keys(name)
        try:
            WebDriverWait(self.driver, timeout=10).until \
                (EC.presence_of_element_located((ProductsPageLocators.SEARCH_BUTTON))).click()
        except NoSuchElementException:
            print "There's no Search Button!"
            logger.info("There's no Search Button!")
            self.logging_browser_performance()

    def edit_product_min_quantity(self, min_quantity):
        """Edits first product found on page, use with find_product if needed"""
        logger.info("***Start editing product***")
        self.driver.find_element(*ProductsPageLocators.EDIT_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        minimum = self.driver.find_element(*ProductsPageLocators.CHANGE_MIN_QUANTITY)
        minimum.send_keys(Keys.CONTROL + "a")
        minimum.send_keys(Keys.BACKSPACE)
        logger.info("Property field is cleared")
        minimum.send_keys(min_quantity)
        logger.info("New value of minimal quantity: {}".format(min_quantity))
        self.driver.find_element(*ProductsPageLocators.SAVE).click()
        logger.info("***Finished editing product***")

    def delete_product(self):
        """ Deletes first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.CHECKBOX).click()
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.DELETE_BUTTON))).click()
        except NoSuchElementException:
            print "There's no DELETE button! Maybe something has changed?"
            logger.info("No Delete button found.")
            self.logging_browser_performance()
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            print "There's no alert to switch to after deleting!"
            logger.info("No alert while deleting.")
            self.logging_browser_performance()

    def alert_bg_color(self):
        """
        Checks if alert's background color is as wished
        :return: hex value of alert's background color
        """
        rgb = self._get_css_attribute_\
            (self.driver.find_element(*ProductsPageLocators.SUCCESS_ALERT), "background-color")
        color_hex = Color.from_string(rgb).hex
        logger.info("Background-color property of the alert is: {}".format(color_hex))
        return color_hex

    def delete_test_images(self):
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()
        self.driver.find_element(*ProductsPageLocators.UPLOADED_IMAGE1_CHECKBOX).click()
        self.driver.find_element(*ProductsPageLocators.UPLOADED_IMAGE_DELETE_BUTTON).click()
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, timeout=20).until\
                (EC.visibility_of_element_located((ProductsPageLocators.IMAGES_CLOSE)))
        self.driver.switch_to_default_content()
