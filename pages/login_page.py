from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_DISMISS_BUTTON = (By.CSS_SELECTOR, "[data-test='error-button']")

    def load(self, url):
        self.open_url(url)
        return self

    def is_loaded(self):
        return self.is_visible(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def dismiss_error(self):
        self.click(self.ERROR_DISMISS_BUTTON)
        self.wait_until_invisible(self.ERROR_MESSAGE)
