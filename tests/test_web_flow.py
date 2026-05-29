import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot


def test_login_and_add_to_cart(page: Page):
    # 1. Truy cập trang web & Chụp ảnh gốc
    page.goto("https://www.saucedemo.com/")
    percy_snapshot(page, name="Màn hình Đăng nhập")

    # 2. Đăng nhập
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # 3. Xác nhận đã vào trang sản phẩm
    expect(page.locator(".title")).to_have_text("Products")

    # ==============================================================
    # 💥 BẮT ĐẦU TẠO LỖI GIAO DIỆN (VISUAL BUG) BẰNG JAVASCRIPT
    # Đổi chữ "Products" thành màu đỏ và đổi chữ trong nút bấm
    page.evaluate("document.querySelector('.title').style.color = 'red';")
    page.evaluate("document.querySelector('#add-to-cart-sauce-labs-backpack').innerText = 'ADD TO TROLLEY';")
    # ==============================================================

    # 4. AI CHỤP ẢNH LẦN 2: Lúc này giao diện đã bị lỗi
    percy_snapshot(page, name="Danh sách Sản phẩm")

    # 5. Click thêm vào giỏ hàng
    # Nút bấm tuy bị đổi chữ, nhưng ID vẫn giữ nguyên.
    # Playwright (kiểm thử truyền thống) vẫn click được và báo PASS!
    page.locator("#add-to-cart-sauce-labs-backpack").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")