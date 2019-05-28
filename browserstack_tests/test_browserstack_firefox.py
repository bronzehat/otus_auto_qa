from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

desired_cap = {
 'browser': 'Firefox',
 'browser_version': '59.0',
 'os': 'Windows',
 'os_version': '7',
 'resolution': '1024x768'
}
city = "ufa"
group = "children of bodom"
driver = webdriver.Remote(
    command_executor='http://zelasayy1:CiQFg6yqPPrRrhz8r15C@hub.browserstack.com:80/wd/hub',
    desired_capabilities=desired_cap)
desired_cap['browserstack.local'] = True
desired_cap['browserstack.localIdentifier'] = 'Test123'
url = "".join(["https://kudago.com/", city])
print("URL: ", url)
driver.get(url)
driver.find_element_by_class_name("search-query").send_keys(group)
driver.find_element_by_class_name("search-submit").send_keys(Keys.ENTER)
sleep(2)
events = driver.find_elements_by_class_name("post-list-item-title")
if not events:
    print("\nNo events for %s in %s found" % (group, city))
else:
    for i in events:
        print(i.text)
driver.quit()