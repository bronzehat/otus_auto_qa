"""
This is a small ftp client to test base ftp functions
"""
from ftplib import FTP, error_reply
from os import chdir, getcwd


ftp_hostname = '192.168.85.154'
ftp_user = 'asayapova'
ftp_password='o9p0[-]='
upload_filename = "test_ssh_opencart_terminal_screen.png"
download_filename = "testfile"
downloads_dir = "".join([getcwd(),"\downloads\\"])
dirname = "test_dir"
server_path = "/home/asayapova/PycharmProjects"
ftp = FTP(ftp_hostname)

class Test_FTP():

    def login(self, username, passwd):
        try:
            ftp.login(user=username, passwd=passwd)
            print("Logged in {} by username {}".format(ftp_hostname, ftp_user))
        except error_reply as e:
            print(e)
            ftp.quit()

    def goto_dir(self, dir):
        ftp.cwd(dir)
        print("Changed dir to {}".format(dir))

    def file_upload(self, filename, dir=server_path):
        ftp.cwd(dir)
        ftp.storbinary("STOR {}".format(filename), open(filename, 'rb'))
        print("Uploaded file {} to dir {}".format(filename, ftp.pwd()))

    def file_delete(self, filename, ftp_dir=server_path):
        ftp.delete("".join([ftp_dir, "/", filename]))
        print("Deleted file {} from dir {}".format(filename, ftp_dir))

    def file_download(self, download_filename, ftp_dir=server_path, localdir=downloads_dir):
        ftp.cwd(ftp_dir)
        chdir(localdir)
        fhandle = open(download_filename, 'wb')
        ftp.retrbinary('RETR ' + download_filename, fhandle.write)
        fhandle.close()
        print("Download file {} from dir {}".format(download_filename, ftp_dir))

    def create_dir(self, dir, path=server_path):
        ftp.cwd(path)
        ftp.mkd(dir)
        print("Created dir {}".format("".join([path, "/", dir])))

    def remove_dir(self, dir, path=server_path):
        ftp.cwd(path)
        ftp.rmd(dir)
        print("Removed dir {}".format("".join([path, "/", dir])))

test_ftp = Test_FTP()
test_ftp.login(ftp_user, ftp_password)
# test_ftp.goto_dir(server_path)
# test_ftp.file_upload(upload_filename)
# test_ftp.file_delete(upload_filename)
# test_ftp.file_download(download_filename)
# test_ftp.create_dir(dirname)
# test_ftp.remove_dir(dirname)
ftp.quit()