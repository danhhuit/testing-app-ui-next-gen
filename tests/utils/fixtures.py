"""
Fixtures và hằng số dùng chung cho toàn bộ test suite.
"""
import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage


# ==============================================================
# Tài khoản test của SauceDemo
# ==============================================================
USERS = {
    "standard": {"username": "standard_user", "password": "secret_sauce"},
    "locked":   {"username": "locked_out_user", "password": "secret_sauce"},
    "problem":  {"username": "problem_user",   "password": "secret_sauce"},
    "perf":     {"username": "performance_glitch_user", "password": "secret_sauce"},
}

# ID sản phẩm trên SauceDemo (dùng cho locator)
PRODUCTS = {
    "backpack":    "sauce-labs-backpack",
    "bike_light":  "sauce-labs-bike-light",
    "bolt_shirt":  "sauce-labs-bolt-t-shirt",
    "fleece":      "sauce-labs-fleece-jacket",
    "onesie":      "sauce-labs-onesie",
    "red_shirt":   "test.allthethings()-t-shirt-(red)",
}


# ==============================================================
# Fixtures tái sử dụng
# ==============================================================

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Fixture: trả về page đã đăng nhập sẵn với standard_user."""
    login = LoginPage(page)
    login.navigate()
    login.login(**USERS["standard"])
    InventoryPage(page).assert_on_inventory_page()
    return page


@pytest.fixture
def problem_user_page(page: Page) -> Page:
    """Fixture: trả về page đăng nhập bằng problem_user (có visual bug tự nhiên)."""
    login = LoginPage(page)
    login.navigate()
    login.login(**USERS["problem"])
    return page
