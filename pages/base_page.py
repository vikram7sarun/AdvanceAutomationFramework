# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)

    # Basic actions
    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, locator, timeout=Config.IMPLICIT_WAIT):
        """Wait for element visibility and return element if located."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element with locator {locator} not found.")
            return None

    def click(self, locator):
        """Click an element specified by locator."""
        element = self.find_element(locator)
        if element:
            element.click()
        else:
            print(f"Could not click element with locator {locator} as it was not found.")

    def send_keys(self, locator, text):
        """Send text to an element specified by locator."""
        element = self.find_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
        else:
            print(f"Could not send keys to element with locator {locator} as it was not found.")

    def get_text(self, locator):
        """Get text of an element specified by locator."""
        element = self.find_element(locator)
        return element.text if element else None

    def is_element_displayed(self, locator):
        """Check if element is displayed."""
        try:
            return self.find_element(locator).is_displayed()
        except NoSuchElementException:
            return False

    # Waits
    def wait_for_element_clickable(self, locator, timeout=Config.IMPLICIT_WAIT):
        """Wait for element to be clickable."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            print(f"Element with locator {locator} not clickable.")
            return None

    def wait_for_element_invisible(self, locator, timeout=Config.IMPLICIT_WAIT):
        """Wait for element to become invisible."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            print(f"Element with locator {locator} did not become invisible.")
            return False

    # Dropdowns
    def select_dropdown_by_value(self, locator, value):
        """Select dropdown option by value."""
        element = self.find_element(locator)
        if element:
            Select(element).select_by_value(value)

    def select_dropdown_by_visible_text(self, locator, text):
        """Select dropdown option by visible text."""
        element = self.find_element(locator)
        if element:
            Select(element).select_by_visible_text(text)

    def select_dropdown_by_index(self, locator, index):
        """Select dropdown option by index."""
        element = self.find_element(locator)
        if element:
            Select(element).select_by_index(index)

    # Alerts
    def accept_alert(self):
        """Accept browser alert."""
        try:
            WebDriverWait(self.driver, Config.IMPLICIT_WAIT).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("No alert to accept.")

    def dismiss_alert(self):
        """Dismiss browser alert."""
        try:
            WebDriverWait(self.driver, Config.IMPLICIT_WAIT).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except TimeoutException:
            print("No alert to dismiss.")

    def get_alert_text(self):
        """Get text from alert."""
        try:
            WebDriverWait(self.driver, Config.IMPLICIT_WAIT).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            print("No alert present.")
            return None

    # JavaScript executors
    def scroll_to_element(self, locator):
        """Scroll to element specified by locator."""
        element = self.find_element(locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_bottom(self):
        """Scroll to bottom of the page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Screenshots
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot and save it with the specified name."""
        self.driver.save_screenshot(f"{name}.png")
