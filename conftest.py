import base64
import os
from datetime import datetime

import pytest
from selenium import webdriver

BASE_URL = "https://www.saucedemo.com/"
DEFAULT_USERNAME = "standard_user"
DEFAULT_PASSWORD = "secret_sauce"


def _env_bool(name, default=True):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser to run tests with: chrome or firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="Force headless browser execution",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("BASE_URL", BASE_URL),
        help="Base URL for SauceDemo",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser_name = request.config.getoption("--browser").lower()
    cli_headless = request.config.getoption("--headless")
    is_headless = _env_bool("HEADLESS", True) if cli_headless is None else cli_headless

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        web_driver = webdriver.Chrome(options=options)
    else:
        options = webdriver.FirefoxOptions()
        if is_headless:
            options.add_argument("-headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        web_driver = webdriver.Firefox(options=options)

    web_driver.set_window_size(1920, 1080)
    yield web_driver
    web_driver.quit()


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/") + "/"


@pytest.fixture
def credentials():
    return {
        "username": os.getenv("SAUCE_USERNAME", DEFAULT_USERNAME),
        "password": os.getenv("SAUCE_PASSWORD", DEFAULT_PASSWORD),
    }


@pytest.fixture
def logged_in(driver, base_url, credentials):
    from pages.inventory_page import InventoryPage
    from pages.login_page import LoginPage

    LoginPage(driver).load(base_url).login(
        credentials["username"], credentials["password"]
    )

    inventory = InventoryPage(driver)
    inventory.wait_for_url("inventory.html")
    assert inventory.is_inventory_displayed(), "Login did not reach the SauceDemo inventory page."
    return inventory


@pytest.fixture
def checkout_page(logged_in):
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    logged_in.add_backpack_to_cart()
    logged_in.go_to_cart()
    CartPage(logged_in.driver).proceed_to_checkout()
    return CheckoutPage(logged_in.driver)


@pytest.fixture
def start_checkout(logged_in):
    """Return a callable that adds the named products and opens checkout step one."""
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    def _start(*product_names):
        for product_name in product_names:
            logged_in.add_to_cart(product_name)
        logged_in.go_to_cart()
        CartPage(logged_in.driver).proceed_to_checkout()
        return CheckoutPage(logged_in.driver)

    return _start


def _capture_failure(driver, test_name):
    screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    return file_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        test_driver = item.funcargs.get("driver")
        if test_driver:
            file_path = _capture_failure(test_driver, item.name)
            try:
                import pytest_html

                with open(file_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("ascii")
                report.extras = getattr(report, "extras", [])
                report.extras.append(
                    pytest_html.extras.image(image_data, mime_type="image/png")
                )
            except ImportError:
                pass
