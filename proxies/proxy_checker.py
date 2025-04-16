import requests
import threading
import os
import time

PROXY_FILE = 'proxies/proxy.txt'
WORKING_FILE = 'proxies/working_proxies.txt'
TIMEOUT = 5  # seconds
THREAD_COUNT = 100

working_proxies = []
lock = threading.Lock()

def check_proxy(proxy):
    try:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            with lock:
                working_proxies.append(proxy)
                print(f'\033[92m[+] Working: {proxy}\033[0m')
    except:
        print(f'\033[91m[-] Dead: {proxy}\033[0m')

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        print(f'\033[91m[!] Proxy file not found: {PROXY_FILE}\033[0m')
        return []
    with open(PROXY_FILE, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def save_working_proxies():
    with open(WORKING_FILE, 'w') as file:
        for proxy in working_proxies:
            file.write(proxy + '\n')
    print(f'\n\033[94m[✓] Saved {len(working_proxies)} working proxies to {WORKING_FILE}\033[0m')

def start_checking():
    proxies = load_proxies()
    if not proxies:
        return
    print(f'\n\033[96m[*] Checking {len(proxies)} proxies...\033[0m\n')
    threads = []

    for proxy in proxies:
        while threading.active_count() >= THREAD_COUNT:
            time.sleep(0.1)
        t = threading.Thread(target=check_proxy, args=(proxy,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    save_working_proxies()

if __name__ == '__main__':
    start_checking()
