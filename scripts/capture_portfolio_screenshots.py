from pathlib import Path
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")
USERNAME = os.getenv("SAUCE_USERNAME", "standard_user")
PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
OUTPUT_DIR = Path("docs/images")


def wait_visible(driver, locator):
    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(BASE_URL)
        wait_visible(driver, (By.ID, "login-button"))
        driver.save_screenshot(str(OUTPUT_DIR / "login-page.png"))

        wait_visible(driver, (By.ID, "user-name")).send_keys(USERNAME)
        wait_visible(driver, (By.ID, "password")).send_keys(PASSWORD)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        ).click()
        wait_visible(driver, (By.CLASS_NAME, "inventory_list"))
        driver.save_screenshot(str(OUTPUT_DIR / "inventory-page.png"))

        report_path = (Path.cwd() / "reports" / "report.html").resolve()
        driver.get(report_path.as_uri())
        wait_visible(driver, (By.TAG_NAME, "body"))
        driver.save_screenshot(str(OUTPUT_DIR / "pytest-report.png"))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
