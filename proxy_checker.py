import threading
import requests
import socks
import socket
from colorama import Fore
from concurrent.futures import ThreadPoolExecutor

working_proxies = []

def check_proxy(proxy, timeout=5):
    ip, port = proxy.split(":")
    try:
        socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, ip, int(port))
        socket.socket = socks.socksocket
        r = requests.get("http://httpbin.org/ip", timeout=timeout)
        if r.status_code == 200:
            working_proxies.append(proxy)
            print(Fore.GREEN + f"[+] WORKING: {proxy}")
    except:
        print(Fore.RED + f"[-] DEAD: {proxy}")

def load_proxies(proxy_file):
    with open(proxy_file, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    return proxies

def start_checking(proxy_file, threads=30):
    proxies = load_proxies(proxy_file)
    print(Fore.CYAN + f"[*] Checking {len(proxies)} proxies using {threads} threads...")
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for proxy in proxies:
            executor.submit(check_proxy, proxy)

    print(Fore.YELLOW + f"\n[!] Working proxies saved in working_proxies.txt")
    with open("working_proxies.txt", "w") as out:
        for proxy in working_proxies:
            out.write(proxy + "\n")
