"""
Test Suite: Kiểm thử Responsive / Cross-Device
Đây là điểm mạnh của Next-Gen testing — Percy so sánh visual
trên nhiều viewport cùng lúc mà không cần viết lại test.

Playwright emulate device, Percy chụp và so sánh layout responsive.
"""
import pytest
from playwright.sync_api import Page, BrowserContext, expect, sync_playwright
from percy import percy_snapshot


# ==============================================================
# Device configurations
# ==============================================================
DEVICES_TO_TEST = [
    "iPhone 14",
    "iPhone SE",
    "Pixel 7",
    "iPad (gen 11)",
]


# ==============================================================
# Mobile Tests (fixture device: iPhone 14)
# ==============================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    """Override context để chạy trên iPhone 14."""
    return {
        **playwright.devices["iPhone 14"],
    }


def test_mobile_login_page_layout(page: Page):
    """
    TC-M01: Layout trang login trên mobile.
    Kiểm tra: form không bị tràn, nút login đủ to để tap.
    """
    page.goto("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_visible()
    expect(page.locator("#user-name")).to_be_visible()
    percy_snapshot(page, name="[TC-M01] Login page - iPhone 14")


def test_mobile_full_checkout_flow(page: Page):
    """
    TC-M02: Toàn bộ luồng mua hàng trên mobile.
    Phát hiện: nút bị cắt, text tràn, modal không hiện đúng.
    """
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page.locator(".title")).to_have_text("Products")
    percy_snapshot(page, name="[TC-M02] Trang sản phẩm - iPhone 14")

    # Thêm 1 sản phẩm
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    percy_snapshot(page, name="[TC-M02] Sau khi thêm sản phẩm - iPhone 14")

    # Mở giỏ hàng
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".title")).to_have_text("Your Cart")
    percy_snapshot(page, name="[TC-M02] Trang giỏ hàng - iPhone 14")


def test_mobile_hamburger_menu(page: Page):
    """
    TC-M03: Menu hamburger trên mobile mở/đóng đúng.
    Visual bug thường gặp: menu che khuất nội dung, animation bị giật.
    """
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # Mở burger menu
    page.locator("#react-burger-menu-btn").click()
    page.wait_for_selector(".bm-menu-wrap", state="visible")
    percy_snapshot(page, name="[TC-M03] Hamburger menu mở - iPhone 14")

    # Đóng lại
    page.locator("#react-burger-cross-btn").click()
    page.wait_for_selector(".bm-menu-wrap", state="hidden")
    percy_snapshot(page, name="[TC-M03] Hamburger menu đóng - iPhone 14")


def test_mobile_product_detail_page(page: Page):
    """
    TC-M04: Trang chi tiết sản phẩm trên mobile.
    Visual: ảnh sản phẩm, mô tả, giá, nút Add to cart phải hiển thị đúng thứ tự.
    """
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # Click vào tên sản phẩm để vào trang detail
    page.locator(".inventory_item_name").first.click()
    expect(page.locator(".inventory_details_name")).to_be_visible()
    percy_snapshot(page, name="[TC-M04] Chi tiết sản phẩm - iPhone 14")


def test_mobile_sort_interaction(page: Page):
    """
    TC-M05: Dropdown sort trên mobile — tap target đủ lớn không?
    Visual bug: dropdown trên mobile đôi khi render ra ngoài viewport.
    """
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    sort_dropdown = page.locator('[data-test="product-sort-container"]')
    sort_dropdown.select_option("za")
    percy_snapshot(page, name="[TC-M05] Sort Z→A - iPhone 14")

    sort_dropdown.select_option("hilo")
    percy_snapshot(page, name="[TC-M05] Sort giá cao→thấp - iPhone 14")
