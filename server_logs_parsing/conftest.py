import pytest
from os import getcwd
from os import listdir
from os.path import isfile, join, getsize
import platform
import socket

if "Windows" in platform.platform():
    system = "windows"
    slash = "\\"
else:
    system = "linux"
    slash = "/"

current_dir = getcwd()


def pytest_addoption(parser):
    """
    Adds a commandline options for tests
    :param parser:
    :return:
        """
    parser.addoption(
        "--dir", action="store", dest="directory", type=str, default=None,
        help="choose a directory for logs to parse"
        )
    parser.addoption(
        "--file", action="store", dest="file", type=str, default=None,
        help="choose a logfile to parse"
    )

@pytest.fixture()
def file(request):
    """
    Returns path to file which will be parsed.
    If the directory is not set, by default current directory is set.
    If directory is set, but a file not, it returns the list of all files in it.
    :param request:
    :return:
    """
    defined_file = request.config.getoption("--file")
    defined_dir = request.config.getoption("--dir")
    if defined_file and not defined_dir:
        path = "".join([current_dir, slash, defined_file])
        if getsize(path) > 0:
            return path
        else:
            raise Exception("Defined file is empty ({})".format(path))
    elif defined_file and defined_dir:
        path = "".join([defined_dir, slash, defined_file])
        if getsize(path) > 0:
            return path
        else:
            raise Exception("Defined file is empty ({})".format(path))
    elif not defined_file and defined_dir:
        if not listdir(defined_dir):
            raise Exception("There are no files in given --dir ({})".format(defined_dir))
        else:
            defined_dir_files = ["".join([defined_dir, slash, f]) for f
                                 in listdir(defined_dir) if isfile(join(defined_dir, f))]
        return defined_dir_files
    else:
        raise Exception("Define at least one of --dir or --file options! Pay attention on README.txt, please")

@pytest.fixture(scope="session")
def host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip