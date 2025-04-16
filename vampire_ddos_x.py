#!/usr/bin/env python3
import os
import sys
import time
import hashlib
import traceback

# === Dynamic Import Fix and Proxy Handling ===

def fix_imports():
    try:
        import colorama
        from colorama import Fore, Style
    except ImportError:
        os.system("pip install colorama")
        import colorama
        from colorama import Fore, Style
    colorama.init()
    return Fore, Style

Fore, Style = fix_imports()

# === Directories Setup ===

def auto_create_dirs():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("proxies", exist_ok=True)
    for f in ["logs/.keep", "proxies/proxy.txt", "proxies/working_proxies.txt"]:
        open(f, 'a').close()

# === Password Verification ===

def verify_password(input_password):
    return hashlib.sha256(input_password.encode()).hexdigest() == PASSWORD_HASH

# === Auto Fix Missing Modules ===

def try_import(module, pip_name=None):
    try:
        return __import__(module)
    except ImportError:
        os.system(f"pip install {pip_name or module}")
        return __import__(module)

# === Load Attack Modules (Auto Recovery) ===

def try_load_attacks():
    try:
        global tcp, udp, slowloris
        import attacks.tcp as tcp
        import attacks.udp as udp
        import attacks.slowloris as slowloris
    except Exception:
        os.makedirs("attacks", exist_ok=True)
        with open("attacks/tcp.py", "w") as f:
            f.write("""def attack(ip, port, threads):\n    print(f'TCP Flood to {ip}:{port} with {threads} threads')\n""")
        with open("attacks/udp.py", "w") as f:
            f.write("""def attack(ip, port, threads):\n    print(f'UDP Flood to {ip}:{port} with {threads} threads')\n""")
        with open("attacks/slowloris.py", "w") as f:
            f.write("""def attack(domain, threads):\n    print(f'Slowloris Attack to {domain} with {threads} threads')\n""")
        try_load_attacks()

# === Load Proxy Checker ===

def try_load_proxy_checker():
    try:
        global load_proxies
        from proxy_checker import load_proxies
    except Exception:
        with open("proxy_checker.py", "w") as f:
            f.write("""def load_proxies():\n    print('Loading proxies... [Dummy Function]')\n""")
        try_load_proxy_checker()

# === Banners ===

def banner_admin():
    print(Fore.RED + Style.BRIGHT + """
 ██╗░░░██╗░█████╗░███╗░░░███╗██████╗░███████╗██╗███╗░░██╗
 ██║░░░██║██╔══██╗████╗░████║██╔══██╗██╔════╝██║████╗░██║
 ╚██╗░██╔╝███████║██╔████╔██║██║░░██║█████╗░░██║██╔██╗██║
 ░╚████╔╝░██╔══██║██║╚██╔╝██║██║░░██║██╔══╝░░██║██║╚████║
 ░░╚██╔╝░░██║░░██║██║░╚═╝░██║██████╔╝███████╗██║██║░╚███║
 ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═════╝░╚══════╝╚═╝╚═╝░░╚══╝
 [ Vampire-X Admin Panel ]
 """ + Style.RESET_ALL)

def banner_user():
    print(Fore.CYAN + Style.BRIGHT + """
╔═════════════════════════════════════╗
║         Vampire-X User Panel       ║
╚═════════════════════════════════════╝
""" + Style.RESET_ALL)

# === Menus ===

def admin_menu():
    print("[1] TCP Flood")
    print("[2] UDP Flood")
    print("[3] Slowloris")
    print("[4] Check Proxies")
    print("[0] Exit")

def user_menu():
    print("[1] TCP Flood")
    print("[2] UDP Flood")
    print("[0] Exit")

# === Live Attack Logging ===

def log_attack(atype, target, port, threads):
    with open("logs/attack.log", "a") as f:
        f.write(f"{time.ctime()} | {atype} | {target}:{port} | Threads: {threads}\n")

# === Handle Choices ===

def handle_choice(choice, mode="user"):
    try:
        if choice == "1":
            target = input("Target IP/Domain: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            log_attack("TCP", target, port, threads)
            tcp.attack(target, port, threads)

        elif choice == "2":
            target = input("Target IP/Domain: ")
            port = int(input("Port: "))
            threads = int(input("Threads: "))
            log_attack("UDP", target, port, threads)
            udp.attack(target, port, threads)

        elif choice == "3" and mode == "admin":
            target = input("Target Domain: ")
            threads = int(input("Threads: "))
            log_attack("Slowloris", target, 80, threads)
            slowloris.attack(target, threads)

        elif choice == "4" and mode == "admin":
            load_proxies()

        elif choice == "0":
            print("Exiting...")
            sys.exit()

        else:
            print(Fore.YELLOW + "Invalid Option!" + Style.RESET_ALL)

    except Exception as e:
        with open("logs/errors.log", "a") as f:
            f.write(f"{time.ctime()} | Error: {str(e)}\n{traceback.format_exc()}\n")
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)

# === Main Execution ===

PASSWORD_HASH = hashlib.sha256("SH404".encode()).hexdigest()

def main():
    try:
        auto_create_dirs()
        try_load_attacks()
        try_load_proxy_checker()

        print("[1] Admin Access")
        print("[2] User Access")
        level = input("Select Mode: ")
        mode = "user"

        if level == "1":
            pwd = input("Enter Admin Password: ")
            if verify_password(pwd):
                mode = "admin"
            else:
                print(Fore.RED + "Wrong Password! Switching to User Mode..." + Style.RESET_ALL)

        os.system('cls' if os.name == 'nt' else 'clear')
        banner_admin() if mode == "admin" else banner_user()

        while True:
            admin_menu() if mode == "admin" else user_menu()
            choice = input("Select Option: ")
            handle_choice(choice, mode)
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            banner_admin() if mode == "admin" else banner_user()

    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrupted. Exiting..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
