"""
conftest.py — pytest tự động load file này.
Đăng ký các fixtures dùng chung ở đây.
"""
import pytest
from playwright.sync_api import Page
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.utils.fixtures import USERS


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Page đã đăng nhập sẵn với standard_user."""
    login = LoginPage(page)
    login.navigate()
    login.login(**USERS["standard"])
    InventoryPage(page).assert_on_inventory_page()
    return page


@pytest.fixture
def problem_user_page(page: Page) -> Page:
    """Page đăng nhập bằng problem_user."""
    login = LoginPage(page)
    login.navigate()
    login.login(**USERS["problem"])
    return page
