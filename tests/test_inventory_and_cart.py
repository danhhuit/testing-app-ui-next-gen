"""
Test Suite: Kiểm thử trang sản phẩm và giỏ hàng
Bao gồm: sorting, add/remove cart, visual bug detection.

Đây là nơi visual testing tỏa sáng nhất — functional test
không phát hiện được ảnh sản phẩm sai hoặc giá hiển thị lệch.
"""
import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot

from tests.pages.inventory_page import InventoryPage
from tests.pages.cart_page import CartPage
from tests.utils.fixtures import PRODUCTS


class TestInventory:

    def test_all_products_displayed(self, logged_in_page: Page):
        """
        TC-I01: Kiểm tra tất cả 6 sản phẩm hiển thị đúng.
        Visual: ảnh sản phẩm, tên, giá, nút phải căn chỉnh đúng.
        """
        inventory = InventoryPage(logged_in_page)
        all_names = inventory.get_all_product_names()
        assert len(all_names) == 6, f"Cần 6 sản phẩm, thực tế có {len(all_names)}"
        percy_snapshot(logged_in_page, name="[TC-I01] Danh sách đầy đủ 6 sản phẩm")

    def test_sort_products_name_a_to_z(self, logged_in_page: Page):
        """
        TC-I02: Sắp xếp sản phẩm A→Z.
        Functional: thứ tự đúng alphabet. Visual: dropdown hiển thị đúng tùy chọn.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.sort_by("az")

        names = inventory.get_all_product_names()
        assert names == sorted(names), "Sản phẩm chưa được sắp xếp A→Z"
        percy_snapshot(logged_in_page, name="[TC-I02] Sort A→Z")

    def test_sort_products_name_z_to_a(self, logged_in_page: Page):
        """
        TC-I03: Sắp xếp sản phẩm Z→A.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.sort_by("za")

        names = inventory.get_all_product_names()
        assert names == sorted(names, reverse=True), "Sản phẩm chưa được sắp xếp Z→A"
        percy_snapshot(logged_in_page, name="[TC-I03] Sort Z→A")

    def test_sort_products_price_low_to_high(self, logged_in_page: Page):
        """
        TC-I04: Sắp xếp giá từ thấp đến cao.
        Functional: thứ tự giá đúng. Visual: nhãn giá có thể bị xáo trộn.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.sort_by("lohi")

        prices = [float(p.replace("$", "")) for p in inventory.get_all_prices()]
        assert prices == sorted(prices), "Giá chưa được sắp xếp thấp→cao"
        percy_snapshot(logged_in_page, name="[TC-I04] Sort giá thấp→cao")

    def test_sort_products_price_high_to_low(self, logged_in_page: Page):
        """
        TC-I05: Sắp xếp giá từ cao đến thấp.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.sort_by("hilo")

        prices = [float(p.replace("$", "")) for p in inventory.get_all_prices()]
        assert prices == sorted(prices, reverse=True), "Giá chưa được sắp xếp cao→thấp"
        percy_snapshot(logged_in_page, name="[TC-I05] Sort giá cao→thấp")

    def test_add_single_product_to_cart(self, logged_in_page: Page):
        """
        TC-I06: Thêm 1 sản phẩm vào giỏ.
        Functional: badge hiển thị số 1. Visual: nút đổi từ "Add" sang "Remove".
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])

        assert inventory.get_cart_count() == 1
        percy_snapshot(logged_in_page, name="[TC-I06] Giỏ hàng sau khi thêm 1 sản phẩm")

    def test_add_multiple_products_to_cart(self, logged_in_page: Page):
        """
        TC-I07: Thêm nhiều sản phẩm, kiểm tra badge tăng đúng.
        Visual bug thường gặp: badge bị ẩn khi số > 1 chữ số.
        """
        inventory = InventoryPage(logged_in_page)
        products_to_add = [PRODUCTS["backpack"], PRODUCTS["bike_light"], PRODUCTS["bolt_shirt"]]

        for i, product in enumerate(products_to_add, 1):
            inventory.add_product_to_cart(product)
            assert inventory.get_cart_count() == i

        percy_snapshot(logged_in_page, name="[TC-I07] Giỏ hàng với 3 sản phẩm")

    def test_remove_product_from_cart(self, logged_in_page: Page):
        """
        TC-I08: Thêm rồi xóa sản phẩm — badge phải biến mất.
        Visual: nút phải chuyển về "Add to cart".
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])
        assert inventory.get_cart_count() == 1

        inventory.remove_product_from_cart(PRODUCTS["backpack"])
        assert inventory.get_cart_count() == 0
        percy_snapshot(logged_in_page, name="[TC-I08] Sau khi xóa khỏi giỏ")

    def test_add_all_products_to_cart(self, logged_in_page: Page):
        """
        TC-I09: Thêm tất cả 6 sản phẩm.
        Stress test visual: layout badge khi số = 6.
        """
        inventory = InventoryPage(logged_in_page)
        for product_id in PRODUCTS.values():
            inventory.add_product_to_cart(product_id)

        assert inventory.get_cart_count() == 6
        percy_snapshot(logged_in_page, name="[TC-I09] Toàn bộ 6 sản phẩm trong giỏ")

    def test_problem_user_has_visual_bugs(self, problem_user_page: Page):
        """
        TC-I10: MINH HỌA — problem_user có ảnh sản phẩm bị sai (tất cả
        hiển thị cùng 1 ảnh). Playwright không phát hiện được, chỉ Percy mới thấy.
        Đây là trường hợp use case chính của Next-Gen Visual Testing.
        """
        percy_snapshot(problem_user_page, name="[TC-I10] Problem user - ảnh sản phẩm bị lỗi (Percy phát hiện)")
        # Playwright vẫn thấy 6 sản phẩm → PASS
        products = InventoryPage(problem_user_page).get_all_product_names()
        assert len(products) == 6  # Functional test PASS nhưng visual BỊ LỖI


class TestCart:

    def test_cart_shows_correct_items(self, logged_in_page: Page):
        """
        TC-C01: Sản phẩm trong giỏ khớp với sản phẩm đã thêm.
        Visual: tên, giá, ảnh trong cart page phải đúng.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.add_product_to_cart(PRODUCTS["backpack"])
        inventory.add_product_to_cart(PRODUCTS["bike_light"])
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        cart.assert_on_cart_page()
        assert cart.get_item_count() == 2

        item_names = cart.get_item_names()
        assert "Sauce Labs Backpack" in item_names
        assert "Sauce Labs Bike Light" in item_names
        percy_snapshot(logged_in_page, name="[TC-C01] Trang giỏ hàng - 2 sản phẩm")

    def test_empty_cart_page(self, logged_in_page: Page):
        """
        TC-C02: Mở trang giỏ hàng khi chưa có gì.
        Visual: layout empty state phải đúng, không bị lệch.
        """
        inventory = InventoryPage(logged_in_page)
        inventory.go_to_cart()

        cart = CartPage(logged_in_page)
        assert cart.get_item_count() == 0
        percy_snapshot(logged_in_page, name="[TC-C02] Giỏ hàng trống")
