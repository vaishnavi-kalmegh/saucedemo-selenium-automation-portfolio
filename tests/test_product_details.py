import pytest

from data.catalog import BACKPACK, PRODUCTS
from pages.inventory_page import InventoryPage
from pages.product_detail_page import ProductDetailPage


@pytest.mark.inventory
@pytest.mark.parametrize("product_name, price", list(PRODUCTS.items()), ids=list(PRODUCTS))
def test_product_detail_page_shows_name_and_price(logged_in, product_name, price):
    logged_in.open_product(product_name)

    detail = ProductDetailPage(logged_in.driver).wait_until_loaded()
    assert detail.get_name() == product_name
    assert detail.get_price() == price
    assert detail.get_description()


@pytest.mark.inventory
def test_add_to_cart_from_product_detail_page(logged_in):
    logged_in.open_product(BACKPACK)
    detail = ProductDetailPage(logged_in.driver).wait_until_loaded()

    detail.add_to_cart()
    assert logged_in.get_cart_count() == "1"


@pytest.mark.inventory
def test_back_to_products_returns_to_inventory(logged_in):
    logged_in.open_product(BACKPACK)
    ProductDetailPage(logged_in.driver).wait_until_loaded().back_to_products()
    assert InventoryPage(logged_in.driver).is_inventory_displayed()
