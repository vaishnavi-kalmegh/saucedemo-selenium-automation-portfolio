import pytest

from data.catalog import BACKPACK, BIKE_LIGHT, PRODUCTS, TAX_RATE
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@pytest.mark.checkout
def test_successful_checkout_completes_order(checkout_page):
    checkout_page.fill_shipping_information("Jane", "Doe", "94016")
    assert checkout_page.is_overview_displayed()
    checkout_page.finish_checkout()
    assert checkout_page.get_completion_header_text() == "Thank you for your order!"


@pytest.mark.checkout
def test_checkout_requires_first_name(checkout_page):
    checkout_page.fill_shipping_information("", "Doe", "94016")
    assert "First Name is required" in checkout_page.get_error_message()


@pytest.mark.checkout
def test_checkout_requires_last_name(checkout_page):
    checkout_page.fill_shipping_information("Jane", "", "94016")
    assert "Last Name is required" in checkout_page.get_error_message()


@pytest.mark.checkout
def test_checkout_requires_postal_code(checkout_page):
    checkout_page.fill_shipping_information("Jane", "Doe", "")
    assert "Postal Code is required" in checkout_page.get_error_message()


@pytest.mark.checkout
def test_cancel_checkout_returns_to_cart(checkout_page):
    checkout_page.cancel_checkout()
    assert CartPage(checkout_page.driver).get_cart_item_count() == 1


@pytest.mark.checkout
def test_checkout_overview_displays_total(checkout_page):
    checkout_page.fill_shipping_information("Jane", "Doe", "94016")
    assert checkout_page.is_overview_displayed()
    assert checkout_page.get_summary_total() > 0


@pytest.mark.checkout
def test_checkout_with_all_fields_empty_reports_first_missing_field(checkout_page):
    checkout_page.fill_shipping_information("", "", "")
    assert "First Name is required" in checkout_page.get_error_message()


@pytest.mark.checkout
def test_overview_lists_every_selected_item(start_checkout):
    checkout = start_checkout(BACKPACK, BIKE_LIGHT)
    checkout.fill_shipping_information("Jane", "Doe", "94016")
    assert checkout.is_overview_displayed()
    assert sorted(checkout.get_overview_item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.checkout
def test_overview_totals_add_up(start_checkout):
    checkout = start_checkout(BACKPACK, BIKE_LIGHT)
    checkout.fill_shipping_information("Jane", "Doe", "94016")
    assert checkout.is_overview_displayed()

    expected_subtotal = PRODUCTS[BACKPACK] + PRODUCTS[BIKE_LIGHT]
    subtotal = checkout.get_summary_subtotal()
    tax = checkout.get_summary_tax()
    total = checkout.get_summary_total()

    assert subtotal == pytest.approx(expected_subtotal, abs=0.005)
    assert sum(checkout.get_overview_item_prices()) == pytest.approx(subtotal, abs=0.005)
    assert tax == pytest.approx(subtotal * TAX_RATE, abs=0.01)
    assert total == pytest.approx(subtotal + tax, abs=0.01)


@pytest.mark.checkout
def test_finished_order_confirms_and_empties_cart(start_checkout):
    checkout = start_checkout(BACKPACK)
    checkout.fill_shipping_information("Jane", "Doe", "94016")
    checkout.finish_checkout()
    assert checkout.get_completion_header_text() == "Thank you for your order!"
    assert checkout.get_completion_text()

    checkout.back_home()
    inventory = InventoryPage(checkout.driver)
    assert inventory.is_inventory_displayed()
    inventory.wait_for_cart_to_be_empty()
    assert not inventory.cart_badge_is_visible()


@pytest.mark.checkout
def test_cancel_from_overview_returns_to_inventory_with_cart_intact(start_checkout):
    checkout = start_checkout(BACKPACK)
    checkout.fill_shipping_information("Jane", "Doe", "94016")
    assert checkout.is_overview_displayed()

    checkout.cancel_from_overview()
    inventory = InventoryPage(checkout.driver)
    assert inventory.is_inventory_displayed()
    assert inventory.get_cart_count() == "1"
