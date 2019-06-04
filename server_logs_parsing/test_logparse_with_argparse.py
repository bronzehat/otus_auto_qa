"""
This module is for testing with argparse.
"""
import argparse
from os import getcwd
from os import listdir
from os.path import isfile, join, getsize
import platform
import re
from collections import Counter
import json
from os import path

ip_regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"   # regexp for searching ip in logfile
client_error_regexp = r'" 4\d{2} '  # 4xx number
server_error_regexp = r'" 5\d{2} '  # 5xx number
request_time_regexp = r'] \d+ "'    # any number between ] and " (configured apache's /D (request time by
                                    # microseconds logging parameter to be between these symbols)
timestamp_regexp = r'\d{2}/\D+/\d{4}:\d{2}:\d{2}:\d{2}'

values = {}
top_count = "10"

if "Windows" in platform.platform():
    system = "windows"
    slash = "\\"
else:
    system = "linux"
    slash = "/"

current_dir = getcwd()

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--dir", action="store", dest="directory", type=str, default=None,
                    help="choose a directory for logs to parse")
PARSER.add_argument("--file", action="store", dest="file", type=str, default=None,
                    help="choose a logfile to parse")
ARGS = PARSER.parse_args()
defined_dir = ARGS.directory
defined_file = ARGS.file


class LogParser:

    def file(self):
        if defined_file and not defined_dir:
            path_to_file = "".join([current_dir, slash, defined_file])
            if getsize(path_to_file) > 0:
                return path_to_file
            else:
                raise Exception("Defined file is empty ({})".format(path))
        elif defined_file and defined_dir:
            path_to_file = "".join([defined_dir, slash, defined_file])
            if getsize(path_to_file) > 0:
                return path_to_file
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

    def copy_unique_elements(self, list_of_all):
        """
        Copies unique elements from list to unique_list
        :param list_of_all:
        :return:
        """
        unique_list = []
        for i in list_of_all:
            if i not in unique_list:
                unique_list.append(i)
            if len(unique_list) == int(top_count):
                break
        return unique_list

    def findall_unique_exps(self, regexp, data):
        """
        Returns list of unique expressions in data (may be limited by length
        if copy_unique_elements function's used)
        :param regexp:
        :param data:
        :return:
        """
        list_of_all = re.findall(regexp, data)
        count = Counter(list_of_all)
        sorted_list = sorted(list_of_all, key=lambda x: (count[x], x), reverse=True)
        return self.copy_unique_elements(sorted_list)

    def findall_unique_exps_lines(self, regexp, logfile):
        """
        Returns a list of lines with unique expressions in logfile (may be limited by length
        if copy_unique_elements function's used)
        :param regexp:
        :param logfile:
        :return:
        """
        list_of_all = []
        with open(logfile) as logfile:
            for line in logfile:
                exp = re.compile(regexp)
                if exp.search(line):
                    list_of_all.append(line)
        return self.copy_unique_elements(list_of_all)

    def requests_count(self, regexp, data):
        """
        Returns requests count containing expression like 'GET' or 'POST'
        :param regexp:
        :param data:
        :return:
        """
        requests_list = re.findall(regexp, data)
        return int(list(Counter(requests_list).values())[0])

    def requests_exec_time_list(self, regexp, data, logfile):
        """
        Returns lines with longest requests (number of lines is set in top_count variable)
        :param regexp:
        :param data:
        :param logfile:
        :return:
        """
        # find every request time and add to collection
        request_time_list = re.findall(regexp, data)
        request_time_count = Counter(request_time_list)
        sorted_request_time_list = sorted(request_time_list, key=lambda x: (request_time_count[x], x), reverse=True)
        # convert strings in requests time integer values
        for index, item in enumerate(sorted_request_time_list):
            sorted_request_time_list[index] = int(''.join(c for c in item if c.isdigit()))
        # collect top <top_count> longest requests
        top_request_time_list = []
        for i in range(int(top_count)):
            max_request = max(sorted_request_time_list)
            top_request_time_list.append(max_request)
            sorted_request_time_list.remove(max_request)
        # search top <top_count> longest requests in a file and collect lines with them to a list
        top_request_lines = []
        with open(logfile) as f:
            for line in f:
                for i in top_request_time_list:
                    if str(i) in line:
                        top_request_lines.append(line)
        return top_request_lines

    def parse(self, log):
        json_file_name = 'log_parse.json'
        open(json_file_name, 'w').close()  # clears json-file for every test run

        print('\nParsed log is {}'.format(log))  # to see what log was parsed
        #
        unique_client_error_lines_list = self.findall_unique_exps_lines(client_error_regexp, log)
        unique_server_error_lines_list = self.findall_unique_exps_lines(server_error_regexp, log)

        with open(log) as f:
            data = f.read()

        unique_ips_list = self.findall_unique_exps(ip_regexp, data)

        get_count = self.requests_count('GET', data)
        post_count = self.requests_count('POST', data)

        total_requests_count = get_count + post_count

        top_request_lines = self.requests_exec_time_list(request_time_regexp, data, log)

        with open(json_file_name, 'w') as json_file:
            values["{}".format(log)] = {'TOP {} IPs'.format(top_count): unique_ips_list,
                                        'Total requests count':  total_requests_count,
                                        'GET requests count': get_count,
                                        'POST requests count': post_count,
                                        'TOP {} client errors'.format(top_count): unique_client_error_lines_list,
                                        'TOP {} server errors'.format(top_count): unique_server_error_lines_list,
                                        'TOP {} longest requests'.format(top_count):  top_request_lines}
            json.dump(values, json_file)

logparser = LogParser()
logfile = logparser.file()

if isinstance(logfile, list):
    for i in logfile:
        try:
            logparser.parse(i)
        except UnicodeDecodeError:
            print("File wasn't parsed (check format) ({})".format(i))
            pass
else:
    try:
        logparser.parse(logfile)
    except UnicodeDecodeError:
        print("File wasn't parsed (check format) ({})".format(logfile))
