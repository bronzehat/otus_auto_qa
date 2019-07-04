import pytest
import subprocess


def pytest_addoption(parser):
    """
    Adds a commandline options for tests
    :param parser:
    :return:
        """
    parser.addoption("--dir", action="store", dest="dir", type=str, default="/home/asayapova",
                    help="type the dir to get files/dirs list from it")
    parser.addoption("--pack", action="store", dest="pack", type=str, default="firefox",
                    help="type the pack to get its version")
    parser.addoption("--protocol", action="store", dest="protocol", type=str, default="tcp",
                    help="type the protocol to check ports for")
    parser.addoption("--service", action="store", dest="service", type=str,
                    default="mysql.service")

@pytest.fixture
def service(request):
    return request.config.getoption("--service")

@pytest.fixture
def net_int():
    ifconfig = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    ifconfig_output = ifconfig.communicate()[0]
    ifconfig_dict = {}
    for i in ifconfig_output.split("\n\n"):
        if ": " in i:
            if_info = str(i.split(": ")[1]).split("\n")
            for if_attrib in if_info: if_attrib.rstrip()
            ifconfig_dict[i.split(": ")[0]] = if_info
    return ifconfig_dict

@pytest.fixture
def os_attrs():
    os_version = subprocess.Popen(["cat", "/etc/os-release"], stdout=subprocess.PIPE)
    os_version_output = os_version.communicate()[0]
    os_attrs_dict = {}
    for line in os_version_output.split("\n"):
        os_attrs_lines =  line.split("=")
        if len(os_attrs_lines) == 2:
            os_attrs_dict[os_attrs_lines[0]] = os_attrs_lines[1]
    return os_attrs_dict

@pytest.fixture
def cpuinfo():
    with open("/proc/cpuinfo", "r") as f:
        cpuinfo = f.readlines()
    cpu_attrs = []
    for i in cpuinfo:
        cpu_attr_list = i.split(":")
        if len(cpu_attr_list) == 2:
            cpu_attrs.append([cpu_attr_list[0].rstrip(), cpu_attr_list[1].rstrip()])
    return cpu_attrs
