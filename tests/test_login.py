import pytest

from data.users import ACCEPTED_USERS, DEMO_PASSWORD, LOCKED_OUT_USER
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.login
def test_valid_login_opens_inventory(driver, base_url, credentials):
    LoginPage(driver).load(base_url).login(credentials["username"], credentials["password"])
    assert InventoryPage(driver).is_inventory_displayed()


@pytest.mark.login
def test_login_rejects_invalid_username(driver, base_url, credentials):
    LoginPage(driver).load(base_url).login("invalid_user", credentials["password"])
    assert "Username and password do not match" in LoginPage(driver).get_error_message()


@pytest.mark.login
def test_login_rejects_invalid_password(driver, base_url, credentials):
    LoginPage(driver).load(base_url).login(credentials["username"], "wrong_password")
    assert "Username and password do not match" in LoginPage(driver).get_error_message()


@pytest.mark.login
def test_login_requires_username(driver, base_url, credentials):
    LoginPage(driver).load(base_url).login("", credentials["password"])
    assert "Username is required" in LoginPage(driver).get_error_message()


@pytest.mark.login
def test_login_requires_password(driver, base_url, credentials):
    LoginPage(driver).load(base_url).login(credentials["username"], "")
    assert "Password is required" in LoginPage(driver).get_error_message()


@pytest.mark.login
def test_locked_out_user_cannot_login(driver, base_url):
    LoginPage(driver).load(base_url).login(LOCKED_OUT_USER, DEMO_PASSWORD)
    assert "locked out" in LoginPage(driver).get_error_message().lower()


@pytest.mark.login
@pytest.mark.parametrize("username", ACCEPTED_USERS)
def test_every_accepted_user_type_can_login(driver, base_url, username):
    LoginPage(driver).load(base_url).login(username, DEMO_PASSWORD)

    # performance_glitch_user is intentionally slow, so allow a longer wait here.
    inventory = InventoryPage(driver, timeout=20)
    inventory.wait_for_url("inventory.html")
    assert inventory.is_inventory_displayed()


@pytest.mark.login
def test_login_error_message_can_be_dismissed(driver, base_url):
    login = LoginPage(driver).load(base_url)
    login.login("invalid_user", DEMO_PASSWORD)
    assert login.get_error_message()
    login.dismiss_error()
    assert login.is_loaded()
