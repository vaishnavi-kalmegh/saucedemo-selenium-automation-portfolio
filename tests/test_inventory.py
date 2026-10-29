import pytest

from data.catalog import (
    PRODUCTS,
    SORT_NAME_ASC,
    SORT_NAME_DESC,
    SORT_PRICE_ASC,
    SORT_PRICE_DESC,
)


@pytest.mark.inventory
def test_inventory_shows_every_product(logged_in):
    assert logged_in.get_product_count() == len(PRODUCTS)
    assert sorted(logged_in.get_product_names()) == sorted(PRODUCTS)


@pytest.mark.inventory
def test_inventory_prices_match_catalog(logged_in):
    displayed = dict(zip(logged_in.get_product_names(), logged_in.get_product_prices()))
    assert displayed == PRODUCTS


@pytest.mark.inventory
def test_default_sort_is_name_ascending(logged_in):
    names = logged_in.get_product_names()
    assert names == sorted(names)


@pytest.mark.inventory
@pytest.mark.parametrize(
    "option, key, reverse",
    [
        (SORT_NAME_ASC, "name", False),
        (SORT_NAME_DESC, "name", True),
        (SORT_PRICE_ASC, "price", False),
        (SORT_PRICE_DESC, "price", True),
    ],
    ids=["name-a-to-z", "name-z-to-a", "price-low-to-high", "price-high-to-low"],
)
def test_sort_orders_products(logged_in, option, key, reverse):
    logged_in.sort_by(option)

    if key == "name":
        actual = logged_in.get_product_names()
    else:
        actual = logged_in.get_product_prices()
    assert actual == sorted(actual, reverse=reverse)


@pytest.mark.inventory
def test_sorting_by_price_keeps_names_paired_with_prices(logged_in):
    logged_in.sort_by(SORT_PRICE_ASC)
    displayed = dict(zip(logged_in.get_product_names(), logged_in.get_product_prices()))
    assert displayed == PRODUCTS


@pytest.mark.inventory
def test_adding_every_product_updates_cart_badge(logged_in):
    for name in logged_in.get_product_names():
        logged_in.add_to_cart(name)
    assert logged_in.get_cart_count() == str(len(PRODUCTS))


@pytest.mark.inventory
def test_removing_a_product_decrements_cart_badge(logged_in):
    first, second = list(PRODUCTS)[:2]
    logged_in.add_to_cart(first)
    logged_in.add_to_cart(second)
    assert logged_in.get_cart_count() == "2"

    logged_in.remove_from_cart(first)
    assert logged_in.get_cart_count() == "1"
