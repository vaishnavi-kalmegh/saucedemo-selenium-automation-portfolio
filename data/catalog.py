"""Static test data for the public SauceDemo storefront."""

PRODUCTS = {
    "Sauce Labs Backpack": 29.99,
    "Sauce Labs Bike Light": 9.99,
    "Sauce Labs Bolt T-Shirt": 15.99,
    "Sauce Labs Fleece Jacket": 49.99,
    "Sauce Labs Onesie": 7.99,
    "Test.allTheThings() T-Shirt (Red)": 15.99,
}

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
BOLT_SHIRT = "Sauce Labs Bolt T-Shirt"

# SauceDemo applies an 8% sales tax on the item total at checkout.
TAX_RATE = 0.08

# Sort dropdown option values used by the inventory page.
SORT_NAME_ASC = "az"
SORT_NAME_DESC = "za"
SORT_PRICE_ASC = "lohi"
SORT_PRICE_DESC = "hilo"
