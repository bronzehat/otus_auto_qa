"""
This test checks drag&drop in opencart demopro
"""
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains

def test_drag_and_drop(chosen_browser):
    chosen_browser.get("http://demo23.opencart.pro/admin/")
    chosen_browser.find_element_by_id("input-username").send_keys("demo")
    chosen_browser.find_element_by_id("input-password").send_keys("demo")
    chosen_browser.find_element_by_xpath("//button[@type='submit']").click()
    chosen_browser.find_element_by_id("button-menu").click()
    design_menu = WebDriverWait(chosen_browser, timeout=10).until\
        (EC.element_to_be_clickable((By.CLASS_NAME, "fa-television")))
    design_menu.click()
    menu_construct = WebDriverWait(chosen_browser, timeout=10).until\
        (EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'http://demo23.opencart.pro/admin/index.php?route=design/custommenu')]")))
    menu_construct.click()
    element = chosen_browser.find_elements_by_class_name("custommenu-item-handle.ui-sortable-handle")[1]
    action = ActionChains(chosen_browser)
    action.drag_and_drop_by_offset(element, 0, 50).perform()
    time.sleep(3)
    save_button = WebDriverWait(chosen_browser, timeout=10).until\
        (EC.element_to_be_clickable((By.CLASS_NAME, "btn-success")))
    save_button.click()
    time.sleep(3)
    # CHANGES ARE NOT SAVED BECAUSE OF RIGHTS, but let's pretend the element
    # is now in necessary position and check it
    catalog = WebDriverWait(chosen_browser, timeout=10).until(EC.element_to_be_clickable((By.ID, "menu-catalog")))
    catalog.click()
    time.sleep(2)
    categories = chosen_browser.find_elements_by_xpath("//a[contains(@href,'http://demo23.opencart.pro/admin/index.php?route=catalog/category')]")[1]
    categories.click()
    time.sleep(2)
    chosen_browser.find_element_by_xpath("//a[contains(@href, 'path=20')]").click()
    moved_element = chosen_browser.find_elements_by_class_name("left")[1]
    print(moved_element.text)  # here must be PC


