"""
These tests check the functions of adding a download file
by admin
"""
import pytest

@pytest.mark.usefixtures("open_downloads")
@pytest.mark.usefixtures("login")
@pytest.mark.usefixtures("open_login_page")
class TestDownloadsPage:
    """

    """
    def test_add_file(self,
                      downloads_page, new_file_name, new_file_mask, new_file,
                      downloads_success):
        """
        tests adding a new file for download
        :param downloads_page:
        :param new_file_name:
        :param new_file_mask:
        :param new_file:
        :param downloads_success:
        :return:
        """
        downloads_page.open_downloads()
        downloads_page.add_file(new_file_name, new_file_mask, new_file)
        assert downloads_success in downloads_page.success_alert()