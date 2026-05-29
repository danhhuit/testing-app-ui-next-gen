"""
Test Suite: Kiểm thử luồng Checkout đầu đủ (E2E)
Đây là luồng nghiệp vụ quan trọng nhất — từ chọn hàng đến hoàn tất đơn.

Luồng: Login → Thêm hàng → Giỏ hàng → Checkout Info → Review → Complete
"""
import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot

from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.cart_page import CartPage, CheckoutPage
from tests.utils.fixtures import USERS, PRODUCTS


class TestCheckout:

    def test_checkout_complete_flow(self, logged_in_page: Page):
        """
        TC-E2E-01: Luồng hoàn chỉnh từ đầu đến cuối.
        Đây là test case quan trọng nhất — kiểm tra cả functional lẫn visual
        ở mọi bước của quy trình thanh toán.
        """
        # Bước 1: Thêm sản phẩm
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])
        inventory.add_product_to_cart(PRODUCTS["fleece"])
        percy_snapshot(logged_in_page, name="[E2E-01] Bước 1: Đã chọn 2 sản phẩm")

        # Bước 2: Vào giỏ hàng
        inventory.go_to_cart()
        cart = CartPage(logged_in_page)
        cart.assert_on_cart_page()
        assert cart.get_item_count() == 2
        percy_snapshot(logged_in_page, name="[E2E-01] Bước 2: Xem giỏ hàng")

        # Bước 3: Checkout - điền thông tin
        cart.proceed_to_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info(first_name="Nguyen", last_name="Van A", postal_code="70000")
        percy_snapshot(logged_in_page, name="[E2E-01] Bước 3: Điền thông tin giao hàng")
        checkout.continue_checkout()

        # Bước 4: Review đơn hàng
        expect(logged_in_page.locator(".title")).to_have_text("Checkout: Overview")
        percy_snapshot(logged_in_page, name="[E2E-01] Bước 4: Xem lại đơn hàng")

        # Bước 5: Hoàn tất
        checkout.finish_order()
        checkout.assert_order_complete()
        percy_snapshot(logged_in_page, name="[E2E-01] Bước 5: Đặt hàng thành công")

    def test_checkout_with_empty_first_name(self, logged_in_page: Page):
        """
        TC-E2E-02: Checkout với thiếu first name — phải hiện lỗi.
        Visual: error banner phải hiển thị đúng màu và vị trí.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info(first_name="", last_name="Van A", postal_code="70000")
        checkout.continue_checkout()

        expect(checkout.error_message).to_be_visible()
        assert "First Name is required" in checkout.error_message.inner_text()
        percy_snapshot(logged_in_page, name="[E2E-02] Lỗi validation - thiếu first name")

    def test_checkout_with_empty_postal_code(self, logged_in_page: Page):
        """
        TC-E2E-03: Checkout thiếu mã bưu chính.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["onesie"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info(first_name="Nguyen", last_name="Van B", postal_code="")
        checkout.continue_checkout()

        expect(checkout.error_message).to_be_visible()
        assert "Postal Code is required" in checkout.error_message.inner_text()
        percy_snapshot(logged_in_page, name="[E2E-03] Lỗi validation - thiếu postal code")

    def test_checkout_cancel_returns_to_cart(self, logged_in_page: Page):
        """
        TC-E2E-04: Nhấn Cancel ở màn checkout quay về giỏ hàng.
        Visual: không có sản phẩm nào bị mất khi hủy.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["bolt_shirt"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.proceed_to_checkout()

        # Click cancel
        logged_in_page.locator('[data-test="cancel"]').click()

        # Phải quay về cart và sản phẩm vẫn còn
        cart.assert_on_cart_page()
        assert cart.get_item_count() == 1
        percy_snapshot(logged_in_page, name="[E2E-04] Hủy checkout - quay lại giỏ hàng")

    def test_price_total_correct_on_overview(self, logged_in_page: Page):
        """
        TC-E2E-05: Tổng tiền trên trang overview phải khớp với giá sản phẩm.
        Functional: kiểm tra logic tính tiền. Visual: layout bảng giá phải chuẩn.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])   # $29.99
        inventory.add_product_to_cart(PRODUCTS["bike_light"]) # $9.99
        inventory.go_to_cart()

        CartPage(logged_in_page).proceed_to_checkout()
        checkout = CheckoutPage(logged_in_page)
        checkout.fill_info("Test", "User", "12345")
        checkout.continue_checkout()

        subtotal_text = logged_in_page.locator(".summary_subtotal_label").inner_text()
        subtotal = float(subtotal_text.replace("Item total: $", ""))
        assert abs(subtotal - 39.98) < 0.01, f"Tổng tiền sai: {subtotal} != 39.98"
        percy_snapshot(logged_in_page, name="[E2E-05] Tổng tiền trên trang overview")
