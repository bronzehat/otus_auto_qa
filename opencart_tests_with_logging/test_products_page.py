"""
These tests check the functions of adding, editing and deleting products
by admin
"""
import time
import pytest
from opencart_tests_with_logging.conftest import IMAGES as images_list

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
                         product_model,
                         bg_color):
        """
        Checks adding product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        products_page.add_product(product_name, product_tag, product_model, images_list)
        time.sleep(5)
        if products_page.alert_bg_color() == bg_color:
            print "\nAlert color is OK!"
            products_page.write_log("Alert color is OK!")
        assert products_success in products_page.success_alert()


    def test_edit_product(self,
                          products_page,
                          product_name,
                          min_quantity,
                          products_success,
                          bg_color):
        """
        Checks editing product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        products_page.find_product(product_name) # edit if need any other name
        products_page.edit_product_min_quantity(min_quantity)
        if products_page.alert_bg_color() == bg_color:
            print "\nAlert color is OK!"
            products_page.write_log("Alert color is OK!")
        assert products_success in products_page.success_alert()

    def test_delete_product(self,
                            products_page,
                            product_name,
                            products_success,
                            bg_color):
        """
        Checks deleting product at product page
        :param chosen_browser:
        :return: asserts if got success alert
        """
        products_page.find_product(product_name) # edit if need any other name
        products_page.delete_product()
        if products_page.alert_bg_color() == bg_color:
            print "\nAlert color is OK!"
            products_page.write_log("Alert color is OK!")
        assert products_success in products_page.success_alert()
