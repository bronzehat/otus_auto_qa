import subprocess
import argparse
import re

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--protocol", action="store", dest="protocol", type=str, default="tcp",
                    help="choose a protocol to check ports for")
PARSER.add_argument("--dir", action="store", dest="dir", type=str, default="/home/asayapova",
                    help="choose a dir to find files and dirs in")
PARSER.add_argument("--package", action="store", dest="pack", type=str, default="firefox",
                    help="choose a package to find its info")
PARSER.add_argument("--os-attr", action="append", dest="os_attr", default=["NAME", "VERSION"],
                    help="choose attributes to find in OS info")
PARSER.add_argument("--cpu-param", action="store", dest="cpu_param", type=str, default="CPU(s)",
                    help="choose an attribute to find in CPU's information")
PARSER.add_argument("--process-param", action="store", dest="process_param", type=str, default="desktop",
                    help="choose an attribute to find process by")
PARSER.add_argument("--service", action="store", dest="service", type=str, default="mysql.service",
                    help="choose a service to check its status")
PARSER.add_argument("--full", action="store_true", dest="full", default=False,
                    help="choose more detailed information is needed (prints whole lists and dicts,"
                         "not only single parameter")

ARGS = PARSER.parse_args()
protocol = ARGS.protocol
dir = ARGS.dir
cpu_param = ARGS.cpu_param
full = ARGS.full
process_param = ARGS.process_param
service = ARGS.service
pack = ARGS.pack
os_attr = ARGS.os_attr


# Check CPU attrs with lscpu command
def lscpu_check(param):
    lscpu = subprocess.Popen("lscpu", stdout=subprocess.PIPE)
    lscpu_output = lscpu.communicate()[0]
    lscpu_dict = {}
    for i in lscpu_output.split("\n"):
        cpu_attr = i.split(":")
        if len(cpu_attr) == 2:
            lscpu_dict[cpu_attr[0]] = cpu_attr[1].strip()
    if full:
        print("All CPU parameters:\n{}".format(lscpu_dict))
    print("Attribute '{}' from CPU info has value: {}".format(param, lscpu_dict[param]))


# Check network interfaces
def get_network_interfaces_info():
    ifconfig = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    ifconfig_output = ifconfig.communicate()[0]
    ifconfig_dict = {}
    for i in ifconfig_output.split("\n\n"):
        if ": " in i:
            if_info = str(i.split(": ")[1]).split("\n")
            for if_attrib in if_info: if_attrib.rstrip()
            ifconfig_dict[i.split(": ")[0]] = if_info
    print("\nNetwork interfaces:")
    for i in ifconfig_dict:
        print(i)
    if_state_regexp = re.compile(r'<(.*?),')
    print("\nNetwork interfaces' state:")
    for i in ifconfig_dict:
        if_state = if_state_regexp.findall(ifconfig_dict[i][0])
        print("{}'s state: {}".format(i, if_state[0]))
    ip_regexp = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    print("Network interfaces IPs:")
    for i in ifconfig_dict:
        if_ip = ip_regexp.findall(ifconfig_dict[i][1])
        print("{}'s IP: {}".format(i, if_ip[0]))


# Check network interfaces statistics
def network_statistics():
    ip_link = subprocess.Popen(["ip", "-s", "link"], stdout=subprocess.PIPE)
    ip_link_output = ip_link.communicate()[0]
    print("\nNetwork interfaces statistics:")
    print(ip_link_output)


# Check default IP route info
def def_ip_route_check():
    iproute = subprocess.Popen(['ip', 'route', 'show'], stdout=subprocess.PIPE)
    iproute_output = iproute.communicate()[0]
    for i in iproute_output.split("\n"):
        if "default" in i:
            print("Default route: {}\n".format(i))


# Check ports state by protocol
def ports_by_protocol_check(protocol):
    if protocol == "tcp":
        port_state_key = "-lt"
    elif protocol == "udp":
        port_state_key = "-lu"
    port_state = subprocess.Popen(['netstat', port_state_key], stdout=subprocess.PIPE)
    port_state_output = port_state.communicate()[0]
    print("Ports state for protocol {}:".format(protocol))
    print(port_state_output)


# Check processes (by keyword and if --full option chosen, the whole list too)
def processes_check(param):
    ps = subprocess.Popen(["ps", "-aux"], stdout=subprocess.PIPE)
    ps_output = ps.communicate()[0]
    ps_list = ps_output.split("\n")
    for i in ps_list:
        i.strip()
        if i == "":
            ps_list.remove(i)
    if full:
        print("List of all processes:\n{}".format(ps_list[1:]))
    print("Processes by keyword '{}':".format(param))
    count = 0
    for i in ps_list:
        if param in i:
            count+=1
            print("{}. {}\n".format(count, i))


# Check service status
def service_status(service):
    service_status = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE)
    service_status_output = service_status.communicate()[0]
    try:
        if "active (running)" in service_status_output:
            print("Service {} is active\n".format(service))
        else:
            print("Service {} is stopped\n".format(service))
    except Exception as e:
        print(e)


# Check package version
def package_info(pack):
    package_version = subprocess.Popen(["dpkg", "--list", pack], stdout=subprocess.PIPE)
    package_version_output = package_version.communicate()[0]
    print(package_version_output)


# Check files and dirs count in given dir (and the whole list of them if --full option chosen
def ls(dir):
    file_list = subprocess.Popen(["ls", "-la", dir], stdout=subprocess.PIPE)
    file_list_output = file_list.communicate()[0]
    if full:
        print("File list in directory '{}':".format(dir))
    files_in_dir = []
    dirs_in_dir = []
    for line in file_list_output.split("\n"):
        if line.startswith("-"):
            files_in_dir.append(line)
        elif line.startswith("d"):
            dirs_in_dir.append(line)
    print("Files in dir '{}' (total count: {})".format(dir, len(files_in_dir)))
    if full:
        for i in files_in_dir:
            print(i)
    print("Dirs in dir '{}' (total count: {})".format(dir, len(dirs_in_dir)))
    if full:
        for j in dirs_in_dir:
            print(j)


# Check current dir
def get_current_dir():
    cur_dir = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
    cur_dir_output = cur_dir.communicate()[0]
    print("\nCurrent directory: {}".format(cur_dir_output))


# Check OS Version
def get_os_attrs(attrs):
    os_version = subprocess.Popen(["cat", "/etc/os-release"], stdout=subprocess.PIPE)
    os_version_output = os_version.communicate()[0]
    os_attrs = {}
    for line in os_version_output.split("\n"):
        os_attrs_keyvalue =  line.split("=")
        if len(os_attrs_keyvalue) == 2:
            os_attrs[os_attrs_keyvalue[0]] = os_attrs_keyvalue[1]
    if type(attrs) == list:
        for i in attrs:
            if os_attrs[i]:
                print("Operating system attribute {}: {}".format(i, os_attrs[i]))
    elif type(attrs) == str:
        if os_attrs[attrs]:
            print("Operating system attribute {}: {}".format(attrs, os_attrs[attrs]))

def get_platform_version():
    print("Platform info:")
    with open("/proc/version") as f:
        for i in f.read().split("\n"):
            print(i)

lscpu_check(cpu_param)
get_network_interfaces_info()
network_statistics()
def_ip_route_check()
ports_by_protocol_check(protocol)
processes_check(process_param)
service_status(service)
package_info(pack)
ls(dir)
get_current_dir()
get_os_attrs(os_attr)
get_platform_version()