import os
import pytest

from appium import webdriver
from appium.options.android import UiAutomator2Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SAUCEDEMO_URL = "https://www.saucedemo.com/"


@pytest.fixture
def mobile_driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.getenv("ANDROID_DEVICE_NAME", "Android Emulator")

    udid = os.getenv("ANDROID_UDID")
    if udid:
        options.udid = udid

    options.browser_name = "Chrome"

    options.set_capability("appium:noReset", True)
    options.set_capability("appium:newCommandTimeout", 120)
    options.set_capability("appium:chromedriverAutodownload", True)

    options.set_capability(
        "goog:chromeOptions",
        {
            "androidPackage": "com.android.chrome",
            "args": [
                "--disable-fre",
                "--no-first-run",
                "--disable-popup-blocking",
            ],
        },
    )

    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4723",
        options=options,
    )

    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def login_saucedemo(driver):
    wait = WebDriverWait(driver, 30)

    driver.get(SAUCEDEMO_URL)

    username_input = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#user-name"))
    )
    password_input = driver.find_element(By.CSS_SELECTOR, "#password")
    login_button = driver.find_element(By.CSS_SELECTOR, "#login-button")

    username_input.clear()
    username_input.send_keys("standard_user")

    password_input.clear()
    password_input.send_keys("secret_sauce")

    login_button.click()

    title = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
    )

    assert title.text == "Products"


def test_mobile_web_login_saucedemo_appium(mobile_driver):
    """
    TC-APP-01:
    Kiểm thử đăng nhập SauceDemo trên Chrome Android bằng Appium.
    """
    login_saucedemo(mobile_driver)


def test_mobile_web_add_to_cart_appium(mobile_driver):
    """
    TC-APP-02:
    Login -> thêm sản phẩm vào giỏ -> kiểm tra badge cart = 1.
    """
    wait = WebDriverWait(mobile_driver, 30)

    login_saucedemo(mobile_driver)

    add_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#add-to-cart-sauce-labs-backpack")
        )
    )
    add_button.click()

    badge = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".shopping_cart_badge")
        )
    )

    assert badge.text == "1"


def test_mobile_web_cart_page_appium(mobile_driver):
    """
    TC-APP-03:
    Login -> thêm sản phẩm -> mở giỏ hàng -> kiểm tra trang Your Cart.
    """
    wait = WebDriverWait(mobile_driver, 30)

    login_saucedemo(mobile_driver)

    add_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#add-to-cart-sauce-labs-backpack")
        )
    )
    add_button.click()

    cart_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".shopping_cart_link")
        )
    )
    cart_button.click()

    cart_title = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".title")
        )
    )

    assert cart_title.text == "Your Cart"