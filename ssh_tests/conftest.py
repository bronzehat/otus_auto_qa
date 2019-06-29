import pytest
from ftplib import FTP, error_reply, error_perm
from os import chdir, getcwd

hostname = '192.168.85.154'
user = 'asayapova'
password='o9p0[-]='
upload_filename = "\\screens\\test_ssh_opencart_terminal_screen.png"
download_filename = "testfile"
downloads = "".join([getcwd(),"\downloads\\"])
dir = "test_dir"
path = "/home/asayapova/PycharmProjects"

def pytest_addoption(parser):
    """
    Adds a commandline options for tests
    :param parser:
    :return:
        """
    parser.addoption(
        "--hostname", action="store", dest="hostname", type=str, default=hostname,
        help="choose the host to connect by FTP"
        )
    parser.addoption(
        "--user", action="store", dest="user", type=str, default=user,
        help="choose a user to to connect by FTP"
    )
    parser.addoption(
        "--password", action="store", dest="password", type=str, default=password,
        help="choose a password for the user to connect by FTP"
    )
    parser.addoption(
        "--upload", action="store", dest="upload", type=str, default=upload_filename,
        help="choose a filename to upload to the host by FTP"
    )
    parser.addoption(
        "--download", action="store", dest="download", type=str, default=download_filename,
        help="choose a filename to download to the host by FTP"
    )
    parser.addoption(
        "--downloads", action="store", dest="downloads", type=str, default=downloads,
        help="choose a directory to file downloads from the host by FTP"
    )
    parser.addoption(
        "--new_dir", action="store", dest="new_dir", type=str, default=dir,
        help="choose a new directory name to create on the host by FTP"
    )
    parser.addoption(
        "--work_path", action="store", dest="workpath", type=str, default=path,
        help="choose a directory to open on the host"
    )


@pytest.fixture(scope="session")
def ftp_connect(request):
    hostname = request.config.getoption("--hostname")
    ftp = FTP(hostname)
    ftp.connect(hostname)
    user = request.config.getoption("--user")
    password = request.config.getoption("--password")
    try:
        ftp.login(user=user, passwd=password)
    except error_perm as e:
        print("\nPermission error occured while logging in, exception:", e)
    except error_reply as e:
        print("\nError occured while logging in, exception:", e)
    request.addfinalizer(ftp.quit)
    return ftp

@pytest.fixture
def ftp_hostname(request):
    return request.config.getoption("--hostname")

@pytest.fixture
def ftp_user(request):
    return request.config.getoption("--user")

@pytest.fixture
def ftp_password(request):
    return request.config.getoption("--password")

@pytest.fixture
def upload_file (request):
    return str(request.config.getoption("--upload"))

@pytest.fixture
def download_file(request):
    return request.config.getoption("--download")

@pytest.fixture
def downloads_dir(request):
    return request.config.getoption("--downloads")

@pytest.fixture
def new_dir(request):
    return request.config.getoption("--new_dir")

@pytest.fixture
def work_path(request):
    return request.config.getoption("--work_path")
