"""
These are locators for Products page
"""

from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    """Locators for Login Page testing"""

    USERNAME = (By.ID, "input-username")
    PASSWORD = (By.ID, "input-password")
    PRIMARY_BUTTON = (By.CLASS_NAME, "btn.btn-primary")
    FORGOTTEN = (By.LINK_TEXT, "Forgotten Password")
    LOGOUT = (By.XPATH, "//a[contains(@href, 'logout')]")
    OFF_SITE = (By.LINK_TEXT, "OpenCart")
    FORGOTTEN_EMAIL = (By.ID, "input-email")
    PASSWORD_RESET_BUTTON = (By.XPATH, "//button[@type='submit']")

class ProductsPageLocators(object):
    """Locators for Products Page testing"""

    # adding a product
    ADD_BUTTON = (By.XPATH, "//a[contains(@data-original-title,'Add New')]")
    ADD_NAME = (By.ID, "input-name1")
    ADD_METATAG = (By.ID, "input-meta-title1")
    GOTO_DATA = (By.LINK_TEXT, "Data")
    ADD_MODEL = (By.NAME, "model")
    # editing a product
    EDIT_BUTTON = (By.XPATH, "//a[contains(@data-original-title,'Edit')]")
    CHANGE_MIN_QUANTITY = (By.ID, "input-minimum")
    # searching and deleting product
    SEARCH_BY_NAME = (By.ID, "input-name")
    SEARCH_BUTTON = (By.ID, "button-filter")
    CHECKBOX = (By.NAME, "selected[]")
    DELETE_BUTTON = (By.XPATH, "//button[@data-original-title='Delete']")
    SUCCESS_ALERT = (By.CLASS_NAME, "alert-success")
    # common locators
    SAVE = (By.XPATH, "//button[@data-original-title='Save']")
