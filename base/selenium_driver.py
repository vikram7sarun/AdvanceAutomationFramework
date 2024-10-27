import logging
import time
from traceback import print_stack
from kombu.asynchronous.timer import Entry
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
# import utilities.custom_logger as cl
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key, Controller


class Selenium_Driver():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "C:\\TEMP\\screenshots\\"
        """relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        #destinationFile = os.path.join(currentDirectory, relativeFileName)"""
        destinationFile = screenshotDirectory + fileName
        try:
            """if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)"""
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot save to directory: " + destinationFile)
        except Exception as e:
            self.log.error("Exception occurred in ScreenShot method ")
            print("Exception is :" + str(e))

    def getCurrentUrl(self):
        return self.driver.current_url

    def getTitle(self):

        return self.driver.title

    def getByType(self, locatorType):
        self.implicitWait(15)
        try:
            locatorType = locatorType.lower()
            locatorType = locatorType.lower()
            if locatorType == "id":
                return By.ID
            elif locatorType == "name":
                return By.NAME
            elif locatorType == "xpath":
                return By.XPATH
            elif locatorType == "css":
                return By.CSS_SELECTOR
            elif locatorType == "classname":
                return By.CLASS_NAME
            elif locatorType == "linktext":
                return By.LINK_TEXT
            else:
                self.log.error("Locator type " + locatorType + " not correct/supported")
            return False
        except Exception as e:
            self.log.error("Exception occurred in getByType method ")
            print("Exception in getByType method is :" + str(e))

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)

            self.log.info("Element Found with locator " + locator + " and locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Element not found with locator " + locator + " and locatorType: " + locatorType)
            print("Exception in getElement method is :" + str(e))
        return element

    def getListOfElements(self, locator, locatorType="id"):
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info("Elements Found with locator " + locator + " and locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Elements not found with locator " + locator + " and locatorType: " + locatorType)
            print("Exception in getListOfElements method is :" + str(e))
        print(len(elements))
        return elements

    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in elementClick method is:" + str(e))

    def elementClickUntilItClicks(self, locator, locatorTOWait):
        try:
            wait = WebDriverWait(self.driver, 20)
            for i in range(4):
                try:
                    self.elementClick(locator)
                    print("Button clicked")
                    wait.until(EC.presence_of_element_located((By.XPATH, locatorTOWait)))
                    return True
                except TimeoutException:
                    print("Page did not open, hence trying again")
                    i = i + 1
                    continue
            return False
        except Exception as e:
            self.log.error("Cannot click on the element with locator: " + locator)
            print("Exception in elementClickUntilItClicks method is:" + str(e))

    def elementsClick(self, locator, locatorType="xpath"):
        elements = self.getListOfElements(locator, locatorType)
        elements.click()

    def clickFirstDisplayedElement(self, locator, locatorType="id"):
        try:
            elementsList = self.getListOfElements(locator, locatorType)
            if len(elementsList) > 0:
                for element in elementsList:
                    if element.is_displayed():
                        element.click()
                        self.log.info("Clicked on element with locator: " + locator + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Element not found with locator " + locator + " and locatorType: " + locatorType)
            print("Exception in getElement method is :" + str(e))

    def getTextOfElement(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            text1 = element.text
            self.log.info("Got the text on element with locator: " + locator + " locatorType: " + locatorType)
            return text1
        except Exception as e:
            self.log.error("Cannot found the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in getTextOfElement is :" + str(e))
            return ""  # Return an empty string when element is not found or an exception occurs

    def dropDown(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            sel.select_by_visible_text(data)
            self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
        except Exception as e:
            self.log.error("Cannot find element in dropdown with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in dropDown is :" + str(e))

    def dropDownwithoptionvalue(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            sel.select_by_value(data)
            self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
        except Exception as e:
            self.log.error("Cannot find element in dropdown with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in dropDownwithoptionvalue method is :" + str(e))

    def dropDownwithindex(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            sel.select_by_index(data)
            self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
        except Exception as e:
            self.log.error("Cannot find element in dropdown with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in dropDown is :" + str(e))

    def get_text_of_selected_elemet(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            sel = Select(element)
            return sel.first_selected_option.text
            # self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
        except Exception as e:
            self.log.error("Cannot find element in dropdown with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in get_text_of_selected_elemet method is :" + str(e))

    # def pressEnterKey(self, locator, locatorType="id"):
    #     try:
    #         element = self.getElement(locator, locatorType)
    #         element.send_keys(Keys.ENTER)
    #         self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
    #     except Exception as e:
    #         self.log.error("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
    #         print("Exception in pressEnterKey method is :" + str(e))
    def pressEnterKey(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                element.send_keys(Keys.ENTER)
                self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + "Selected")
            else:
                self.log.error("Cannot find the element with locator: " + locator + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Exception in pressEnterKey method: " + str(e))
            print("Exception in pressEnterKey method is :" + str(e))

    def isElementDisplayed(self, locator, locatorType):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                isDisplayed = element.is_displayed()
                return isDisplayed
            else:
                self.log.info("Element not found")
                return False
        except Exception as e:
            self.log.error("Element not found")
            print("Exception in isElementDisplayed method is :" + str(e))
            return False

    def openNewTab(self, newUrl):

        try:
            # open new window with execute_script()
            self.driver.execute_script("window.open('');")
            # switch to new window with switch_to.window()
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(newUrl)
        except Exception as e:
            self.log.error("could not open a new tab to got to url: " + newUrl)
            print("Exception in openNewTab method is :" + str(e))

    def pressPageRefresh(self):
        try:
            self.driver.refresh()
        except Exception as e:
            self.log.error("could not refresh")
            print("Exception in pressPageRefresh method is :" + str(e))

    def scrollDown(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(2)
        except Exception as e:
            self.log.error("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in scrollDown method is :" + str(e))

    def scrollUp(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(2)
        except Exception as e:
            self.log.error("Cannot click on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in scrollUp method is :" + str(e))

    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            # self.clearField(locator, locatorType)
            element.clear()
            element.send_keys(data)
            self.log.info("Data sent successfully.")
            self.log.info("Send data on element with locator: " + data + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in sendKeys method is :" + str(e))

    def sendKeysFirstDisplayedElement(self, data, locator, locatorType="id"):
        try:
            elementsList = self.getListOfElements(locator, locatorType)
            for element in elementsList:
                if element.is_displayed():
                    self.clearField(locator, locatorType)
                    element.send_keys(data)
            self.log.info("Send data on element with locator: " + locator + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in sendKeys method is :" + str(e))

    def navigateBack(self):
        try:
            self.driver.execute_script("window.history.go(-1)")
            self.log.info("Succesfully moved to prevous window")
        except Exception as e:
            self.log.error("Cannot move to prevous window")
            print("Exception in navigateBack method is :" + str(e))

    def navigateTo(self, url):
        try:
            self.driver.get(url)
            time.sleep(3)
            self.log.info("Succesfully navigated to: " + url)
        except Exception as e:
            self.log.error("Cannot navigate to: " + url)
            print("Exception in navigateTo method is :" + str(e))

    def clearField(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            self.log.info("Send data on element with locator: " + locator + " locatorType: " + locatorType)
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in clearField method is :" + str(e))

    def getText(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            text = element.text
            self.log.info("Get text on element with locator: " + locator + " locatorType: " + locatorType)
            return text
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in getText method is :" + str(e))
            return ""  # Return an empty string when element is not found or an exception occurs

    def getValue(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            text = element.get_attribute('value')
            self.log.info("Get text on element with locator: " + locator + " locatorType: " + locatorType)
            return text
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in getText method is :" + str(e))

    def isElementPresent(self, locator, locatorType='id'):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except Exception as e:
            self.log.error("Element not found")
            print("Exception in isElementPresent method is :" + str(e))
            return False

    def elementPresenceCheck(self, locator, byType='id'):
        print("In elementPresenceCheck")
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.error("Element not found")
                return False
        except Exception as e:
            self.log.info("Element not found")
            print("Exception in elementPresenceCheck method is :" + str(e))
            return False

    def waitForElement(self, locator, locatorType="id", timeout=300, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.element_to_be_clickable((byType,
                                                             locator)))
            self.log.info("Element appeared on the web page")
        except Exception as e:
            self.log.info("Element not appeared on the web page")
            print("Exception in waitForElement method is :" + str(e))
        return element

    def waitForElementToBeUnvisible(self, locator, locatorType="id", timeout=300):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            wait.until(EC.invisibility_of_element_located((byType, locator)))
            self.log.info("Element disappeared on the web page")
        except Exception as e:
            self.log.info("Element still appears on the web page")
            print("Exception in waitForElement method is :" + str(e))

    def waitForElementToBeVisible(self, locator, locatorType="id", timeout=300):
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                          " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            wait.until(EC.visibility_of_element_located((byType, locator)))
            self.log.info("Element visible on the web page")
        except Exception as e:
            self.log.info("Element still not appeared on the web page")
            print("Exception in waitForElement method is :" + str(e))

    def waitForStalenessOfElement(self, locator, locatorType="id"):
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.staleness_of((byType, locator)))
        except StaleElementReferenceException as e:
            print("Stale Element Exception")

    def implicitWait(self, timeout=20):
        self.driver.implicitly_wait(timeout)

    def waitUntilTitlePresence(self, title, timeout=15):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.title_contains(title))

    def handle_alert(self, action="accept"):
        wait = WebDriverWait(self.driver, timeout=5)
        alert = wait.until(lambda d: d.switch_to.alert)
        if action == "accept":
            alert.accept()
        else:
            alert.dismiss()

    def switchToWindow(self, i):
        try:
            handles = self.driver.window_handles
            num = len(handles)
            print("number of handles: " + str(num))
            # If second window is opened then put i = 1
            self.driver.switch_to.window(handles[i])
            self.log.info("Switched to new window")
        except Exception as e:
            self.log.error("Cannot switch to new window as new window is not found")
            print("Exception in switchToWindow method is :" + str(e))

    def switchToFrame(self, frame_name):
        self.driver.switch_to.frame(frame_name)

    def switchToFrameUsingIndex(self, index):
        self.driver.switch_to.frame(index)

    def switchToFrameUsingWebelement(self, locator, locatorType):
        element = self.getElement(locator, locatorType)
        self.driver.switch_to.frame(element)

    def switchToDefaultFrame(self):
        self.driver.switch_to.default_content()

    def moveSlider(self, offset, locator, locatorType="id"):
        byType = self.getByType(locatorType)
        slider = self.driver.find_element(byType, locator)
        move = ActionChains(self.driver)
        move.drag_and_drop_by_offset(slider, offset, 0).perform()

    def moveToElement(self, locator, locatorType="id", click=False):
        element = self.getElement(locator, locatorType)
        actions = ActionChains(self.driver)
        if click:
            actions.move_to_element(element).click().perform()
        else:
            actions.move_to_element(element).perform()

    def actions_click(self, locator, locatorType="id"):
        element = self.getElement(locator, locatorType)
        actions = ActionChains(self.driver)
        actions.click(on_element=element).perform()

    def actions_move_to_element(self, locator, locatorType="id"):
        element = self.getElement(locator, locatorType)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()

    def actions_send_keys(self, text):
        actions = ActionChains(self.driver)
        actions.send_keys(text).perform()

    def action_send_keys_to_element(self, text, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                actions = ActionChains(self.driver)
                self.clearField(locator, locatorType)
                actions.send_keys_to_element(element, text).perform()
            else:
                print("Element not found.")
        except Exception as e:
            print("An error occurred: {str(e)}")

    def element_click_scrolled_into_view(self, locator, locatorType="id"):
        element = self.getElement(locator, locatorType)
        self.driver.execute_script("arguments[0].click();", element)

    def element_scroll_into_view(self, locator, locatorType="id"):
        element = self.getElement(locator, locatorType)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def js_sendkey(self, value, locator, locatorType="id"):
        element = self.getElement(locator, locatorType)
        self.driver.execute_script("arguments[0].value='" + value + "';", element)

    def getAttributeValue(self, attribute, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            value = element.get_attribute(attribute)
            self.log.info("Get attribute value on element with locator: " + locator + " locatorType: " + locatorType)
            return value
        except Exception as e:
            self.log.error("Cannot send data on the element with locator: " + locator + " locatorType: " + locatorType)
            print("Exception in getAttributeValue method is :" + str(e))

    def closeCurrentTab(self):
        self.driver.close()

    def element_info(self, element):
        print("---------------------Element info-------------------------")
        print("is diplayed: " + str(element.is_displayed()))
        print("is enabled: " + str(element.is_enabled()))
        print("location: " + str(element.location))
        print("attribute href: " + str(element.get_attribute('href')))
        print("attribute id: " + str(element.get_attribute('id')))
        print("attribute title: " + str(element.get_attribute('title')))
        print("attribute alt: " + str(element.get_attribute('alt')))
        print("Parent: " + str(element.parent))
        print("Size: " + str(element.size))
        print("tag_name: " + str(element.tag_name))

    def isElementClickable(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                is_clickable = element.is_enabled() and element.is_displayed()
                if is_clickable:
                    self.log.info("Element with locator: " + locator + " locatorType: " + locatorType + " is clickable")
                else:
                    self.log.error(
                        "Element with locator: " + locator + " locatorType: " + locatorType + " is not clickable")
                return is_clickable
            else:
                self.log.error("Cannot find the element with locator: " + locator + " locatorType: " + locatorType)
                return False
        except Exception as e:
            self.log.error("Exception in isElementClickable method: " + str(e))
            print("Exception in isElementClickable method is:" + str(e))
            return False

    # def fileUpload(self,path):
    #     autoit.win_wait_active("Open")
    #     time.sleep(2)
    #     autoit.control_set_text("Open", "Edit1", path)
    #     autoit.send("{ENTER}")
