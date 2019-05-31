"""
This test checks concerts in different sites
"""
import pytest
import os
import platform
import allure
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@allure.feature("events_search")
@allure.step
@allure.severity(allure.severity_level.BLOCKER)
def test_kassir(chosen_browser, city, group):
    site = "".join(["https://", city, ".kassir.ru"])
    chosen_browser.get(site)
    sleep(2)
    search = chosen_browser.find_element_by_id("js_head_search")
    search.send_keys(group)
    search.send_keys(Keys.ENTER)
    sleep(2)
    try:
        print("***********************************************")
        events = chosen_browser.find_elements_by_class_name("caption")
        for i in events:
            print(i.text)
        print("***********************************************")
        if "Windows" in platform.platform():
            screen_kassir_path = "".join([os.getcwd(), r"\screenshots\event_kassir.png"])
        else:
            screen_kassir_path = "".join([os.getcwd(), "/screenshots/event_kassir.png"])
        if os.path.isfile(screen_kassir_path):
            os.remove(screen_kassir_path)
        chosen_browser.save_screenshot(screen_kassir_path)
        allure.attach.file(screen_kassir_path)
    except NoSuchElementException:
        print("No concerts of %s in %s found" % (group, city))
    except TimeoutException:
        print("Time out occured while searching by group %s in city %s" % (group, city))

@allure.feature("events_search")
@allure.severity(allure.severity_level.CRITICAL)
def test_fangid(chosen_browser, city_rus, city, group):
    site = "https://fangid.com"
    chosen_browser.get(site)
    chosen_browser.find_element_by_xpath("//span[contains(@class, 'sni-name') and text() = '%s']" % city_rus).click()
    sleep(3)
    events = chosen_browser.find_elements_by_xpath("//*[contains(@class, 'as-title') and text() = '%s']" % group)
    if "Windows" in platform.platform():
        screen_fangid_path = "".join([os.getcwd(), r"\screenshots\event_fangid.png"])
    else:
        screen_fangid_path = "".join([os.getcwd(), "/screenshots/event_fangid.png"])
    if os.path.isfile(screen_fangid_path):
        os.remove(screen_fangid_path)
    if len(events) > 0:
        chosen_browser.execute_script("arguments[0].scrollIntoView();", events[0])
        chosen_browser.save_screenshot(screen_fangid_path)
        allure.attach.file(screen_fangid_path)
        for i in events:
            i.click()
            info = chosen_browser.find_elements_by_class_name("acii-content")
            print("***********************************************")
            for i in info:
                print(i.text)
                print("")
            print("***********************************************")
            chosen_browser.back()
    else:
        print("No concerts of %s in %s found" % (group, city))

@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("Tests just for quantity")
@allure.testcase("https://google.com", "Second link just for allure report")
@allure.issue("https://yandex.ru", "First link just for allure report")
def test_for_allure_xfail():
    pytest.xfail("this test is just for allure report")

@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("Tests just for quantity")
@allure.description("This test is always skipped")
@allure.title("Alternative title for test_for_allure_skip")
def test_for_allure_skip():
    pytest.skip("this test is just for allure report")

@allure.severity(allure.severity_level.TRIVIAL)
@allure.step
@allure.epic("Tests just for quantity")
@allure.description("This is text for dynamic allure description, let's see if it's modified")
def test_for_allure_fail():
    allure.dynamic.description("Final description. This test always fails")
    assert 2 == 1
