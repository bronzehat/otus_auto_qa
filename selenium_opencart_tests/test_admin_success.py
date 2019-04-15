"""
These are tests of successful scenarios
for our test opencart site's login page
"""
import time
import pytest
from selenium_opencart_tests.models.page_objects.page_objects import LoginPage


@pytest.mark.usefixtures("open_login_page")
class TestLoginPage:
    """Class for Login Page positive tests"""

    def test_admin_login(self,
                         login_page,
                         admin_username,
                         admin_password,
                         page_url_key):
        """
        This test checks successful login by admin
        in admin dashboard
        :param admin_login_page:
        :param chosen_browser:
        :return: asserts if dashboard opens
        """
        loginpage = login_page
        loginpage.set_username(admin_username)
        loginpage.set_password(admin_password)
        loginpage.login()
        time.sleep(5)
        assert page_url_key in loginpage._get_url()
        loginpage.logout()

    def test_opencart_off_page(self, login_page, vendor_url):
        """
        This test is checking if opencart official site
        opens while clicking at the link "OpenCart"
        :param chosen_browser: asserts if url is correct
        :return:
        """
        loginpage = login_page
        loginpage.goto_opencart_site()
        assert loginpage._get_url() == vendor_url
        loginpage._back_()
        time.sleep(5)

    def test_forgotten_page_url(self, chosen_browser,
                                forgotten_page):
        """
        This test checks url of the page
        while "Forgotten Password" is clicked
        :param chosen_browser: asserts if url is correct
        :return:
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.forgotten_password()
        assert forgotten_page in loginpage._get_url()
