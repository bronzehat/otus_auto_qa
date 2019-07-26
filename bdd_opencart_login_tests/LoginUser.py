from selenium import webdriver


class LoginUser():

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(firefox_options=self.options)

    def open_login_user_page(self):
        self.driver.get("http://demo23.opencart.pro/")

    def open_login_user_menu(self):
        self.driver.find_element_by_xpath("//a[contains(@href, 'route=account/account')]").click()
        self.driver.find_element_by_xpath("//a[contains(@href, 'route=account/login')]").click()

    def enter_user_credentials(self):
        self.driver.find_element_by_id("input-email").send_keys("2annasay+oppro@mail.ru")
        self.driver.find_element_by_id("input-password").send_keys("o9p0[-]=")

    def submit_user_login(self):
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    def open_user_home(self):
        self.driver.find_element_by_xpath("//a[contains(@href, 'route=account/edit')]")

    def quit_browser_user(self):
        self.driver.quit()
