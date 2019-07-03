"""
This is a script parsing html page through socket lib.
If you wish more detailed output, use --detailed option.
If you wish the received page text to be printed, use --printpage option.
Page is saved in saved_page.html by default.
"""
import socket
import argparse
from html.parser import HTMLParser
import re

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--hostname", action="store", dest="hostname", type=str, default="192.168.85.154",
                    help="type the hostname to connect")
PARSER.add_argument("--url", action="store", dest="url", type=str, default="/opencart/index.php",
                    help="type the URL to connect")
PARSER.add_argument("--method", action="store", dest="method", type=str, default="GET",
                    help="type the method to use")
PARSER.add_argument("--header", action="append", dest="header", type=dict,
                    default={"Content-Type": "text/html; charset=utf-8"},
                    help='type header to use')
PARSER.add_argument("--capabilities", action="append", dest="cap", type=dict,
                    default={"capabilities": {}, "desiredCapabilities": {}},
                    help='type capabilities to send to browser')
PARSER.add_argument("--printpage", action="store_true", dest="printpage",
                    default=False,
                    help='choose if you want to print whole page text')
PARSER.add_argument("--detailed", action="store_true", dest="detailed",
                    default=False,
                    help='choose if you want to print detailed info: not only quantity, but elements too')
ARGS = PARSER.parse_args()
hostname = ARGS.hostname
url = "".join(["http://", hostname, ARGS.url])
method = ARGS.method
header = ARGS.header
capabilities = ARGS.cap
detailed = ARGS.detailed
printpage = ARGS.printpage

# Regexp for search in page text
images_regexp = re.compile(r'<img [^>]*src="([^"]+)')
links_regexp = re.compile(r'<a [^>]*href="([^"]+)')

# Form the message to send
message_list = [method, " ", ARGS.url, " HTTP/1.0\r\n", "Host: ", hostname, ":80\r\n"]
for i in header:
    message_list.append("".join([i, ": ", header[i], "\r\n"]))
if capabilities:
    message_list.append("\r\n{")
    for i in capabilities:
        message_list.append("".join([i, ": ", str(capabilities[i])]))
        message_list.append(", ")
    message_list.append("}")
message_list.append("\r\n")
message = "".join(message_list)
print("*********************************************************")
print("Sent message:")
print(message)
print("*********************************************************")


def count_images_on_page(data):
    """
    Counts images on page by regexp
    :param data:
    :return:
    """
    img = images_regexp.findall(data)
    print("Images count on page:", len(img))
    if detailed:
        print(img)
    print("*********************************************************")


def count_links_on_page(data):
    """
    Counts links on page by regexp
    :param data:
    :return:
    """
    lnk = links_regexp.findall(data)
    print("Links count on page:", len(lnk))
    if detailed:
        print(lnk)
    print("*********************************************************")


def get_responce_code(data):
    """
    Checks responce code on the page
    :param data:
    :return:
    """
    for line in data.split("\n"):
        if line.startswith("HTTP"):
            print("Responce code:", line.split(" ")[1])
    print("*********************************************************")


def get_headers_on_page(data):
    """
    Checks page headers at it's beginning
    :param data:
    :return:
    """
    headers = []
    for line_number, line in enumerate(data.split("\n")):
        if line.startswith("HTTP"):
            continue
        if line == "\r":
            break
        headers.append(line)
    print("Headers on page:")
    for i in headers:
        print(i)
    print("*********************************************************")


def save_page(data):
    """
    Saves received page to a file
    :param data:
    :return:
    """
    data = data.encode('utf-8')
    with open('saved_page.html', 'wb') as f:
        f.write(data)


class MyHTMLParser(HTMLParser):

    # Initializing lists
    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()
    tags = []
    tags_final = []

    # HTML Parser Methods
    def handle_starttag(self, starttag, attrs):
        """
        For counting starttags. Here is also used for parsing tags with text
        :param starttag:
        :param attrs:
        :return:
        """
        self.lsStartTags.append(starttag)
        if starttag != "p" and starttag != "strong" and starttag != "script":
            self.tags.append(["tag", starttag])

    def handle_endtag(self, endtag):
        """
        For counting endtags
        :param endtag:
        :return:
        """
        self.lsEndTags.append(endtag)

    def handle_startendtag(self, startendtag, attrs):
        """
        For counting startendtag
        :param startendtag:
        :param attrs:
        :return:
        """
        self.lsStartEndTags.append(startendtag)

    def handle_comment(self,data):
        """
        Not used here, just for future
        :param data:
        :return:
        """
        self.lsComments.append(data)

    def handle_data(self, data):
        """
        Writes into list any data except \\n, whitespaces, script text
        :param data:
        :return:
        """
        if data != "\n" and data != " " and not data.startswith("  ") and not data.startswith("\n") \
                and not data.startswith("<!--"):
            self.tags.append(["data", data])

    def tag_by_value(self):
        """
        Form the final list where list[i][0] is tag, and list[i][1] is text
        :return:
        """
        for i in range(len(self.tags)):
            if self.tags[i][0] == "tag" and self.tags[i + 1][0] == "data":
                self.tags_final.append([self.tags[i][1], self.tags[i + 1][1]])
        print("Tags with text on page:")
        print(self.tags_final)
        print("*********************************************************")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((hostname, 80))
s.send(str.encode(message))
resp = s.recv(1000)
output = []
while len(resp) > 0:
    output.append(resp.decode("utf-8"))
    resp = s.recv(1000)
output_text = "".join(output)
save_page(output_text)
if printpage:
    print(output_text)
    print("*********************************************************")
get_responce_code(output_text)
get_headers_on_page(output_text)
count_images_on_page(output_text)
count_links_on_page(output_text)

parser = MyHTMLParser()
parser.feed(output_text)
parser.tag_by_value()
print("Top used start tag:", max(set(parser.lsStartTags), key=parser.lsStartTags.count))
print("Top used end tag:", max(set(parser.lsEndTags), key=parser.lsEndTags.count))
print("Top used start-end tag:", max(set(parser.lsStartEndTags), key=parser.lsStartEndTags.count))
print("*********************************************************")

parser.close()
s.close()

