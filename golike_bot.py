from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from colorama import Fore, init
init(autoreset=True)

# Import config
from config import GOLIKE_EMAIL, GOLIKE_PASS, YT_CHANNEL, NUM_TASKS

def log_green(text): print(Fore.GREEN + "[+] " + text)
def log_red(text): print(Fore.RED + "[-] " + text)
def log_yellow(text): print(Fore.YELLOW + "[*] " + text)

options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
# options.add_argument("--headless")  # Uncomment ẩn browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

def login_golike():
    log_yellow("Đang login GoLike...")
    driver.get("https://app.golike.net/login")
    time.sleep(3)
    try:
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))  # Hoặc ID="email"
        email_field.send_keys(GOLIKE_EMAIL)
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(GOLIKE_PASS)
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], .login-btn")
        submit_btn.click()
        time.sleep(5)
        if "/home" in driver.current_url:
            log_green("Login OK!")
            return True
        log_red("Login fail! Check captcha/email.")
    except Exception as e:
        log_red(f"Login error: {e}")
    return False

def farm_yt_subs():
    log_yellow("Farm earn YT subs...")
    driver.get("https://app.golike.net/earn/youtube-subscribers")
    time.sleep(3)
    for i in range(NUM_TASKS):
        try:
            task_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".task-list, .earn-tasks")))  # Container tasks
            task_btn = driver.find_element(By.CSS_SELECTOR, ".start-task, .task-item:first-child .btn")  # Task đầu
            task_btn.click()
            time.sleep(2)
            
            yt_url_elem = driver.find_element(By.CSS_SELECTOR, ".task-url, iframe[src*='youtube']")
            yt_url = yt_url_elem.get_attribute("src") or yt_url_elem.get_attribute("href")
            
            driver.execute_script(f"window.open('{yt_url}', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.uniform(5, 10))
            
            sub_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='Subscribe'], #subscribe-button")))
            sub_btn.click()
            time.sleep(2)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            claim_btn = driver.find_element(By.CSS_SELECTOR, ".claim-points, .complete-task")
            claim_btn.click()
            log_green(f"Task {i+1} OK!")
            
        except Exception as e:
            log_red(f"Task {i+1} error: {e}")
        
        time.sleep(random.uniform(15, 25))

def buy_yt_subs(amount=5):
    log_yellow("Buy YT subs...")
    driver.get("https://app.golike.net/buy/youtube-subscribers")
    time.sleep(3)
    
    url_input = wait.until(EC.presence_of_element_located((By.NAME, "url")))
    url_input.clear()
    url_input.send_keys(YT_CHANNEL)
    
    qty_input = driver.find_element(By.NAME, "quantity")
    qty_input.clear()
    qty_input.send_keys(str(amount))
    
    buy_btn = driver.find_element(By.CSS_SELECTOR, ".buy-btn, button[type='submit']")
    buy_btn.click()
    time.sleep(3)
    log_green(f"Buy {amount} subs submitted! Check balance.")

try:
    if login_golike():
        farm_yt_subs()
        time.sleep(5)
        buy_yt_subs(5)
finally:
    time.sleep(5)
    driver.quit()