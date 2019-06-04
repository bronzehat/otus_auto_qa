import pytest
import re
from collections import Counter
import json


def test_parsing_webserver_logs(file, host_ip):
    """
    Parses logfile (or logfiles, if directory is set by cmd option '--dir'
    and then writes into json file data about TOP IPs, total requests count, GET/POST requests count: get_count,
    TOP client errors, TOP server errors, TOP longest requests (TOP is given in a top_count variable)
    :param file:
    :param host_ip:
    :return:
    """

    ip_regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"   # regexp for searching ip in logfile
    client_error_regexp = r'" 4\d{2} '  # 4xx number
    server_error_regexp = r'" 5\d{2} '  # 5xx number
    request_time_regexp = r'] \d+ "'    # any number between ] and " (configured apache's /D (request time by
                                        # microseconds logging parameter to be between these symbols)

    values = {}
    total_values = {"PARSED LOGS": values}
    top_count = "10"

    open('log_parse.json', 'w').close() # clears json-file for every test run

    def copy_unique_elements(list_of_all):
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

    def findall_unique_exps(regexp, data):
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
        return copy_unique_elements(sorted_list)

    def findall_unique_exps_lines(regexp, logfile):
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
        return copy_unique_elements(list_of_all)

    def requests_count(regexp, data):
        """
        Returns requests count containing expression like 'GET' or 'POST'
        :param regexp:
        :param data:
        :return:
        """
        requests_list = re.findall(regexp, data)
        return int(list(Counter(requests_list).values())[0])

    def requests_exec_time_list(regexp, data, logfile):
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

    def parse(log):
        print('\n{}'.format(log))  # to see what log was parsed
        unique_client_error_lines_list = findall_unique_exps_lines(client_error_regexp, log)
        unique_server_error_lines_list = findall_unique_exps_lines(server_error_regexp, log)

        with open(log) as f:
            data = f.read()

        unique_ips_list = findall_unique_exps(ip_regexp, data)

        get_count = requests_count('GET', data)
        post_count = requests_count('POST', data)

        total_requests_count = get_count + post_count

        top_request_lines = requests_exec_time_list(request_time_regexp, data, log)

        with open('log_parse.json', 'a') as json_file:
            values["{}".format(log)] = {'TOP {} IPs'.format(top_count): unique_ips_list,
                                        'Total requests count':  total_requests_count,
                                        'GET requests count': get_count,
                                        'POST requests count': post_count,
                                        'TOP {} client errors'.format(top_count): unique_client_error_lines_list,
                                        'TOP {} server errors'.format(top_count): unique_server_error_lines_list,
                                        'TOP {} longest requests'.format(top_count):  top_request_lines}
            json.dump(total_values, json_file)

    if isinstance(file, list):
        for i in file:
            try:
                parse(i)
            except UnicodeDecodeError:
                print("File wasn't parsed (check format) ({})".format(file))
                pass
    else:
        try:
            parse(file)
        except UnicodeDecodeError:
            print("File wasn't parsed (check format) ({})".format(file))
