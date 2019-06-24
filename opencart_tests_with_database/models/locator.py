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
    GOTO_IMAGE = (By.LINK_TEXT, "Image")
    ADD_IMAGE_BUTTON = (By.XPATH, "//button[contains(@data-original-title,'Add Image')]")
    IMAGE_EDIT_BUTTON1 = (By.XPATH, "//img[contains(@src,'http://localhost/opencart/image/cache/no_image-100x100.png')]")
    ADD_IMAGE_POPUP = (By.CLASS_NAME, "popover.fade.right.in")
    IMAGE_EDIT_BUTTON2 = (By.ID, "button-image")
    IMAGE_UPLOAD_BUTTON = (By.ID, "button-upload")
    UPLOADED_IMAGE = (By.XPATH, "//a[contains(@href, 'http://localhost/opencart/image/catalog")
    INPUT_FILE = (By.CSS_SELECTOR, "input[type='file']")
    DEFAULT_IMAGE = (By.XPATH, "img[contains(@data-placeholder,'http://localhost/opencart/image/cache/no_image')]")
    # editing a product
    EDIT_BUTTON = (By.XPATH, "//a[contains(@data-original-title,'Edit')]")
    CHANGE_MIN_QUANTITY = (By.ID, "input-minimum")
    # searching and deleting product
    SEARCH_BY_NAME = (By.ID, "input-name")
    SEARCH_BUTTON = (By.ID, "button-filter")
    CHECKBOX = (By.NAME, "selected[]")
    DELETE_BUTTON = (By.XPATH, "//button[@data-original-title='Delete']")
    SUCCESS_ALERT = (By.CLASS_NAME, "alert-success")
    # deleting test images
    UPLOADED_IMAGE_CHECKBOX = (By.XPATH, "//input[@value='catalog")
    UPLOADED_IMAGE_DELETE_BUTTON = (By.XPATH, "//button[@data-original-title='Delete']")
    # common locators
    SAVE = (By.XPATH, "//button[@data-original-title='Save']")
