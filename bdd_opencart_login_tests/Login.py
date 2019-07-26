from robot.api.deco import keyword
# from selenium import webdriver
import sys
sys.path.remove('')
sys.path.append('.')
from LoginAdmin import LoginAdmin
from LoginUser import LoginUser


class Login(LoginAdmin, LoginUser):
    """
    Class combining admin and customer login test for OpenCart
    """

    @keyword(name="Login Admin")
    def login_admin(self):
        self.open_login_admin_page()
        self.enter_admin_credentials()
        self.submit_admin_login()
        self.open_adminpane_menu()
        self.quit_browser_admin()

    @keyword(name="Login User")
    def login_user(self):
        self.open_login_user_page()
        self.open_login_user_menu()
        self.enter_user_credentials()
        self.submit_user_login()
        self.open_user_home()
        self.quit_browser_user()

