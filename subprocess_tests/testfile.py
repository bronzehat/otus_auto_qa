import subprocess
import sys
import os
import argparse
import pytest
import re

PARSER = argparse.ArgumentParser()
# PARSER.add_argument("--proc", action="store", dest="hostname", type=str, default="192.168.85.154",
#                     help="type one the /proc files to parse")
# PARSER.add_argument("--url", action="store", dest="url", type=str, default="/opencart/index.php",
#                     help="type the URL to connect")
# PARSER.add_argument("--method", action="store", dest="method", type=str, default="GET",
#                     help="type the method to use")
# PARSER.add_argument("--header", action="append", dest="header", type=dict,
#                     default={"Content-Type": "text/html; charset=utf-8"},
#                     help='type header to use')
# PARSER.add_argument("--capabilities", action="append", dest="cap", type=dict,
#                     default={"capabilities": {}, "desiredCapabilities": {}},
#                     help='type capabilities to send to browser')
# PARSER.add_argument("--printpage", action="store_true", dest="printpage",
#                     default=False,
#                     help='choose if you want to print whole page text')
# PARSER.add_argument("--detailed", action="store_true", dest="detailed",
#                     default=False,
#                     help='choose if you want to print detailed info: not only quantity, but elements too')
# ARGS = PARSER.parse_args()
# hostname = ARGS.hostname
# url = "".join(["http://", hostname, ARGS.url])
# method = ARGS.method
# header = ARGS.header
# capabilities = ARGS.cap
# detailed = ARGS.detailed
# printpage = ARGS.printpage


# # CPU info
with open("/proc/cpuinfo", "r") as f:
    cpuinfo = f.readlines()
processor_count = 0
for i in cpuinfo:
    if i.startswith("processor"):
        processor_count+=1
print("Found number of processors: {}".format(processor_count))
cpu_dict = {}
for i in cpuinfo:
    cpu_keyvalue_list = i.split(":")
    if len(cpu_keyvalue_list) == 2:
        cpu_dict[cpu_keyvalue_list[0].rstrip()] = cpu_keyvalue_list[1].rstrip()
if "model name" in cpu_dict.keys():
    print("Found model name:{}".format(cpu_dict["model name"]))

# # Network interfaces
#
# # ls /sys/class/net gives all the interfaces
# find_interfaces = subprocess.Popen(['ls', '/sys/class/net'], stdout=subprocess.PIPE)
# interfaces = find_interfaces.communicate()[0]
# print("Found network interfaces:\n{}".format(interfaces.rstrip()))
#
# # cat /sys/class/net/ens33/operstate gives up or down
# for i in interfaces.split("\n"):
#     if i:
#         if_up_check = subprocess.Popen(['cat', '/sys/class/net/{}/operstate'.format(i)], stdout=subprocess.PIPE)
#         if_state = if_up_check.communicate()[0]
#         print("Network interface {} state is {}".format(i, if_state.rstrip()))

ifconfig = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
ifconfig_output = ifconfig.communicate()[0]
ifconfig_list = []
ifconfig_dict = {}
for i in ifconfig_output.split("\n\n"):
    if ": " in i:
        if_info = str(i.split(": ")[1]).split("\n")
        for if_attrib in if_info: if_attrib.rstrip()
        ifconfig_dict[i.split(": ")[0]] = if_info
print(ifconfig_dict)
for i in ifconfig_dict: print("Found network interface: {}".format(i))
if_state_regexp = re.compile(r'<(.*?),')
for i in ifconfig_dict:
    if_state = if_state_regexp.findall(ifconfig_dict[i][0])
    print("Network interface {}'s state is: {}".format(i, if_state[0]))
