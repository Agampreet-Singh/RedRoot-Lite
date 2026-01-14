#!/usr/bin/env python3
# RedRoot Password Cracker - Script 1
# By Agampreet Singh
import argparse
import hashlib
import os
import pickle
import re
import subprocess
import time
import zipfile
from itertools import product
from rich.console import Console
from rich.text import Text
from rich.progress import Progress

console = Console()

# --- UI / Banner ---
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def animate_typing_banner():
    clear()
    message = "Welcome Mr. Agampreet"
    colors = ["red", "gold1"]
    styled_text = Text()
    for i, char in enumerate(message):
        color = colors[i % len(colors)]
        styled_text.append(char, style=f"bold {color}")
        console.print(styled_text, end="\r", soft_wrap=True)
        time.sleep(0.02)
    console.print("\n")
    time.sleep(0.2)

# --- Constants ---
SUPPORTED_HASHES = ["md5", "sha1", "sha256", "sha512", "ntlm", "bcrypt"]
MASK_MAP = {
    "?l": "abcdefghijklmnopqrstuvwxyz",
    "?u": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "?d": "0123456789",
    "?s": "!@#$%^&*()"
}

# ------------------ Hash Utilities ------------------
def detect_hash_type(h):
    h = h.strip()
    if h.startswith(("$2a$", "$2b$", "$2y$")):
        return "bcrypt"
    return {
        32: "md5",
        40: "sha1",
        64: "sha256",
        128: "sha512"
    }.get(len(h), "ntlm")

def compute_hash(algo, word):
    if algo == "ntlm":
        return hashlib.new("md4", word.encode("utf-16le")).hexdigest()
    elif algo == "bcrypt":
        import bcrypt
        return bcrypt.hashpw(word.encode(), bcrypt.gensalt()).decode()
    else:
        h = hashlib.new(algo)
        h.update(word.encode())
        return h.hexdigest()

# ------------------ Session ------------------
def save_session(file, data):
    if not file:
        return
    try:
        with open(file, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        console.print(f"[bold red][!] Failed to save session: {e}[/bold red]")

def load_session(file):
    if not file:
        return {}
    try:
        with open(file, "rb") as f:
            return pickle.load(f)
    except Exception:
        return {}

# ------------------ Benchmark ------------------
def benchmark(algorithm, duration=5):
    console.print(f"[bold yellow][+] Benchmarking {algorithm} for {duration} seconds...[/bold yellow]")
    count = 0
    start = time.time()
    while time.time() - start < duration:
        if algorithm == "bcrypt":
            import bcrypt
            bcrypt.hashpw(b"test", bcrypt.gensalt())
        else:
            compute_hash(algorithm, "test")
        count += 1
    console.print(f"[bold green][+] {count // duration} hashes/second (approx)[/bold green]")

# ------------------ Cracking Techniques ------------------
def dictionary_attack(hashes, wordlist, algo, session, session_file):
    console.print("[cyan][*] Starting dictionary attack...[/cyan]")
    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for word in f:
                word = word.strip()
                if not word:
                    continue
                check_candidate(hashes, algo, word, session, session_file)
    except FileNotFoundError:
        console.print(f"[bold red][!] Wordlist not found: {wordlist}[/bold red]")

def brute_force_attack(hashes, algo, charset, maxlen, session, session_file):
    console.print(f"[cyan][*] Starting brute-force attack (max length: {maxlen})...[/cyan]")
    for l in range(1, maxlen + 1):
        for word_tuple in product(charset, repeat=l):
            guess = "".join(word_tuple)
            check_candidate(hashes, algo, guess, session, session_file)

def mask_attack(hashes, algo, mask, session, session_file):
    console.print(f"[cyan][*] Starting mask attack with pattern: {mask}[/cyan]")
    tokens = re.findall(r"\?.|.", mask)
    charsets = []
    for tok in tokens:
        if tok in MASK_MAP:
            charsets.append(MASK_MAP[tok])
        else:
            charsets.append(tok)
    pool = [""]
    for charset in charsets:
        pool = [p + c for p in pool for c in charset]
    for guess in pool:
        check_candidate(hashes, algo, guess, session, session_file)

def rule_based_attack(hashes, wordlist, algo, session, session_file):
    console.print("[cyan][*] Starting rule-based attack...[/cyan]")
    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            for word in f:
                word = word.strip()
                if not word:
                    continue
                mutations = [word, word.upper(), word.capitalize(), word[::-1]]
                for m in mutations:
                    check_candidate(hashes, algo, m, session, session_file)
    except FileNotFoundError:
        console.print(f"[bold red][!] Wordlist not found: {wordlist}[/bold red]")

def incremental_attack(hashes, algo, session, session_file):
    charset = "etaoinshrdlucmfwypvbgkqjxz0123456789"
    console.print("[cyan][*] Starting incremental attack (length 1–5)...[/cyan]")
    for l in range(1, 6):
        for word_tuple in product(charset, repeat=l):
            guess = "".join(word_tuple)
            check_candidate(hashes, algo, guess, session, session_file)

# ------------------ Candidate Check ------------------
def check_candidate(hashes, algo, guess, session, session_file):
    if algo == "bcrypt":
        import bcrypt
        for h in list(hashes):
            if h not in session:
                try:
                    if bcrypt.checkpw(guess.encode(), h.encode()):
                        console.print(f"[bold green][+] Cracked: {h} -> {guess}[/bold green]")
                        session[h] = guess
                        save_session(session_file, session)
                except Exception:
                    continue
    else:
        hashed = compute_hash(algo, guess)
        if hashed in hashes and hashed not in session:
            console.print(f"[bold green][+] Cracked: {hashed} -> {guess}[/bold green]")
            session[hashed] = guess
            save_session(session_file, session)

# ------------------ ZIP Password Cracker ------------------
def zip_crack(zip_path, wordlist):
    console.print("[cyan][*] Starting ZIP password cracking...[/cyan]")
    if not zipfile.is_zipfile(zip_path):
        console.print("[bold red][!] Invalid ZIP file.[/bold red]")
        return
    try:
        with zipfile.ZipFile(zip_path) as zf:
            with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
                for word in f:
                    password = word.strip().encode("utf-8")
                    try:
                        zf.extractall(pwd=password)
                        console.print(f"[bold green][+] Cracked ZIP Password: {password.decode()}[/bold green]")
                        return
                    except RuntimeError:
                        continue
                    except Exception:
                        continue
    except FileNotFoundError:
        console.print(f"[bold red][!] Wordlist not found: {wordlist}[/bold red]")
    console.print("[bold red][!] Password not found in wordlist.[/bold red]")

# ------------------ Hash Extraction Helpers ------------------
def extract_shadow(passwd_file, shadow_file, out="merged.hashes"):
    try:
        with open(out, "wb") as o:
            subprocess.run(["unshadow", passwd_file, shadow_file], stdout=o)
        console.print(f"[bold green][+] Merged UNIX hashes into {out}[/bold green]")
    except FileNotFoundError:
        console.print("[bold red][!] unshadow not found or files missing[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] extract_shadow error: {e}[/bold red]")

def extract_sam(system, sam, out="sam.hashes"):
    try:
        with open(out, "wb") as o:
            subprocess.run(["samdump2", sam, system], stdout=o)
        console.print(f"[bold green][+] Extracted Windows hashes to {out}[/bold green]")
    except FileNotFoundError:
        console.print("[bold red][!] samdump2 not found or files missing[/bold red]")
    except Exception as e:
        console.print(f"[bold red][!] extract_sam error: {e}[/bold red]")

# ------------------ Runner ------------------
def run_cracker(args):
    if args.show and args.session:
        session = load_session(args.session)
        if not session:
            print("[!] No session file found")
            return
        for h, p in session.items():
            print(f"{h} -> {p}")
        return

    if args.test:
        import timeit
        print("Benchmarking SHA256 with 1M hashes...")
        t = timeit.timeit(lambda: hashlib.sha256(b"password").hexdigest(), number=10**6)
        print(f"Time: {t:.2f} seconds")
        return

    if args.zipfile and args.zip_dict:
        zip_crack(args.zipfile, args.zip_dict)
        return

    if args.extract_shadow:
        passwd, shadow = args.extract_shadow
        extract_shadow(passwd, shadow, args.session or "unshadowed.txt")
        return

    if args.extract_sam:
        system, sam = args.extract_sam
        extract_sam(system, sam, args.session or "samdump.txt")
        return

    if args.hashfile and args.algorithm:
        session = load_session(args.session) if args.session else {}
        hashes = [h.strip() for h in open(args.hashfile, "r") if h.strip()]
        algo = args.algorithm if args.algorithm != "auto" else detect_hash_type(hashes[0])

        if args.dictionary:
            dictionary_attack(hashes, args.dictionary, algo, session, args.session)
        if args.rules and args.dictionary:
            rule_based_attack(hashes, args.dictionary, algo, session, args.session)
        if args.brute:
            brute_force_attack(hashes, algo, args.charset, args.maxlen, session, args.session)
        if args.mask:
            mask_attack(hashes, algo, args.mask, session, args.session)
        if args.incremental:
            incremental_attack(hashes, algo, session, args.session)
        return

    print("[!] No valid mode selected. Use -h for help.")

# ------------------ Main ------------------
def main():
    animate_typing_banner()
    console.rule("[bold red]RedRoot - Password Cracker[/bold red]")

    parser = argparse.ArgumentParser(description="RedRoot Ultimate Password Cracker")
    parser.add_argument("--hashfile", help="File with hashes")
    parser.add_argument("--algorithm", help="Hash type (or auto)")
    parser.add_argument("--dictionary", help="Wordlist file")
    parser.add_argument("--brute", action="store_true")
    parser.add_argument("--mask", help="Mask attack e.g., ?l?l?d?d")
    parser.add_argument("--rules", action="store_true")
    parser.add_argument("--incremental", action="store_true")
    parser.add_argument("--charset", default="abc123", help="Charset for brute-force")
    parser.add_argument("--maxlen", type=int, default=4)
    parser.add_argument("--session", help="Save/load cracked session")
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--extract-shadow", nargs=2, metavar=("passwd","shadow"))
    parser.add_argument("--extract-sam", nargs=2, metavar=("system","sam"))
    parser.add_argument("--zipfile", help="Encrypted ZIP file")
    parser.add_argument("--zip-dict", help="Wordlist for ZIP file")

    args = parser.parse_args()
    run_cracker(args)

if __name__ == "__main__":
    main()
