"""
Test Suite: Kiểm thử trang chi tiết sản phẩm (Product Detail)
Thường bị bỏ qua nhưng hay có visual bug về image, layout.
"""
import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot

from tests.pages.inventory_page import InventoryPage
from tests.utils.fixtures import PRODUCTS


class TestProductDetail:

    def test_product_detail_page_elements(self, logged_in_page: Page):
        """
        TC-P01: Trang chi tiết sản phẩm có đủ thành phần cần thiết.
        Visual: ảnh lớn, tên, mô tả, giá, nút thêm giỏ hàng, nút back.
        """
        logged_in_page.locator(".inventory_item_name").first.click()

        expect(logged_in_page.locator(".inventory_details_img")).to_be_visible()
        expect(logged_in_page.locator(".inventory_details_name")).to_be_visible()
        expect(logged_in_page.locator(".inventory_details_price")).to_be_visible()
        expect(logged_in_page.locator(".inventory_details_desc")).to_be_visible()
        percy_snapshot(logged_in_page, name="[TC-P01] Trang chi tiết sản phẩm")

    def test_add_to_cart_from_detail_page(self, logged_in_page: Page):
        """
        TC-P02: Thêm vào giỏ hàng từ trang chi tiết.
        Visual: badge cart badge xuất hiện, nút đổi thành "Remove".
        """
        logged_in_page.locator(".inventory_item_name").first.click()
        add_button = logged_in_page.locator('[data-test^="add-to-cart"]')
        add_button.click()

        expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
        expect(logged_in_page.locator('[data-test^="remove"]')).to_be_visible()
        percy_snapshot(logged_in_page, name="[TC-P02] Thêm vào giỏ từ trang chi tiết")

    def test_back_button_returns_to_list(self, logged_in_page: Page):
        """
        TC-P03: Nút Back quay về đúng trang danh sách.
        Visual: trang list render lại đúng, không mất state.
        """
        logged_in_page.locator(".inventory_item_name").first.click()
        logged_in_page.locator('[data-test="back-to-products"]').click()

        InventoryPage(logged_in_page).assert_on_inventory_page()
        percy_snapshot(logged_in_page, name="[TC-P03] Quay lại danh sách từ detail")

    @pytest.mark.parametrize("product_index", [0, 1, 2, 3, 4, 5])
    def test_all_product_detail_pages(self, logged_in_page: Page, product_index: int):
        """
        TC-P04: Kiểm tra từng trang detail của 6 sản phẩm.
        Phát hiện: sản phẩm nào bị sai ảnh, sai giá trên trang detail.
        """
        product_names = logged_in_page.locator(".inventory_item_name").all()
        if product_index < len(product_names):
            product_name = product_names[product_index].inner_text()
            product_names[product_index].click()

            expect(logged_in_page.locator(".inventory_details_name")).to_have_text(product_name)
            percy_snapshot(logged_in_page, name=f"[TC-P04] Detail sản phẩm #{product_index + 1}: {product_name[:20]}")
            logged_in_page.go_back()
