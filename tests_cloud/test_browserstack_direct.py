import json
import os
import urllib.parse
from contextlib import contextmanager

from playwright.sync_api import sync_playwright, expect


BROWSERSTACK_WS_ENDPOINT = "wss://cdp.browserstack.com/playwright?caps="


def get_browserstack_caps(test_name: str) -> dict:
    """
    Khai báo capability cho BrowserStack Cloud.
    Username và Access Key được lấy từ biến môi trường,
    tuyệt đối không hard-code key thật trong source code.
    """
    username = os.getenv("BROWSERSTACK_USERNAME")
    access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")

    if not username or not access_key:
        raise RuntimeError(
            "Missing BROWSERSTACK_USERNAME or BROWSERSTACK_ACCESS_KEY environment variable"
        )

    return {
        "browser": "chrome",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "11",
        "name": test_name,
        "build": "NextGen UI Testing - Playwright Cloud Direct",
        "project": "NextGen UI Testing",
        "browserstack.username": username,
        "browserstack.accessKey": access_key,
        "browserstack.debug": "true",
        "browserstack.networkLogs": "true",
        "browserstack.console": "info",
    }


def mark_session_status(page, status: str, reason: str):
    """
    Đánh dấu trạng thái pass/fail trên BrowserStack Dashboard.
    """
    executor_object = {
        "action": "setSessionStatus",
        "arguments": {
            "status": status,
            "reason": reason,
        },
    }

    page.evaluate(
        "_ => {}",
        f"browserstack_executor: {json.dumps(executor_object)}",
    )


@contextmanager
def browserstack_page(test_name: str):
    """
    Tạo page chạy trực tiếp trên BrowserStack Cloud bằng Playwright CDP.
    """
    caps = get_browserstack_caps(test_name)
    ws_endpoint = BROWSERSTACK_WS_ENDPOINT + urllib.parse.quote(json.dumps(caps))

    with sync_playwright() as playwright:
        browser = playwright.chromium.connect(ws_endpoint)
        page = browser.new_page()

        try:
            yield page
            mark_session_status(page, "passed", f"{test_name} passed")
        except Exception as error:
            try:
                mark_session_status(page, "failed", str(error))
            except Exception:
                pass
            raise
        finally:
            browser.close()


def login_saucedemo(page):
    """
    Hàm dùng chung để login vào SauceDemo.
    """
    page.goto("https://www.saucedemo.com/")

    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    expect(page.locator(".title")).to_have_text("Products")


def test_cloud_direct_login_saucedemo():
    """
    TC-BS-01:
    Kiểm thử đăng nhập SauceDemo trên BrowserStack Cloud.
    """
    with browserstack_page("TC-BS-01 Login SauceDemo") as page:
        login_saucedemo(page)


def test_cloud_direct_add_to_cart():
    """
    TC-BS-02:
    Kiểm thử login rồi thêm sản phẩm vào giỏ hàng trên BrowserStack Cloud.
    """
    with browserstack_page("TC-BS-02 Add product to cart") as page:
        login_saucedemo(page)

        page.locator("#add-to-cart-sauce-labs-backpack").click()
        expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_cloud_direct_cart_page():
    """
    TC-BS-03:
    Kiểm thử login, thêm sản phẩm và mở trang giỏ hàng trên BrowserStack Cloud.
    """
    with browserstack_page("TC-BS-03 Open cart page") as page:
        login_saucedemo(page)

        page.locator("#add-to-cart-sauce-labs-backpack").click()
        page.locator(".shopping_cart_link").click()

        expect(page.locator(".title")).to_have_text("Your Cart")
