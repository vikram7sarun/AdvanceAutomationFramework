from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    DASHBOARD_HEADER = (By.TAG_NAME, "h1")

    def is_dashboard_displayed(self):
        return self.find_element(self.DASHBOARD_HEADER).is_displayed()