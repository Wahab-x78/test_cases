import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

# Login Test Cases
def test_valid_login(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("testuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-gray-900")))
    assert "Welcome" in driver.page_source

def test_invalid_email_login(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.NAME, "email").send_keys("invalid@example")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Invalid email or password" in error_div.text

def test_invalid_password_login(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Failed to log in" in error_div.text or "Invalid email or password" in error_div.text

def test_empty_fields_login(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Email is required" in error_div.text or "Password is required" in error_div.text

# Signup Test Cases
def test_duplicate_email_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.NAME, "name").send_keys("Duplicate User")
    driver.find_element(By.NAME, "email").send_keys("test@example.com")
    driver.find_element(By.NAME, "password").send_keys("duppass123")
    driver.find_element(By.NAME, "confirmPassword").send_keys("duppass123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Email already exists" in error_div.text

def test_weak_password_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.NAME, "name").send_keys("Weak User")
    driver.find_element(By.NAME, "email").send_keys("weakuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("weak")
    driver.find_element(By.NAME, "confirmPassword").send_keys("weak")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Password must be at least 8 characters" in error_div.text

def test_missing_fields_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.NAME, "name").send_keys("Missing User")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-600")))
    assert "Email is required" in error_div.text or "Password is required" in error_div.text

# Page Load Test Cases
def test_login_page_loads(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome Back')]")))
    assert "Welcome Back" in driver.page_source

def test_signup_page_loads(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/signup")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Create Account')]")))
    assert "Create Account" in driver.page_source

# New Simple Test Case (Guaranteed to Pass)
def test_login_submit_button_exists(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert button.text == "Sign In"