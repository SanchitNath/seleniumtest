from selenium import webdriver
from utils.common_methods import CommonMethods as cm
from locators.app_locator import AppLocators as al

def setup(driver):
    assert cm.is_element_present(al.app_logo), "App logo is not present on the page"
    cm.click_element(al.app_title)

class AppPage:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def create_app_page(self):
        """Create the app page with all elements."""
        title_present = cm.is_element_present(al.app_title)
        if title_present:
            cm.sleep(1)
            assert cm.is_element_present(al.notifications_icon)
            menu = cm.get_element_text(al.sidebar_menu)
            items_in_menu = cm.get_elements(al.sidebar_menu_items)
            if menu and items_in_menu:
                print(f"Number of items in menu: {len(items_in_menu)}")
            assert cm.is_element_present(al.user_profile_icon)
            cm.enter_text(al.search_input, "Search for something")
            footer_text = cm.get_element_text(al.footer_text)
            print(f"Footer Text: {footer_text}")

