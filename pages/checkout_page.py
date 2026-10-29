from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, parse_money


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    FINISH_BUTTON = (By.ID, "finish")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    CHECKOUT_OVERVIEW_TITLE = (By.CLASS_NAME, "title")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    OVERVIEW_ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item .inventory_item_name")
    OVERVIEW_ITEM_PRICES = (By.CSS_SELECTOR, ".cart_item .inventory_item_price")
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    # --- step one: your information ---

    def fill_shipping_information(self, first_name: str, last_name: str, postal_code: str):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def cancel_checkout(self):
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url("cart.html")

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    # --- step two: overview ---

    def is_overview_displayed(self) -> bool:
        try:
            return bool(
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        self.CHECKOUT_OVERVIEW_TITLE, "Checkout: Overview"
                    )
                )
            )
        except TimeoutException:
            return False

    def get_overview_item_names(self):
        self.wait_for_url("checkout-step-two.html")
        return [e.text.strip() for e in self.driver.find_elements(*self.OVERVIEW_ITEM_NAMES)]

    def get_overview_item_prices(self):
        self.wait_for_url("checkout-step-two.html")
        return [parse_money(e.text) for e in self.driver.find_elements(*self.OVERVIEW_ITEM_PRICES)]

    def get_summary_subtotal(self) -> float:
        return parse_money(self.get_text(self.SUMMARY_SUBTOTAL))

    def get_summary_tax(self) -> float:
        return parse_money(self.get_text(self.SUMMARY_TAX))

    def get_summary_total(self) -> float:
        return parse_money(self.get_text(self.SUMMARY_TOTAL))

    def cancel_from_overview(self):
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url("inventory.html")

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)
        self.wait_for_url("checkout-complete.html")

    # --- order complete ---

    def get_completion_header_text(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)

    def get_completion_text(self) -> str:
        return self.get_text(self.COMPLETE_TEXT)

    def back_home(self):
        self.click(self.BACK_HOME_BUTTON)
        self.wait_for_url("inventory.html")
