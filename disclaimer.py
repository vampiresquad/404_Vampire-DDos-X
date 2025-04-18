import os
import time
import random
from colorama import Fore, Style, init
init(autoreset=True)

def terminal_shake():
    for _ in range(10):
        os.system("clear")
        print(" " * random.randint(1, 10), end="")
        print(Fore.RED + Style.BRIGHT + "!! WARNING !!")
        time.sleep(0.05)

def play_warning_sound():
    try:
        os.system("termux-media-player play warning.mp3")  # Ensure 'warning.mp3' is present
    except:
        pass  # Silent fail if media not available

def blood_drip_effect():
    blood = Fore.RED + Style.BRIGHT + "☠ BLOOD DRIPPING... ☠"
    for _ in range(3):
        print("\n" * random.randint(1, 3) + " " * random.randint(1, 5) + blood)
        time.sleep(0.2)

def show_disclaimer():
    terminal_shake()
    play_warning_sound()
    blood_drip_effect()

    disclaimer = f"""
{Fore.RED}{Style.BRIGHT}
⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀     {Fore.LIGHTRED_EX}██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗███████╗
⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀     ██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔════╝
⠀⠀⠀⠀⣿⣿⡟⠛⠛⠛⠛⠛⠻⣿⣿⡇⠀⠀⠀⠀     ██║   ██║███████║██╔████╔██║██████╔╝██║███████╗
⠀⠀⠀⠀⠹⣿⣷⣶⣶⣶⣶⣾⣿⡿⠏⠀⠀⠀⠀     ██║   ██║██╔══██║██║╚██╔╝██║██╔═══╝ ██║╚════██║
⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠛⠉⠀⠀⠀⠀⠀     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║     ██║███████║
                                                       ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝
{Fore.LIGHTYELLOW_EX}
╔════════════════════════════════════════════════════════════════╗
║                   {Fore.RED}!!! WARNING !!!                    {Fore.LIGHTYELLOW_EX}               ║
╠════════════════════════════════════════════════════════════════╣
║ {Fore.LIGHTWHITE_EX}This tool is a digital weapon and can cause harm if misused!   {Fore.LIGHTYELLOW_EX}║
║ {Fore.RED}Only ethical hackers, security researchers, or authorized users {Fore.LIGHTYELLOW_EX}║
║ {Fore.RED}are allowed to use this tool. Unauthorized usage is ILLEGAL.   {Fore.LIGHTYELLOW_EX}║
╠════════════════════════════════════════════════════════════════╣
║ {Fore.CYAN}Author : {Fore.LIGHTWHITE_EX}Muhammad Shourov a.k.a. VAMPIRE                      {Fore.LIGHTYELLOW_EX}║
║ {Fore.CYAN}Team   : {Fore.LIGHTWHITE_EX}Vampire Squad (Ethical Hackers Organization)        {Fore.LIGHTYELLOW_EX}║
║ {Fore.CYAN}GitHub : {Fore.LIGHTWHITE_EX}https://github.com/vampiresquad                      {Fore.LIGHTYELLOW_EX}║
╠════════════════════════════════════════════════════════════════╣
║ {Fore.LIGHTRED_EX}We (Vampire Squad) are not responsible for any misuse or damage.║
║ Use this tool only with full responsibility and legal access!   {Fore.LIGHTYELLOW_EX}║
╚════════════════════════════════════════════════════════════════╝

{Style.RESET_ALL}
"""
    print(disclaimer)
