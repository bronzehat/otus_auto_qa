"""
These tests are for negative scenatios
checking error alerts for our test opencart
site's login page
"""
import time
import pytest
from selenium_opencart_tests.models.page_objects.page_objects import LoginPage


@pytest.mark.usefixtures("open_login_page")
class TestLoginFail:
    """Class for Login Page negative tests"""

    def test_empty_login_fail(self, chosen_browser):
        """
        Checks if no enter with empty user|password
        :param chosen_browser:
        :return:
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.login()
        time.sleep(5)
        assert "No match for Username and/or Password." in \
               loginpage._error_alert()


    def test_forgotten_password_alert(self, chosen_browser):
        """
        Checks if alert appears after incorrect email is given
        to recover password
        :param admin_login_page:
        :param chosen_browser:
        :return: asserts if alert is correct
        """
        loginpage = LoginPage(chosen_browser)
        loginpage.forgotten_password()
        loginpage.enter_email("12345")
        loginpage.reset_password_button()
        assert "Warning: The E-Mail Address was not found in our records, please try again!"\
               in loginpage._error_alert()
