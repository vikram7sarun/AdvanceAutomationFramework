from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class WebDriverFactory():

    def __init__(self, browser='chrome', remote="False"):
        # self.driver = None
        self.browser = browser.lower()
        self.remote = remote
        self.selenium_grid_url = "http://localhost:4444/wd/hub"
        self.getWebDriverInstance()

    def getWebDriverInstance(self):
        if self.browser == "chromeRemote":
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(command_executor=self.selenium_grid_url, options=options)
        elif self.browser == "firefoxRemote":
            options = webdriver.FirefoxOptions()
            driver = webdriver.Remote(command_executor=self.selenium_grid_url, options=options)
        elif self.browser == "edgeRemote":
            options = webdriver.EdgeOptions()
            driver = webdriver.Remote(command_executor=self.selenium_grid_url, options=options)
        elif self.browser == "chrome":
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif self.browser == "firefox":
            pass
            # service = FirefoxService(GeckoDriverManager().install())
            # driver = webdriver.Firefox(service=service)
        elif self.browser == "edge":
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service)
        else:
            raise ValueError(f"Browser '{self.browser}' is not supported.")

        driver.maximize_window()

    def quit(self):
        if self.driver:
            self.driver.quit()

