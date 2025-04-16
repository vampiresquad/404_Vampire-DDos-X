# proxy_checker.py

import requests
from concurrent.futures import ThreadPoolExecutor

def load_proxies():
    try:
        with open("proxies/proxy.txt", "r") as file:
            proxies = [p.strip() for p in file.readlines() if p.strip()]
        print(f"[Proxy Checker] Loaded {len(proxies)} proxies")

        def check(proxy):
            try:
                response = requests.get(
                    "http://ip-api.com/json",
                    proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                    timeout=3
                )
                if response.status_code == 200:
                    with open("proxies/working_proxies.txt", "a") as wf:
                        wf.write(proxy + "\n")
                    print(f"[Proxy Checker] Working: {proxy}")
            except:
                pass

        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(check, proxies)

    except FileNotFoundError:
        print("[Proxy Checker] proxy.txt not found.")
