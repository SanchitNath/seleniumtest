from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CommonMethods:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be present in the DOM."""
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator)
        )

    def click_element(self, locator):
        """Click on an element."""
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text, clear_first=True):
        """Enter text into an input field."""
        input_text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        if clear_first:
            input_text.clear()
        input_text.send_keys(text)

    def get_element_text(self, locator):
        """Get the text of an element."""
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def is_element_present(self, locator, timeout=30):
        """Check if an element is present in the DOM."""
        try:
            self.wait_for_element(locator, timeout)
            return True
        except:
            return False
        
    def get_elements(self, locator):
        """Get a list of elements matching the locator."""
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(locator))
    
    def get_element_attribute(self, locator, attribute):
        """Get the value of an attribute of an element."""
        element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.get_attribute(attribute)
    
    def sleep(self, seconds):
        """Sleep for a specified number of seconds."""
        time.sleep(seconds)
