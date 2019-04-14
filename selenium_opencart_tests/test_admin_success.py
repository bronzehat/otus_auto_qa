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

    def test_admin_login(self, chosen_browser):
        """
        This test checks successful login by admin
        in admin dashboard
        :param admin_login_page:
        :param chosen_browser:
        :return: asserts if dashboard opens
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.set_username("root")
        loginpage.set_password("o9p0[-]=")
        loginpage.login()
        time.sleep(5)
        assert "dashboard" in loginpage._get_url()
        loginpage.logout()

    def test_opencart_off_page(self, chosen_browser):
        """
        This test is checking if opencart official site
        opens while clicking at the link "OpenCart"
        :param chosen_browser: asserts if url is correct
        :return:
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.goto_opencart_site()
        assert loginpage._get_url() == "https://www.opencart.com/"
        loginpage._back_()
        time.sleep(5)

    def test_forgotten_page_url(self, chosen_browser):
        """
        This test checks url of the page
        while "Forgotten Password" is clicked
        :param chosen_browser: asserts if url is correct
        :return:
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.forgotten_password()
        assert "index.php?route=common/forgotten" in loginpage._get_url()