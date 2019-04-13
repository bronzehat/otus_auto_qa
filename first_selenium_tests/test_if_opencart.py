"""
This short test is just for checking if the current base url is
our opencart for tests
"""

def test_if_opencart(chosen_browser, base_url):
    """
    the current page is our opencart for tests
    """
    chosen_browser.get(base_url)
    assert chosen_browser.current_url == "http://localhost/opencart/"
