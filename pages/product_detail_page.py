from selenium.webdriver.common.by import By

from pages.base_page import BasePage, parse_money


class ProductDetailPage(BasePage):
    NAME = (By.CLASS_NAME, "inventory_details_name")
    PRICE = (By.CLASS_NAME, "inventory_details_price")
    DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart")
    REMOVE_BUTTON = (By.ID, "remove")
    BACK_TO_PRODUCTS_BUTTON = (By.ID, "back-to-products")

    def wait_until_loaded(self):
        self.wait_for_url("inventory-item.html")
        self.find(self.NAME)
        return self

    def get_name(self):
        return self.get_text(self.NAME)

    def get_price(self):
        return parse_money(self.get_text(self.PRICE))

    def get_description(self):
        return self.get_text(self.DESCRIPTION)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        self.find(self.REMOVE_BUTTON)

    def back_to_products(self):
        self.click(self.BACK_TO_PRODUCTS_BUTTON)
        self.wait_for_url("inventory.html")
