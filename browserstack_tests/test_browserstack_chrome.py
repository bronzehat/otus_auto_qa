"""
This test checks concerts in different sites
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


city = "ufa"
group = "Children of Bodom"

desired_cap = {
 'browser': 'Chrome',
 'browser_version': '74.0',
 'os': 'Windows',
 'os_version': '7',
 'resolution': '1024x768',
 'name': 'Bstack-[Python] Sample Test'
}

driver = webdriver.Remote(
    command_executor='http://zelasayy1:CiQFg6yqPPrRrhz8r15C@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)

url = "".join(["https://", city, ".kassir.ru/"])
print("URL: ", url)
driver.get(url)
search = driver.find_element_by_id("js_head_search")
search.send_keys(group)
search.send_keys(Keys.ENTER)
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
driver.quit()
#
# import pytest
# import socket
# from time import sleep
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
#
#
# print("Hostname: ", socket.gethostname())
#
# def test_kassir(chosen_browser, city, group):
#     driver = chosen_browser
#     url = "".join(["https://", city, ".kassir.ru/"])
#     driver.get(url)
#     driver.find_element_by_id("js_head_search").send_keys(group)
#     driver.find_element_by_id("js_head_search").send_keys(Keys.ENTER)
#     sleep(2)
#     try:
#         print("***********************************************")
#         events = driver.find_elements_by_class_name("caption")
#         for i in events:
#             print(i.text)
#         print("***********************************************")
#     except NoSuchElementException:
#         print("No concerts of %s in %s found" % (group, city))
#     except TimeoutException:
#         print("Time out occured while searching by group %s in city %s" % (group, city))
