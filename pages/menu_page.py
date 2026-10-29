from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MenuPage(BasePage):
    """The burger side menu that is available on every authenticated page."""

    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
    ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")

    def open(self):
        self.click(self.MENU_BUTTON)
        self.find(self.LOGOUT_LINK)
        return self

    def logout(self):
        self.open()
        self.click(self.LOGOUT_LINK)

    def reset_app_state(self):
        self.open()
        self.click(self.RESET_APP_STATE_LINK)
