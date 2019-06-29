"""
This is a small ftp client to test base ftp functions
"""
from os import chdir, path, makedirs, getcwd
from ftplib import error_reply, error_perm


def test_upload_file(ftp_connect, work_path, upload_file):
        try:
            ftp_connect.cwd(work_path)
        except error_reply as e:
            print("Could not change current direction to {}: ".format(work_path), e)
        print("Changed current dir to {}".format(work_path))
        filename = upload_file.split("\\")[-1]

        def upload(path):
            try:
                fh = open(path, 'rb')
                ftp_connect.storbinary("STOR {}".format(filename), fh)
                fh.close()
                print("Uploaded file {} to dir {}".format(filename, ftp_connect.pwd()))
            except error_reply as e:
                print("Could not upload file {} to directory {}".format(upload_file, work_path))

        path_to_file = "".join([getcwd(), upload_file])
        if path.isfile(path_to_file):
            print("The path to the file for upload is relative, uploading...")
            upload(path_to_file)
        elif path.isfile(upload_file):
            print("The path to the file for upload is absolute, uploading...")
            upload(upload_file)
        assert filename in ftp_connect.nlst()


def test_delete_uploaded_file(ftp_connect, upload_file, work_path):
    filename = upload_file.split("\\")[-1]
    try:
        ftp_connect.delete("".join([work_path, "/", filename]))
        print("Deleted file {} from dir {}".format(filename, work_path))
    except error_reply as e:
        print("Could not delete file {} in directory {}: ".format(work_path, filename), e)
    assert upload_file not in ftp_connect.nlst()


def test_file_download(ftp_connect, download_file, work_path, downloads_dir):
    try:
        ftp_connect.cwd(work_path)
    except error_reply as e:
        print("Could not change current direction to {}: ".format(work_path), e)
    try:
        chdir(downloads_dir)
    except Exception as e:
        if "The system cannot find the file specified: " in str(e):
            if not path.isdir(downloads_dir):
                print("No {} directory found, creating it...".format(downloads_dir))
                makedirs(downloads_dir)
                print("{} directory created.".format(downloads_dir))
    if path.isdir(downloads_dir):
        chdir(downloads_dir)
    if path.isfile("".join([downloads_dir, "\\", download_file])):
        print("File {} in directory {} already existed".format(download_file, downloads_dir))
    try:
        fhandle = open(download_file, 'wb')
        ftp_connect.retrbinary('RETR ' + download_file, fhandle.write)
        fhandle.close()
    except error_reply as e:
        print("Could not download file {} to {}: ".format(download_file, downloads_dir), e)
    print("Download file {} from dir {}".format(download_file, work_path))
    assert path.isfile("".join([downloads_dir, "\\", download_file]))


def test_create_dir(ftp_connect, new_dir, work_path):
    try:
        ftp_connect.cwd(work_path)
    except error_reply as e:
        print("Could not change current direction to {}: ".format(work_path), e)
    try:
        ftp_connect.mkd(new_dir)
        print("Created dir {}".format("".join([work_path, "/", new_dir])))
    except error_perm as e:
        print("There are problems with rights while creating {} in {}".format(new_dir, work_path))
    assert new_dir in ftp_connect.nlst()

def test_remove_dir(ftp_connect, new_dir, work_path):
    try:
        ftp_connect.cwd(work_path)
    except error_reply as e:
        print("Could not change current direction to {}: ".format(work_path), e)
    try:
        ftp_connect.rmd(new_dir)
        print("Removed dir {}".format("".join([work_path, "/", new_dir])))
    except error_reply as e:
        print("There are problems while deleting {} in {}".format(new_dir, work_path))
    assert new_dir not in ftp_connect.nlst()
