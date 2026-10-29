import pytest

from data.catalog import BACKPACK, BIKE_LIGHT, PRODUCTS
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.cart
def test_add_backpack_to_cart(logged_in):
    logged_in.add_backpack_to_cart()
    assert logged_in.get_cart_count() == "1"


@pytest.mark.cart
def test_add_bike_light_to_cart(logged_in):
    logged_in.add_bike_light_to_cart()
    assert logged_in.get_cart_count() == "1"


@pytest.mark.cart
def test_add_two_items_to_cart(logged_in):
    logged_in.add_backpack_to_cart()
    logged_in.add_bike_light_to_cart()
    assert logged_in.get_cart_count() == "2"


@pytest.mark.cart
def test_remove_backpack_from_inventory_updates_cart(logged_in):
    logged_in.add_backpack_to_cart()
    assert logged_in.get_cart_count() == "1"
    logged_in.remove_backpack()
    assert not logged_in.cart_badge_is_visible()


@pytest.mark.cart
def test_remove_backpack_from_cart_empties_cart(logged_in):
    logged_in.add_backpack_to_cart()
    logged_in.go_to_cart()
    cart = CartPage(logged_in.driver)
    cart.remove_backpack()
    assert cart.is_empty()


@pytest.mark.cart
def test_continue_shopping_returns_to_inventory(logged_in):
    logged_in.add_backpack_to_cart()
    logged_in.go_to_cart()
    CartPage(logged_in.driver).continue_shopping()
    assert InventoryPage(logged_in.driver).is_inventory_displayed()


@pytest.mark.cart
def test_cart_lists_added_items_with_correct_prices(logged_in):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.go_to_cart()

    cart = CartPage(logged_in.driver)
    assert sorted(cart.get_cart_item_names()) == sorted([BACKPACK, BIKE_LIGHT])
    assert sorted(cart.get_cart_item_prices()) == sorted(
        [PRODUCTS[BACKPACK], PRODUCTS[BIKE_LIGHT]]
    )


@pytest.mark.cart
def test_removing_one_of_two_items_keeps_the_other(logged_in):
    logged_in.add_to_cart(BACKPACK)
    logged_in.add_to_cart(BIKE_LIGHT)
    logged_in.go_to_cart()

    cart = CartPage(logged_in.driver)
    cart.remove_item(BACKPACK)
    assert cart.get_cart_item_names() == [BIKE_LIGHT]


@pytest.mark.cart
def test_cart_contents_survive_continue_shopping(logged_in):
    logged_in.add_to_cart(BACKPACK)
    logged_in.go_to_cart()
    CartPage(logged_in.driver).continue_shopping()

    inventory = InventoryPage(logged_in.driver)
    assert inventory.get_cart_count() == "1"
    inventory.go_to_cart()
    assert CartPage(logged_in.driver).get_cart_item_names() == [BACKPACK]
