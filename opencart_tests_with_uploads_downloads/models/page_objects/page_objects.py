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
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from opencart_tests_with_uploads_downloads.models.locator import ProductsPageLocators,\
    LoginPageLocators, DownloadsPageLocators
from opencart_tests_with_uploads_downloads.models.page import BasePage


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

    def add_product(self, name, tag, model, images_list):
        """Adds a product, fills the required fields"""
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.ADD_NAME).send_keys(name)
        self.driver.find_element(*ProductsPageLocators.ADD_METATAG).send_keys(tag)
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        self.driver.find_element(*ProductsPageLocators.ADD_MODEL).send_keys(model)
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        self.add_image(images_list)
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.SAVE))).click()
        except NoSuchElementException:
            print "There's no SAVE button! Maybe something has changed?"

    def add_image(self, images_list):
        """
        Adds images to a product - uncomment first line if needed a
        single adding image action (without adding product, etc.)
        :param images:
        :return:
        """
        # self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        for i in images_list:
            self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
            self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
            self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
            self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()# time.sleep(2)
            self.driver.find_element(*ProductsPageLocators.IMAGE_UPLOAD_BUTTON).click()
            time.sleep(2)
            self.driver.find_element(*ProductsPageLocators.INPUT_FILE).send_keys(os.getcwd() + i)
            time.sleep(4)
            self.driver.switch_to.alert.accept()
            time.sleep(2)
            uploaded_image = "".join([str(ProductsPageLocators.UPLOADED_IMAGE[1]), str(i), "')]"])
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

    def edit_product_min_quantity(self, min_quantity):
        """Edits first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.EDIT_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        minimum = self.driver.find_element(*ProductsPageLocators.CHANGE_MIN_QUANTITY)
        minimum.send_keys(Keys.CONTROL + "a")
        minimum.send_keys(Keys.BACKSPACE)
        minimum.send_keys(min_quantity)
        self.driver.find_element(*ProductsPageLocators.SAVE).click()

    def delete_product(self, images_list):
        """ Deletes first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.EDIT_BUTTON).click()
        self.delete_test_images(images_list)
        self.driver.find_element(*ProductsPageLocators.SAVE).click()
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

    def delete_test_images(self, images_list):
        """
        deletes test images from uploaded images list
        uncomment commened lines if needed just deletion as a single action
        :return:
        """
        # self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        # self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()

        for i in images_list:
            time.sleep(2)
            image_checkbox_str = "".join([str(ProductsPageLocators.UPLOADED_IMAGE_CHECKBOX[1]), str(i), "']"])
            for i in self.driver.find_elements_by_id(image_checkbox_str):
                print(i)
            # PROBLEM - NO CHECKBOX IS CLICKED!
            self.driver.execute_script("arguments[0].scrollIntoView();", image_checkbox)
            self.driver.execute_script("$(arguments[0]).click();", image_checkbox)
            actionchains = ActionChains(self.driver)
            actionchains.move_to_element(image_checkbox)
            actionchains.click()
            actionchains.perform()
        time.sleep(2)
        self.driver.find_element(*ProductsPageLocators.UPLOADED_IMAGE_DELETE_BUTTON).click()
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        time.sleep(3)
        self.driver.switch_to.alert.accept()
        self.driver.switch_to_default_content()

    def alert_bg_color(self):
        """
        Checks if alert's background color is as wished
        :return: hex value of alert's background color
        """
        rgb = self._get_css_attribute_\
            (self.driver.find_element(*ProductsPageLocators.SUCCESS_ALERT), "background-color")
        return Color.from_string(rgb).hex

class DownloadPage(BasePage):
    """
    Class for our test opencart site's Downloads Page testing
    """
    def open_downloads(self):
        """
        Opens downloads page for tests
        :return:
        """
        try:
            self.driver.find_element_by_link_text("Catalog").click()
            self.driver.find_element_by_link_text("Downloads").click()
        except NoSuchElementException:
            print "Can't find Downloads list!"
        except TimeoutException:
            print "Too long loading Downloads list!"

    def add_file(self, name, mask, file):
        """
        Tests adding a new file for download
        :return:
        """
        self.driver.find_element(*DownloadsPageLocators.ADD_DOWNLOAD_FILE_BUTTON).click()
        self.driver.find_element(*DownloadsPageLocators.INPUT_NEW_FILE_NAME).send_keys(name)
        self.driver.find_element(*DownloadsPageLocators.INPUT_NEW_FILE_MASK).send_keys(mask)
        # uncomment next line and comment the line after it
        # if real path to file is accepted by the site
        # path = "".join([os.getcwd(), "/", str(file)])
        path = "".join([str(file), ".uE2AcfY1Re2qwZtJ864teoErpmD2Herv"])
        self.driver.find_element(*DownloadsPageLocators.INPUT_NEW_FILE).send_keys(path)
        self.driver.find_element(*ProductsPageLocators.SAVE).click()


