"""
This short test is just for checking if the current base url is
our opencart for tests
"""

def test_if_opencart(chosen_browser, base_url, etalon_url):
    """
    Checks if the current page is our opencart for tests
    :param chosen_browser: browser defined in command line option
    --browser
    :param base_url: url defined in command line option
    --url
    :param etalon_url: url that must be
    :return: asserts if current url in browser equals to etalon
    """
    chosen_browser.get(base_url)
    assert chosen_browser.current_url == etalon_url
