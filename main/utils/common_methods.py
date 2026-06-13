from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from main.utils.logger import LogGen


class CommonMethods:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.driver.implicitly_wait(10)  # Set a default implicit wait
        self.logger = LogGen.loggen()

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

    def check_link_status(self, url):
        """Check the status of a link."""
        try:
            get_response = requests.get(url)
            response = requests.head(url, allow_redirects=True)
            return response.status_code
        except requests.RequestException as e:
            self.logger.error(f"Error checking link: {e}")
            return None

    def check_req_bad_request(self, url):
        """Check if a link returns a bad request."""
        try:
            response = requests.get(url)
            return response.status_code == 400
        except requests.RequestException as e:
            self.logger.error(f"Error checking bad request: {e}")
            return False

    def check_req_unauthorized(self, url):
        """Check if a link returns an unauthorized status."""
        try:
            response = requests.get(url)
            return response.status_code == 401
        except requests.RequestException as e:
            self.logger.error(f"Error checking unauthorized request: {e}")
            return False

    def check_req_payment_required(self, url):
        """Check if a link returns a payment required status."""
        try:
            response = requests.get(url)
            return response.status_code == 402
        except requests.RequestException as e:
            self.logger.error(f"Error checking payment required request: {e}")
            return False

    def check_req_forbidden(self, url):
        """Check if a link returns a forbidden status."""
        try:
            response = requests.get(url)
            return response.status_code == 403
        except requests.RequestException as e:
            self.logger.error(f"Error checking forbidden request: {e}")
            return False

    def check_req_not_found(self, url):
        """Check if a link returns a not found status."""
        try:
            response = requests.get(url)
            return response.status_code == 404
        except requests.RequestException as e:
            self.logger.error(f"Error checking not found request: {e}")
            return False

    def check_req_method_not_allowed(self, url):
        """Check if a link returns a method not allowed status."""
        try:
            response = requests.get(url)
            return response.status_code == 405
        except requests.RequestException as e:
            self.logger.error(f"Error checking method not allowed request: {e}")
            return False

    def check_req_not_acceptable(self, url):
        """Check if a link returns a not acceptable status."""
        try:
            response = requests.get(url)
            return response.status_code == 406
        except requests.RequestException as e:
            self.logger.error(f"Error checking not acceptable request: {e}")
            return False

    def check_req_proxy_authentication_required(self, url):
        """Check if a link returns a proxy authentication required status."""
        try:
            response = requests.get(url)
            return response.status_code == 407
        except requests.RequestException as e:
            self.logger.error(f"Error checking proxy authentication required request: {e}")
            return False

    def check_request_timeout(self, url):
        """Check if a link returns a request timeout status."""
        try:
            response = requests.get(url)
            return response.status_code == 408
        except requests.RequestException as e:
            self.logger.error(f"Error checking request timeout: {e}")
            return False

    def check_req_conflict(self, url):
        """Check if a link returns a conflict status."""
        try:
            response = requests.get(url)
            return response.status_code == 409
        except requests.RequestException as e:
            self.logger.error(f"Error checking conflict request: {e}")
            return False

    def check_req_gone(self, url):
        """Check if a link returns a gone status."""
        try:
            response = requests.get(url)
            return response.status_code == 410
        except requests.RequestException as e:
            self.logger.error(f"Error checking gone request: {e}")
            return False