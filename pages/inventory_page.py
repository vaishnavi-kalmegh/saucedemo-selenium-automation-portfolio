from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, class_token, parse_money, xpath_literal


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BACKPACK = (By.ID, "add-to-cart-sauce-labs-backpack")
    ADD_TO_CART_BIKE_LIGHT = (By.ID, "add-to-cart-sauce-labs-bike-light")
    ADD_TO_CART_BOLT_SHIRT = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    REMOVE_BACKPACK = (By.ID, "remove-sauce-labs-backpack")
    REMOVE_BIKE_LIGHT = (By.ID, "remove-sauce-labs-bike-light")

    # --- product-specific locators (built from the visible product name) ---

    @staticmethod
    def _item_xpath(product_name):
        return (
            f"//div[{class_token('inventory_item')}]"
            f"[.//div[{class_token('inventory_item_name')} "
            f"and normalize-space(.)={xpath_literal(product_name)}]]"
        )

    def _item_button(self, product_name):
        return (By.XPATH, self._item_xpath(product_name) + "//button")

    def _item_link(self, product_name):
        return (
            By.XPATH,
            f"//a[.//div[{class_token('inventory_item_name')} "
            f"and normalize-space(.)={xpath_literal(product_name)}]]",
        )

    # --- page state ---

    def is_loaded(self):
        return self.is_inventory_displayed()

    def is_inventory_displayed(self):
        return self.is_visible(self.TITLE) and self.get_text(self.TITLE) == "Products"

    # --- adding / removing products ---

    def add_to_cart(self, product_name):
        button = self._item_button(product_name)
        self.click(button)
        self.wait.until(EC.text_to_be_present_in_element(button, "Remove"))

    def remove_from_cart(self, product_name):
        button = self._item_button(product_name)
        self.click(button)
        self.wait.until(EC.text_to_be_present_in_element(button, "Add to cart"))

    def add_backpack_to_cart(self):
        self.click(self.ADD_TO_CART_BACKPACK)
        self.wait.until(lambda driver: driver.find_elements(*self.REMOVE_BACKPACK))

    def add_bike_light_to_cart(self):
        self.click(self.ADD_TO_CART_BIKE_LIGHT)
        self.wait.until(lambda driver: driver.find_elements(*self.REMOVE_BIKE_LIGHT))

    def add_bolt_shirt_to_cart(self):
        self.click(self.ADD_TO_CART_BOLT_SHIRT)

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK)
        self.wait_until_invisible(self.REMOVE_BACKPACK)

    # --- cart badge ---

    def get_cart_count(self):
        return self.get_text(self.SHOPPING_CART_BADGE)

    def cart_badge_is_visible(self):
        return bool(self.driver.find_elements(*self.SHOPPING_CART_BADGE))

    def wait_for_cart_to_be_empty(self):
        return self.wait_until_invisible(self.SHOPPING_CART_BADGE)

    def go_to_cart(self):
        self.click(self.SHOPPING_CART_LINK)
        self.wait_for_url("cart.html")

    # --- product details ---

    def open_product(self, product_name):
        self.click(self._item_link(product_name))
        self.wait_for_url("inventory-item.html")

    # --- sorting and listing ---

    def sort_by(self, option):
        select = Select(self.find(self.SORT_DROPDOWN))
        select.select_by_value(option)
        self.wait.until(
            lambda driver: Select(
                driver.find_element(*self.SORT_DROPDOWN)
            ).first_selected_option.get_attribute("value")
            == option
        )

    def get_product_count(self):
        return len(self.driver.find_elements(*self.INVENTORY_ITEM))

    def get_product_names(self):
        return [element.text.strip() for element in self.driver.find_elements(*self.PRODUCT_NAMES)]

    def get_product_prices(self):
        return [
            parse_money(element.text)
            for element in self.driver.find_elements(*self.PRODUCT_PRICES)
        ]
