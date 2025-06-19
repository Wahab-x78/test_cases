import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os
import requests

def get_chromedriver_version():
    result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
    return result.stdout.split()[0] if result.returncode == 0 else None

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    # Use a unique, writable directory with cleanup
    user_data_dir = f"/tmp/chrome-profile-{int(time.time())}"
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    try:
        # Verify ChromeDriver version compatibility
        chromedriver_version = get_chromedriver_version()
        if not chromedriver_version:
            raise Exception("ChromeDriver not found or incompatible")
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # Check if target URL is reachable
        response = requests.head("http://51.20.89.86:5000")
        if response.status_code != 200:
            raise Exception("Target server not reachable")
        yield driver
    except Exception as e:
        raise
    finally:
        driver.quit()
        if os.path.exists(user_data_dir):
            for item in os.listdir(user_data_dir):
                os.remove(os.path.join(user_data_dir, item))
            os.rmdir(user_data_dir)

def test_valid_login(driver):
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys("abdulwahabsarwar91@gmail.com")
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://51.20.89.86:5000/builder/info"))
    assert driver.current_url == "http://51.20.89.86:5000/builder/info"

def test_invalid_email_login(driver):
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.ID, "email").send_keys("invalid@example.com")
    driver.find_element(By.ID, "password").send_keys("12345678")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Invalid credentials" in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_invalid_password_login(driver):
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.ID, "email").send_keys("abdulwahabsarwar91@gmail.com")
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Invalid credentials" in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_empty_fields_login(driver):
    driver.get("http://51.20.89.86:5000/login")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "An unexpected error occurred" in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_duplicate_email_signup(driver):
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "name").send_keys("Duplicate User")
    driver.find_element(By.ID, "email").send_keys("abdulwahabsarwar91@gmail.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "terms").click()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Signup failed" in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_weak_password_signup(driver):
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "name").send_keys("Weak User")
    driver.find_element(By.ID, "email").send_keys("weak@example.com")
    driver.find_element(By.ID, "password").send_keys("weak")
    driver.find_element(By.ID, "terms").click()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Signup failed" in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_missing_fields_signup(driver):
    driver.get("http://51.20.89.86:5000/signup")
    driver.find_element(By.ID, "email").send_keys("missing@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "terms").click()
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-red-500")))
    assert "Please agree to the Terms of Service" not in driver.find_element(By.CLASS_NAME, "text-red-500").text

def test_login_page_loads(driver):
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-2xl")))
    assert "Log in" in driver.find_element(By.CLASS_NAME, "text-2xl").text

def test_signup_page_loads(driver):
    driver.get("http://51.20.89.86:5000/signup")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "text-2xl")))
    assert "Create an account" in driver.find_element(By.CLASS_NAME, "text-2xl").text

def test_login_submit_button_exists(driver):
    driver.get("http://51.20.89.86:5000/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert button.text == "Log in"