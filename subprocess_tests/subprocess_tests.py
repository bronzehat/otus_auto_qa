import subprocess
import re


def test_service_status(service):
    service_status = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    service_status_output = service_status.communicate()[0]
    try:
        if "active (running)" in service_status_output:
            print("\nService {} is active".format(service))
        else:
            print("\nService {} is stopped".format(service))
    except Exception as e:
        print(e)
    assert "active (running)" in service_status_output

def test_network_interface_state(net_int):
    if_state_regexp = re.compile(r'<(.*?),')
    print("")
    for i in net_int.keys():
        if_state = if_state_regexp.findall(net_int[i][0])
        print("Network interface {}'s state is: {}".format(i, if_state[0]))
        assert if_state[0] == "UP"

def test_os_version(os_attrs, ):
    print("")
    print("Operating system name: {}".format(os_attrs["NAME"]))
    print("Operating system version: {}".format(os_attrs["VERSION"]))
    assert "Ubuntu" in os_attrs["NAME"]

def test_cpu_cores(cpuinfo):
    cpu_cores_count = 0
    for attr in cpuinfo:
        if attr[0] == 'cpu cores':
            cpu_cores_count += int(attr[1])
    print("\nNumber of CPU cores: {}".format(cpu_cores_count))
    assert cpu_cores_count >= 2

