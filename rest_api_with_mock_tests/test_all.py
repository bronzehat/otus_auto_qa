"""
These tests are common and exist to check you can work with
the given URLs
"""


def test_status200(url):
    """
    Ensures that the given URLs exist and the status code is 200
    :param base_url: a fixture with a list of url
    :return:
    """
    print()
    if isinstance(url, list):
        for i in url:
            print(i.name(), "status code:", i.get_responce_code())
            assert i.get_responce_code() == 200
    else:
        print(url.name(), "status code:", url.get_responce_code())
        assert url.get_responce_code() == 200


def test_page_elements_count(url):
    """
    Counts page elements number through the json length
    :param base_url:
    :return:
    """
    print()
    if isinstance(url, list):
        for i in url:
            print(i.name(), 'page\'s elements count: ', i.elements_count())
            assert i.elements_count() > 0, "Given URL has 0 elements"
    else:
        print(url.name(), 'page\'s elements count: ', url.elements_count())
        assert url.elements_count() > 0, "Given URL has 0 elements"
