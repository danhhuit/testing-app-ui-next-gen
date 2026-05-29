"""
Test Suite: Kiểm thử luồng đăng nhập
Bao gồm: happy path, negative cases, và visual testing với Percy.

Mục đích minh họa:
- Functional test (Playwright) phát hiện lỗi logic
- Visual test (Percy) phát hiện lỗi giao diện
"""
import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot

from tests.pages.login_page import LoginPage
from tests.utils.fixtures import USERS


class TestLogin:

    def test_login_standard_user(self, page: Page):
        """
        TC-L01: Đăng nhập thành công với tài khoản hợp lệ.
        Kiểm tra: redirect đúng trang, title hiển thị đúng.
        """
        login = LoginPage(page)
        login.navigate()
        percy_snapshot(page, name="[TC-L01] Trang đăng nhập - trạng thái mặc định")

        login.login(**USERS["standard"])
        expect(page.locator(".title")).to_have_text("Products")
        percy_snapshot(page, name="[TC-L01] Sau đăng nhập - trang sản phẩm")

    def test_login_locked_out_user(self, page: Page):
        """
        TC-L02: Đăng nhập với tài khoản bị khóa.
        Kiểm tra: hiển thị thông báo lỗi đúng nội dung và đúng vị trí.
        Visual bug thường gặp: icon lỗi bị ẩn, màu nền error message sai.
        """
        login = LoginPage(page)
        login.navigate()
        login.login(**USERS["locked"])

        error_msg = login.get_error_message()
        assert "locked out" in error_msg.lower(), f"Thông báo lỗi không đúng: {error_msg}"
        percy_snapshot(page, name="[TC-L02] Thông báo lỗi - tài khoản bị khóa")

    def test_login_wrong_password(self, page: Page):
        """
        TC-L03: Đăng nhập với mật khẩu sai.
        Kiểm tra: thông báo lỗi xuất hiện, form không redirect.
        """
        login = LoginPage(page)
        login.navigate()
        login.login(username="standard_user", password="wrong_password_123")

        login.assert_on_login_page()
        error_msg = login.get_error_message()
        assert "Username and password do not match" in error_msg
        percy_snapshot(page, name="[TC-L03] Thông báo lỗi - sai mật khẩu")

    def test_login_empty_fields(self, page: Page):
        """
        TC-L04: Click đăng nhập khi để trống cả hai trường.
        Kiểm tra: form validation hoạt động đúng.
        Visual bug: placeholder text có thể biến mất, border màu sai.
        """
        login = LoginPage(page)
        login.navigate()
        login.login_button.click()

        error_msg = login.get_error_message()
        assert "Username is required" in error_msg
        percy_snapshot(page, name="[TC-L04] Validation lỗi - trường trống")

    def test_login_empty_password_only(self, page: Page):
        """
        TC-L05: Nhập username nhưng để trống password.
        """
        login = LoginPage(page)
        login.navigate()
        login.username_input.fill("standard_user")
        login.login_button.click()

        error_msg = login.get_error_message()
        assert "Password is required" in error_msg
        percy_snapshot(page, name="[TC-L05] Validation lỗi - thiếu password")

    def test_logout_and_redirect(self, logged_in_page: Page):
        """
        TC-L06: Đăng xuất và kiểm tra redirect về trang login.
        Visual bug: nút logout đôi khi ẩn đi sau khi sidebar mở.
        """
        from tests.pages.inventory_page import InventoryPage
        inventory = InventoryPage(logged_in_page)
        percy_snapshot(logged_in_page, name="[TC-L06] Sidebar menu mở")

        inventory.logout()
        LoginPage(logged_in_page).assert_on_login_page()
        percy_snapshot(logged_in_page, name="[TC-L06] Sau đăng xuất - quay về login")

    @pytest.mark.parametrize("username,password", [
        ("", "secret_sauce"),
        ("standard_user", ""),
        ("", ""),
        ("<script>alert(1)</script>", "secret_sauce"),
        ("' OR '1'='1", "' OR '1'='1"),
    ])
    def test_login_invalid_inputs(self, page: Page, username: str, password: str):
        """
        TC-L07: Kiểm tra các input không hợp lệ và XSS cơ bản.
        Playwright kiểm tra app không crash, Percy kiểm tra UI không vỡ.
        """
        login = LoginPage(page)
        login.navigate()
        login.login(username=username, password=password)
        # App phải hiển thị error hoặc vẫn ở trang login — không được crash
        login.assert_on_login_page()
