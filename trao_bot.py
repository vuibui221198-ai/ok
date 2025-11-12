import requests
import time
import random
from colorama import Fore, init
init(autoreset=True)

# Import config
from config import TRAO_USERNAME, TRAO_PASSWORD, YT_CHANNEL, NUM_TASKS

def log_green(text): print(Fore.GREEN + "[+] " + text)
def log_red(text): print(Fore.RED + "[-] " + text)
def log_yellow(text): print(Fore.YELLOW + "[*] " + text)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://traodoisub.com/',
    'Origin': 'https://traodoisub.com'
})

def login():
    log_yellow("Đang login Traodoisub...")
    data = {
        'username': TRAO_USERNAME,
        'password': TRAO_PASSWORD,
        'token': ''  # Nếu có CSRF, lấy từ GET /login
    }
    resp = session.post('https://traodoisub.com/scr/login.php', data=data)
    if resp.status_code == 200 and 'dashboard' in resp.url:  # Hoặc check 'success' in resp.text
        log_green("Login OK!")
        return True
    log_red("Login fail! Kiểm tra acc hoặc token.")
    print("Response:", resp.text[:200])  # Debug
    return False

def get_jobs(job_type="youtube_sub"):
    log_yellow(f"Lấy {NUM_TASKS} jobs {job_type}...")
    resp = session.get(f'https://traodoisub.com/ex/{job_type}/get.php')
    if resp.status_code == 200:
        try:
            jobs = resp.json().get('data', [])
            log_green(f"Tìm {len(jobs)} jobs.")
            return jobs[:NUM_TASKS]
        except:
            log_red("JSON parse fail. Response:", resp.text[:200])
    return []

def do_task(job):
    # Sub YT thật (dùng requests hoặc Selenium mini - đơn giản: delay giả sub)
    job_url = job.get('link')  # Từ job data
    log_yellow(f"Sub: {job_url}")
    time.sleep(random.uniform(5, 10))  # Giả xem YT
    # Nếu cần sub thật: Thêm Selenium code nhỏ ở đây (import... driver.get(job_url); sub_btn.click())

def claim_coin(job_id, job_type="youtube_sub"):
    data = {
        'id': job_id,
        'jazoest': '22098'  # Token mẫu từ 2025 gist, update nếu khác
    }
    resp = session.post(f'https://traodoisub.com/ex/{job_type}/nhantien.php', data=data)
    if '"2"' in resp.text or resp.status_code == 200:  # Success code
        log_green(f"Claim job {job_id} OK (+{job.get('xu', 1)} xu)!")
        return True
    log_red(f"Claim fail: {resp.text[:100]}")
    return False

def farm_tasks(job_type="youtube_sub"):
    if not login():
        return
    jobs = get_jobs(job_type)
    if not jobs:
        log_red("Không có jobs! Thử lại sau.")
        return
    completed = 0
    for job in jobs:
        job_id = job.get('id')
        do_task(job)
        if claim_coin(job_id, job_type):
            completed += 1
        time.sleep(random.uniform(10, 20))  # Anti-spam
    log_green(f"Farm done: {completed}/{NUM_TASKS} tasks.")

def exchange_sub(amount=5):
    log_yellow("Exchange sub YT...")
    data = {
        'url': YT_CHANNEL,
        'soluong': amount,
        'type': 'youtube_sub'
    }
    resp = session.post('https://traodoisub.com/ex/youtube_sub/mua.php', data=data)
    if 'thanh cong' in resp.text.lower() or resp.status_code == 200:
        log_green(f"Exchange {amount} sub OK!")
    else:
        log_red("Exchange fail. Check xu balance.")

if __name__ == "__main__":
    farm_tasks("youtube_sub")
    time.sleep(5)  # Delay trước exchange
    exchange_sub(5)