# tests/test_login.py
import logging
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import Config
import yaml


def load_yaml_data(file_name):
    with open(f"data/{file_name}.yaml", "r") as file:
        return yaml.safe_load(file)


logger = logging.getLogger("TestLogger")



@pytest.mark.usefixtures("setup")
@pytest.mark.smoke
def test_valid_login(self):
    logger.info("Executing test_valid_login")
    login_page = LoginPage(self.driver)
    login_page.open_url(Config.BASE_URL)
    login_page.login("valid_user", "valid_password")
    # assert login_page.is_dashboard_displayed(), "Login failed: Dashboard not displayed."



@pytest.mark.usefixtures("setup")
@pytest.mark.regression
def test_invalid_login(self):
    logger.info("Executing test_invalid_login")
    login_page = LoginPage(self.driver)

    login_page.open_url(Config.BASE_URL)
    login_page.login("invalid_user", "invalid_password")

    assert not login_page.is_dashboard_displayed(), "Login should have failed but dashboard is displayed."



# @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
# def test_valid_login(browser, request):
#     request.getfixturevalue("setup")