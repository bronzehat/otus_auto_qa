"""
This test checks concerts in different sites
"""
import pytest
import socket
from time import sleep
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


print("Hostname: ", socket.gethostname())

def test_kassir(chosen_browser, city, group):
    driver = chosen_browser
    url = "".join(["https://", city, ".kassir.ru/"])
    driver.get(url)
    driver.find_element_by_id("js_head_search").send_keys(group)
    driver.find_element_by_id("js_head_search").send_keys(Keys.ENTER)
    sleep(2)
    try:
        print("***********************************************")
        events = driver.find_elements_by_class_name("caption")
        for i in events:
            print(i.text)
        print("***********************************************")
    except NoSuchElementException:
        print("No concerts of %s in %s found" % (group, city))
    except TimeoutException:
        print("Time out occured while searching by group %s in city %s" % (group, city))
