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
    driver.get("http://http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("dabdulwahabsarwar91@gmail.com")
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/builder/info"))
    assert "/builder/info" in driver.current_url

def test_empty_fields_login(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/login")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Missing fields" in error_div.text or "Invalid credentials" in error_div.text

def test_login_submit_button_exists(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert "Log in" in button.text

def test_login_email_field_exists(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    email_field = driver.find_element(By.ID, "email")
    assert email_field.get_attribute("placeholder") == "name@example.com"

# Signup Test Cases
def test_duplicate_email_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "name").send_keys("Duplicate User")
    driver.find_element(By.ID, "email").send_keys("abdulwahabsarwar91@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Test@1234")
    driver.find_element(By.ID, "terms").click()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "User already exists" in error_div.text

def test_weak_password_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "name").send_keys("Weak User")
    driver.find_element(By.ID, "email").send_keys("weakuser@example.com")
    driver.find_element(By.ID, "password").send_keys("weak")
    driver.find_element(By.ID, "terms").click()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Password must be at least 8 characters long" in error_div.text

def test_missing_terms_agreement_signup(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "name").send_keys("Missing Terms User")
    driver.find_element(By.ID, "email").send_keys("missingterms@example.com")
    driver.find_element(By.ID, "password").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Please agree to the Terms of Service and Privacy Policy" in error_div.text

def test_signup_name_field_exists(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/signup")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "name")))
    name_field = driver.find_element(By.ID, "name")
    assert name_field.get_attribute("placeholder") == "John Doe"

# Page Load Test Cases
def test_login_page_loads(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Log in')]")))
    assert "Log in" in driver.page_source

def test_signup_page_loads(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/signup")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Create an account')]")))
    assert "Create an account" in driver.page_source

# Additional Test Case for New System Feature
def test_remember_me_checkbox_exists(driver):
    print(f"Setting up test at {time.strftime('%Y-%m-%d %H:%M:%S PKT')}")
    driver.get("http://http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "remember")))
    checkbox = driver.find_element(By.ID, "remember")
    assert checkbox.get_attribute("type") == "checkbox"