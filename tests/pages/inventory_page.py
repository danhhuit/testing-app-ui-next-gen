"""
Page Object Model cho trang danh sách sản phẩm.
"""
from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator(".title")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def get_product_card(self, product_name: str):
        """Trả về locator của card sản phẩm theo tên."""
        return self.page.locator(".inventory_item").filter(has_text=product_name)

    def get_add_to_cart_button(self, product_id: str):
        return self.page.locator(f'[data-test="add-to-cart-{product_id}"]')

    def get_remove_button(self, product_id: str):
        return self.page.locator(f'[data-test="remove-{product_id}"]')

    def get_all_product_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_all_prices(self) -> list[str]:
        return self.page.locator(".inventory_item_price").all_inner_texts()

    def sort_by(self, option: str):
        """option: 'az', 'za', 'lohi', 'hilo'"""
        self.sort_dropdown.select_option(option)

    def add_product_to_cart(self, product_id: str):
        self.get_add_to_cart_button(product_id).click()

    def remove_product_from_cart(self, product_id: str):
        self.get_remove_button(product_id).click()

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.cart_link.click()

    def logout(self):
        self.burger_menu.click()
        self.page.wait_for_selector("#logout_sidebar_link", state="visible")
        self.logout_link.click()

    def assert_on_inventory_page(self):
        expect(self.title).to_have_text("Products")
