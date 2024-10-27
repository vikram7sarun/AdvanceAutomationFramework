# pages/login_page.py
import logging

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):

    logger = logging.getLogger("TestLogger")


    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    USERNAME_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit'")

    def login(self, username, password):
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
