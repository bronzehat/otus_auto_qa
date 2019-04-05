"""
These tests are common and exist to check you can work with
the given URLs
"""
import requests


def test_status200(base_url):
    """
    Ensures that the given URLs exist and the status code is 200
    :param base_url: a fixture with a list of url
    :return:
    """
    responce = requests.get(base_url)
    assert responce.status_code == 200


def test_page_elements_count(base_url):
    """
    Counts page elements number through the json length
    :param base_url:
    :return:
    """
    responce = requests.get(base_url)
    count = len(responce.json())
    print(base_url + 'page\'s elements count: ' + str(count))