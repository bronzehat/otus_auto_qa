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
from opencart_tests_with_database.models.locator import ProductsPageLocators, LoginPageLocators
from opencart_tests_with_database.models.page import BasePage
from selenium.webdriver import ActionChains

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
        self.log_in_db("Logout")
        time.sleep(2)
        self.screen("/logout.png")

    def goto_opencart_site(self):
        """clicks the link of OpenCart off site"""
        self.driver.find_element(*LoginPageLocators.OFF_SITE).click()
        self.log_in_db("Off site is opened")
        self.screen("/off_site.png")


class ProductsPage(BasePage):
    """Class for our test opencart site's Products Page testing"""

    def write_log(self, message):
        self.log_in_db(message)

    def open_products_list(self):
        """Opens products list for test"""
        try:
            self.driver.find_element_by_link_text("Catalog").click()
            self.driver.find_element_by_link_text("Products").click()
            self.log_in_db("Successful Products page opening")
        except NoSuchElementException:
            message = "Can't find Products list!"
            print(message)
            self.log_in_db(message)
        except TimeoutException:
            message = "Too long loading Products list!"
            print(message)
            self.log_in_db(message)

    def add_product(self, name, tag, model, images_list):
        """Adds a product, fills the required fields"""
        self.log_in_db("***Start adding product***")
        self.log_in_db("New product name is: {}".format(name))
        self.log_in_db("New product tag is: {}".format(tag))
        self.log_in_db("New product model is: {}".format(model))
        self.log_in_db("New product image is: {}".format(images_list))
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.ADD_NAME).send_keys(name)
        self.driver.find_element(*ProductsPageLocators.ADD_METATAG).send_keys(tag)
        self.log_in_db("Name and tag are filled")
        time.sleep(2)
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        self.driver.find_element(*ProductsPageLocators.ADD_MODEL).send_keys(model)
        self.log_in_db("Model is filled")
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        for i in images_list:
            self.add_image(i)
            self.screen("/add_images.png")
            self.log_in_db("Created screen add_images.png")
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.SAVE))).click()
            self.log_in_db("***Changes are saved***")
        except NoSuchElementException:
            print("There's no SAVE button! Maybe something has changed?")
            self.log_in_db("There's no SAVE button! Maybe something has changed?")

    def add_image(self, image):
        """
        Adds an image to a product
        :param image:
        :return:
        """
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()  # time.sleep(2)
        self.driver.find_element(*ProductsPageLocators.IMAGE_UPLOAD_BUTTON).click()
        time.sleep(2)
        image_path = "".join([os.getcwd(), image])
        self.driver.find_element(*ProductsPageLocators.INPUT_FILE).send_keys(image_path)
        self.log_in_db("Image {} is found".format(image))
        time.sleep(4)
        self.driver.switch_to.alert.accept()
        self.log_in_db("Alert is accepted")
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
            print("There's no Search Button!")
            self.log_in_db("There's no Search Button!")

    def edit_product_min_quantity(self, min_quantity):
        """Edits first product found on page, use with find_product if needed"""
        self.log_in_db("***Start editing product***")
        self.driver.find_element(*ProductsPageLocators.EDIT_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_DATA).click()
        minimum = self.driver.find_element(*ProductsPageLocators.CHANGE_MIN_QUANTITY)
        minimum.send_keys(Keys.CONTROL + "a")
        minimum.send_keys(Keys.BACKSPACE)
        self.log_in_db("Property field is cleared")
        minimum.send_keys(min_quantity)
        self.log_in_db("New value of minimal quantity: {}".format(min_quantity))
        self.driver.find_element(*ProductsPageLocators.SAVE).click()
        self.screen("/edit_finish.png")
        self.log_in_db("Created a screen edit_finish.png")
        self.log_in_db("***Finished editing product***")

    def delete_product(self):
        """ Deletes first product found on page, use with find_product if needed"""
        self.driver.find_element(*ProductsPageLocators.CHECKBOX).click()
        try:
            WebDriverWait(self.driver, timeout=10).until\
                (EC.presence_of_element_located((ProductsPageLocators.DELETE_BUTTON))).click()
        except NoSuchElementException:
            print("There's no DELETE button! Maybe something has changed?")
            self.log_in_db("No Delete button found.")
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            print("There's no alert to switch to after deleting!")
            self.log_in_db("No alert while deleting.")

    def alert_bg_color(self):
        """
        Checks if alert's background color is as wished
        :return: hex value of alert's background color
        """
        rgb = self._get_css_attribute_\
            (self.driver.find_element(*ProductsPageLocators.SUCCESS_ALERT), "background-color")
        color_hex = Color.from_string(rgb).hex
        self.log_in_db("Background-color property of the alert is: {}".format(color_hex))
        return color_hex

    def delete_test_image(self, images_list):
        """
        Deletes test images from the list in arguments
        :param images_list:
        :return:
        """
        self.driver.find_element(*ProductsPageLocators.ADD_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.GOTO_IMAGE).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_BUTTON).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON1).click()
        self.driver.find_element(*ProductsPageLocators.ADD_IMAGE_POPUP).click()
        self.driver.find_element(*ProductsPageLocators.IMAGE_EDIT_BUTTON2).click()
        for image in images_list:
            image_name = image.split("/")[-1]
            checkbox = "".join([ProductsPageLocators.UPLOADED_IMAGE_CHECKBOX[1], "/", image_name, "']"])
            self.driver.find_element(ProductsPageLocators.UPLOADED_IMAGE_CHECKBOX[0], checkbox).click()
            self.driver.find_element(*ProductsPageLocators.UPLOADED_IMAGE_DELETE_BUTTON).click()
            time.sleep(3)
            self.driver.switch_to.alert.accept()
            time.sleep(3)
            self.driver.switch_to.alert.accept()
            time.sleep(3)
        actionchains = ActionChains(self.driver)
        actionchains.send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
