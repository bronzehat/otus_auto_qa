"""
This module is for testing with argparse.
"""
import argparse
import requests
import pytest


URLS = ["https://dog.ceo/api/breeds/list/all",
        "https://api.openbrewerydb.org/breweries",
        "https://api.cdnjs.com/libraries"]


PARSER = argparse.ArgumentParser()
PARSER.add_argument("-addr", action="store", dest="addr",
                    help="run test for all or [dogs, brew, cdnjs]")
ARGS = PARSER.parse_args()
PARAMETER = ARGS.addr
RESULT = []
if PARAMETER == "all":
    RESULT = URLS
elif PARAMETER == "dogs":
    RESULT.append(URLS[0])
elif PARAMETER == "brew":
    RESULT.append(URLS[1])
elif PARAMETER == "cdnjs":
    RESULT.append(URLS[2])
else:
    print("No suitable URL! Print 'all' or dogs of brew or cdnjs")
    pytest.xfail("No suitable URL")


def argparsing(result):
    """
    This function gives status code of the given page
    :param result: is the list of URLs to run (depends on the
    command line argument
    :return: prints page responce's status code
    """
    if isinstance(result, list):
        for i in result:
            responce = requests.get(i)
            print(i, "status code:", responce.status_code)
    else:
        responce = requests.get(result)
        print(result, "status code:", responce.status_code)

for j in RESULT:
    argparsing(j)
