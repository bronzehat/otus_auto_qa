"""
These tests are common and exist to check you can work with
the given URLs
"""
import requests


def test_status200(url):
    """
    Ensures that the given URLs exist and the status code is 200
    :param base_url: a fixture with a list of url
    :return:
    """
    if isinstance(url, list):
        for i in url:
            responce = requests.get(i)
            print(i, "status code:", responce.status_code)
    else:
        responce = requests.get(url)
        print(url, "status code:", responce.status_code)
        assert responce.status_code == 200


def test_page_elements_count(url):
    """
    Counts page elements number through the json length
    :param base_url:
    :return:
    """
    if isinstance(url, list):
        for i in url:
            responce = requests.get(i)
            count = len(responce.json())
            print(i + 'page\'s elements count: ' + str(count))
    else:
        responce = requests.get(url)
        count = len(responce.json())
        print(url + 'page\'s elements count: ' + str(count))
