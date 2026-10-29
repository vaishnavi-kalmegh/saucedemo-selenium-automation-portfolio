from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def xpath_literal(value):
    """Return value as a safely quoted XPath string literal."""
    if '"' not in value:
        return f'"{value}"'
    if "'" not in value:
        return f"'{value}'"
    parts = value.split('"')
    return "concat(" + ", '\"', ".join(f'"{part}"' for part in parts) + ")"


def class_token(name):
    """XPath predicate matching one whole CSS class token on the current node."""
    return f"contains(concat(' ', normalize-space(@class), ' '), ' {name} ')"


def parse_money(text):
    """Parse labels such as 'Item total: $39.98' or '$9.99' into a float."""
    return float(text.split("$")[-1].strip())


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_url(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
        )
        self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
        )
        element.clear()
        element.send_keys(text)
        if element.get_attribute("value") != text:
            self.driver.execute_script(
                """
                const element = arguments[0];
                const value = arguments[1];
                const setter = Object.getOwnPropertyDescriptor(
                    HTMLInputElement.prototype, "value"
                ).set;
                setter.call(element, value);
                element.dispatchEvent(new Event("input", {bubbles: true}));
                element.dispatchEvent(new Event("change", {bubbles: true}));
                """,
                element,
                text,
            )
        self.wait.until(lambda driver: element.get_attribute("value") == text)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text.strip()

    def is_visible(self, locator):
        try:
            return bool(self.wait.until(EC.visibility_of_element_located(locator)))
        except TimeoutException:
            return False

    def wait_until_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_url(self, fragment):
        self.wait.until(EC.url_contains(fragment))
