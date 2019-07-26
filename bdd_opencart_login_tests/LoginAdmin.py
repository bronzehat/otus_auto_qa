from selenium import webdriver


class LoginAdmin():

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(firefox_options=self.options)

    def open_login_admin_page(self):
        self.driver.get("http://demo23.opencart.pro/admin/")

    def enter_admin_credentials(self):
        self.driver.find_element_by_id("input-username").send_keys("demo")
        self.driver.find_element_by_id("input-password").send_keys("demo")

    def submit_admin_login(self):
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def open_adminpane_menu(self):
        self.driver.find_element_by_id("button-menu").click()

    def quit_browser_admin(self):
        self.driver.quit()
