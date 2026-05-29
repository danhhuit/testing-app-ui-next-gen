"""
Test Suite: MINH HỌA VISUAL BUGS cho đề tài nghiên cứu
=======================================================
File này là trái tim của PoC — cố tình tạo ra các lỗi giao diện
mà functional test (Playwright) KHÔNG phát hiện được,
nhưng Visual AI (Percy) PHÁT HIỆN NGAY.

Mỗi test case minh họa một loại visual bug khác nhau,
kèm comment giải thích tại sao đây là vấn đề thực tế.
"""
import pytest
from playwright.sync_api import Page, expect
from percy import percy_snapshot

from tests.pages.inventory_page import InventoryPage
from tests.utils.fixtures import PRODUCTS


class TestVisualBugs:
    """
    Bộ test minh họa 6 loại visual bug phổ biến trong thực tế.
    Tất cả đều bị Playwright bỏ qua, nhưng Percy sẽ flag.
    """

    def test_vb01_text_color_bug(self, logged_in_page: Page):
        """
        VB-01: Lỗi màu chữ (Color Bug)
        --------------------------------
        Tình huống thực tế: Developer commit CSS sai, đổi màu brand color.
        Playwright: PASS (text vẫn present, nội dung đúng)
        Percy: FAIL (pixel diff phát hiện màu thay đổi)
        """
        inventory = InventoryPage(logged_in_page)
        inventory.assert_on_inventory_page()

        # Inject lỗi màu sắc
        logged_in_page.evaluate("""
            document.querySelector('.title').style.color = '#CC0000';
            document.querySelector('.app_logo').style.color = '#CC0000';
        """)

        # Playwright vẫn PASS — nội dung không thay đổi
        expect(logged_in_page.locator(".title")).to_have_text("Products")
        percy_snapshot(logged_in_page, name="[VB-01] Lỗi màu chữ - Playwright PASS, Percy FAIL")

    def test_vb02_text_content_bug(self, logged_in_page: Page):
        """
        VB-02: Lỗi nội dung text (Content Bug)
        ----------------------------------------
        Tình huống thực tế: Sai bản dịch, hoặc i18n bị lỗi ở môi trường staging.
        Playwright: PASS nếu test không check text cụ thể
        Percy: FAIL ngay lập tức
        """
        logged_in_page.evaluate("""
            document.querySelector('#add-to-cart-sauce-labs-backpack').innerText = 'ADD TO TROLLEY';
            document.querySelector('#add-to-cart-sauce-labs-bike-light').innerText = 'MUA NGAY';
            document.querySelector('.app_logo').innerText = 'Swag Lab';
        """)

        # Functional test không check text nút → PASS
        logged_in_page.locator("#add-to-cart-sauce-labs-backpack").click()
        expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
        percy_snapshot(logged_in_page, name="[VB-02] Lỗi nội dung text - Playwright PASS, Percy FAIL")

    def test_vb03_layout_shift_bug(self, logged_in_page: Page):
        """
        VB-03: Lỗi dịch chuyển layout (Layout Shift Bug)
        --------------------------------------------------
        Tình huống thực tế: CSS media query bị conflict, phần tử lệch vị trí.
        Playwright: PASS (element vẫn tồn tại và clickable)
        Percy: FAIL (vị trí pixel thay đổi)
        """
        logged_in_page.evaluate("""
            const header = document.querySelector('.primary_header');
            if (header) header.style.marginTop = '40px';
            const cart = document.querySelector('.shopping_cart_link');
            if (cart) cart.style.marginTop = '-20px';
        """)

        # Playwright không check vị trí → vẫn PASS
        expect(logged_in_page.locator(".shopping_cart_link")).to_be_visible()
        percy_snapshot(logged_in_page, name="[VB-03] Lỗi layout shift - Playwright PASS, Percy FAIL")

    def test_vb04_missing_image_bug(self, logged_in_page: Page):
        """
        VB-04: Lỗi ảnh bị mất (Missing Image Bug)
        -------------------------------------------
        Tình huống thực tế: CDN lỗi, ảnh trả về 404, hiện ảnh placeholder.
        Playwright: PASS (alt text vẫn present)
        Percy: FAIL (pixel diff phát hiện broken image)
        """
        logged_in_page.evaluate("""
            const images = document.querySelectorAll('.inventory_item_img img');
            images.forEach((img, i) => {
                if (i % 2 === 0) {
                    img.src = 'https://invalid-url-that-will-fail.com/image.jpg';
                }
            });
        """)

        # Playwright không check src hay visual → PASS
        assert logged_in_page.locator(".inventory_item").count() == 6
        percy_snapshot(logged_in_page, name="[VB-04] Lỗi ảnh bị mất - Playwright PASS, Percy FAIL")

    def test_vb05_font_size_regression(self, logged_in_page: Page):
        """
        VB-05: Lỗi kích thước font (Font Regression)
        ----------------------------------------------
        Tình huống thực tế: Thay đổi CSS global làm vỡ typography.
        Playwright: PASS hoàn toàn
        Percy: FAIL vì font-size pixel thay đổi
        """
        logged_in_page.evaluate("""
            document.querySelectorAll('.inventory_item_name').forEach(el => {
                el.style.fontSize = '20px';
                el.style.fontWeight = '900';
            });
            document.querySelectorAll('.inventory_item_price').forEach(el => {
                el.style.fontSize = '10px';
                el.style.color = '#aaaaaa';
            });
        """)

        expect(logged_in_page.locator(".inventory_item_name").first).to_be_visible()
        percy_snapshot(logged_in_page, name="[VB-05] Lỗi kích thước font - Playwright PASS, Percy FAIL")

    def test_vb06_button_style_regression(self, logged_in_page: Page):
        """
        VB-06: Lỗi style nút bấm (Button Style Regression)
        ----------------------------------------------------
        Tình huống thực tế: Component library update làm thay đổi style button.
        Playwright: PASS (nút vẫn clickable)
        Percy: FAIL (border-radius, background-color thay đổi)
        """
        logged_in_page.evaluate("""
            document.querySelectorAll('.btn_inventory').forEach(btn => {
                btn.style.backgroundColor = '#28a745';
                btn.style.borderRadius = '20px';
                btn.style.border = '3px dashed #155724';
                btn.style.color = 'white';
            });
        """)

        # Nút vẫn click được → Playwright PASS
        logged_in_page.locator("#add-to-cart-sauce-labs-backpack").click()
        expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
        percy_snapshot(logged_in_page, name="[VB-06] Lỗi style nút bấm - Playwright PASS, Percy FAIL")

    def test_vb07_combined_visual_regression(self, logged_in_page: Page):
        """
        VB-07: Nhiều lỗi cùng lúc (Combined Regression)
        -------------------------------------------------
        Tình huống thực tế: Một thay đổi CSS toàn cục ảnh hưởng nhiều component.
        Percy hiển thị diff rõ ràng từng vùng bị ảnh hưởng.
        """
        logged_in_page.evaluate("""
            // Simulate a bad CSS variable change
            document.documentElement.style.setProperty('--color-primary', '#FF69B4');
            document.querySelector('.title').style.color = '#FF69B4';
            document.querySelector('.app_logo').style.color = '#FF69B4';
            document.querySelectorAll('.btn_inventory').forEach(btn => {
                btn.style.backgroundColor = '#FF69B4';
            });
            document.querySelectorAll('.inventory_item_price').forEach(el => {
                el.style.color = '#FF69B4';
            });
        """)

        # Mọi functional test vẫn PASS vì logic không thay đổi
        expect(logged_in_page.locator(".title")).to_have_text("Products")
        assert logged_in_page.locator(".inventory_item").count() == 6
        percy_snapshot(logged_in_page, name="[VB-07] CSS variable bị đổi - toàn trang pink")
