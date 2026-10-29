import pytest

from pages.login_page import LoginPage
from pages.menu_page import MenuPage

PROTECTED_PAGES = ["inventory.html", "cart.html", "checkout-step-one.html"]


@pytest.mark.session
def test_logout_returns_to_login_page(logged_in):
    MenuPage(logged_in.driver).logout()
    assert LoginPage(logged_in.driver).is_loaded()


@pytest.mark.session
def test_inventory_is_inaccessible_after_logout(logged_in, base_url):
    MenuPage(logged_in.driver).logout()
    login = LoginPage(logged_in.driver)
    assert login.is_loaded()

    login.open_url(base_url + "inventory.html")
    assert "logged in" in login.get_error_message()


@pytest.mark.session
@pytest.mark.parametrize("page", PROTECTED_PAGES)
def test_protected_pages_redirect_anonymous_visitors_to_login(driver, base_url, page):
    login = LoginPage(driver)
    login.open_url(base_url + page)

    assert login.is_loaded()
    assert "logged in" in login.get_error_message()


@pytest.mark.session
def test_reset_app_state_empties_cart(logged_in):
    logged_in.add_backpack_to_cart()
    assert logged_in.get_cart_count() == "1"

    MenuPage(logged_in.driver).reset_app_state()
    logged_in.wait_for_cart_to_be_empty()
    assert not logged_in.cart_badge_is_visible()
