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

    def test_add_product(self,
                         products_page,
                         products_success,
                         product_name,
                         product_tag,
                         product_model):
        """
        Checks adding product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = products_page
        product.add_product(product_name, product_tag, product_model)
        time.sleep(5)
        assert products_success in product._success_alert()
        time.sleep(3)

    def test_edit_product(self,
                          chosen_browser,
                          product_name,
                          min_quantity,
                          products_success):
        """
        Checks editing product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = ProductsPage(chosen_browser)
        product.find_product(product_name) # edit if need any other name
        product.edit_product_min_quantity(min_quantity)
        time.sleep(5)
        assert products_success in product._success_alert()
        time.sleep(3)

    def test_delete_product(self,
                            products_page,
                            product_name,
                            products_success):
        """
        Checks deleting product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        product = products_page
        product.find_product(product_name) # edit if need any other name
        product.delete_product()
        time.sleep(5)
        assert products_success in product._success_alert()
