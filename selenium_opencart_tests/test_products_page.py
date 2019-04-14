"""
These tests check the functions of adding, editing and deleting products
by admin
"""
import time
import pytest
from selenium_opencart_tests.models.page_objects.page_objects import ProductsPage, LoginPage


@pytest.mark.usefixtures("open_products")
@pytest.mark.usefixtures("login")
@pytest.mark.usefixtures("open_login_page")
class TestProductsPage:
    """Class for Products Page positive tests (add, edit, delete a product)"""

    def test_add_product(self, chosen_browser):
        """
        Checks adding product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = ProductsPage(chosen_browser)
        product.add_product("TestProduct", "TestMetaTagTitle", "TestModel")
        time.sleep(5)
        assert "Success: You have modified products!" in product._success_alert()
        time.sleep(3)

    def test_edit_product(self, chosen_browser):
        """
        Checks editing product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = ProductsPage(chosen_browser)
        product.find_product("TestProduct") # edit if need any other name
        product.edit_product_min_quantity("5")
        time.sleep(5)
        assert "Success: You have modified products!" in product._success_alert()
        time.sleep(3)

    def test_delete_product(self, chosen_browser):
        """
        Checks deleting product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = ProductsPage(chosen_browser)
        product.find_product("TestProduct") # edit if need any other name
        product.delete_product()
        time.sleep(5)
        assert "Success: You have modified products!" in product._success_alert()
