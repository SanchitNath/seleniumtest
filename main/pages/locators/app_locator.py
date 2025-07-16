from selenium.webdriver.common.by import By

class AppLocators:
    app_logo = (By.XPATH, "//img[@alt='App Logo']")
    app_title = (By.XPATH, "//h1[@class='app-title']")
    search_input = (By.XPATH, "//input[@id='search']")
    notifications_icon = (By.XPATH, "//div[@class='notifications-icon']")
    user_profile_icon = (By.XPATH, "//div[@class='user-profile-icon']")
    footer_text = (By.XPATH, "//footer//p[@class='footer-text']")
    sidebar_menu = (By.XPATH, "//nav[@class='sidebar-menu']")
    sidebar_menu_items = (By.XPATH, "//nav[@class='sidebar-menu']//li")
    