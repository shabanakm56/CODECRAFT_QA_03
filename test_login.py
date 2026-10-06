"""Automated login tests for Sauce Demo (https://www.saucedemo.com)
Tools: Python, Selenium WebDriver, pytest
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com"
VALID_PASSWORD = "secret_sauce"


@pytest.fixture
def driver():
    """Start a fresh Chrome browser for each test and close it afterwards."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1280,900")
    # options.add_argument("--headless=new")  # uncomment to run without a visible browser
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()


def login(driver, username, password):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def error_text(driver):
    return WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    ).text


# ---------- Positive test cases ----------

def test_valid_login_standard_user(driver):
    """TC01: valid credentials open the inventory page."""
    login(driver, "standard_user", VALID_PASSWORD)
    WebDriverWait(driver, 5).until(EC.url_contains("/inventory.html"))
    assert driver.find_element(By.CSS_SELECTOR, "[data-test='title']").text == "Products"


def test_logout_after_login(driver):
    """TC02: user can log out and return to the login page."""
    login(driver, "standard_user", VALID_PASSWORD)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    ).click()
    assert driver.find_element(By.ID, "login-button").is_displayed()


# ---------- Negative test cases ----------

@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("standard_user", "wrong_password",
         "Username and password do not match any user in this service"),
        ("invalid_user", VALID_PASSWORD,
         "Username and password do not match any user in this service"),
        ("invalid_user", "wrong_password",
         "Username and password do not match any user in this service"),
        ("", "", "Username is required"),
        ("", VALID_PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", VALID_PASSWORD, "this user has been locked out"),
    ],
    ids=[
        "TC03_wrong_password",
        "TC04_wrong_username",
        "TC05_both_invalid",
        "TC06_both_empty",
        "TC07_empty_username",
        "TC08_empty_password",
        "TC09_locked_out_user",
    ],
)
def test_invalid_login(driver, username, password, expected_error):
    """TC03-TC09: invalid or missing credentials show the right error and block login."""
    login(driver, username, password)
    assert expected_error in error_text(driver)
    assert "/inventory.html" not in driver.current_url


def test_protected_page_requires_login(driver):
    """TC10: opening the inventory page directly without logging in is blocked."""
    driver.get(f"{BASE_URL}/inventory.html")
    assert "Epic sadface" in error_text(driver)