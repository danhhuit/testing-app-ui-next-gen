"""
Page Object Model cho trang đăng nhập SauceDemo.
Tách biệt logic locator và action khỏi test case → dễ bảo trì hơn.
"""
from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator('[data-test="error"]')

    def navigate(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        return self.error_message.inner_text()

    def assert_on_login_page(self):
        expect(self.page).to_have_url(self.URL)
        expect(self.login_button).to_be_visible()
