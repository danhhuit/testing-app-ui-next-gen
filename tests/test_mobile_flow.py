import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot


# Cấu hình để chạy trên iPhone 14
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {
        **playwright.devices["iPhone 14"],
    }


def test_mobile_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    # AI chụp ảnh giao diện Mobile
    percy_snapshot(page, name="Giao diện Mobile iPhone 14")

    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    expect(page.locator(".title")).to_have_text("Products")