"""
redrootfuzz.cli

Final CLI for redrootfuzz.

Features:
- choose packaged wordlists automatically
- list packaged wordlists (--list-wordlists)
- choose packaged wordlist by filename (--wordlist-name)
- still supports custom -w / --wordlist path
- optional HTTP check, custom resolvers, threads, permutations toggle
- safe default version string (adjust as you bump package version)

Place this file as: redrootfuzz/cli.py
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional
import time
import os

# Local imports
from .fuzzer import Fuzzer, load_wordlist

# Rich for animations and panels
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.live import Live
from rich.align import Align

console = Console()

# Package version (keep in sync with __init__.py)
VERSION = "0.1.0"

# Directory where packaged wordlists live
WORDLIST_DIR = Path(__file__).parent.parent / "wordlists"


def animate_typing_banner(text, color="cyan", delay=0.05):
    """Prints text with a typing animation effect, updating in-place on a single line.

    Uses rich.live.Live to update the same console line rather than printing many lines.
    The text is center-aligned for a neat banner effect. At the end we print a newline so
    subsequent console output appears below the banner.
    """
    styled_text = Text("", style=color)
    # Use Live for in-place updates. refresh_per_second controls UI smoothness.
    with Live(Align(styled_text, align="center"), console=console, refresh_per_second=30):
        for char in text:
            styled_text.append(char)
            # update the live display (Live context manager handles rendering)
            time.sleep(delay)
    # Ensure a final newline so later prints start on the next line
    console.print()


def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def available_wordlists() -> List[str]:
    """Return sorted list of .txt files present in the package wordlists dir."""
    if not WORDLIST_DIR.exists():
        return []
    return sorted([p.name for p in WORDLIST_DIR.iterdir() if p.is_file() and p.suffix == ".txt"])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="redrootfuzz", description="RedRoot subdomain fuzzer")
    p.add_argument("-d", "--domain", required=True, help="target domain (e.g. example.com)")
    p.add_argument("-w", "--wordlist", help="path to wordlist file (absolute or relative)")
    p.add_argument("--wordlist-name", dest="wordlist_name",
                   help="choose packaged wordlist by filename from wordlists/ (e.g. redroot-tiny-wordlists.txt)")
    p.add_argument("--list-wordlists", action="store_true", help="show packaged wordlists and exit")
    p.add_argument("-t", "--threads", type=int, default=30, help="concurrent worker threads")
    p.add_argument("--no-perm", action="store_true", help="don't generate permutations")
    p.add_argument("--resolver", nargs="+", help="custom DNS resolver(s) IPs, e.g. 8.8.8.8 1.1.1.1")
    p.add_argument("-o", "--output", help="file to write discovered subdomains")
    p.add_argument("--http-check", action="store_true", help="verify HTTP(S) responsiveness (optional dependency)")
    p.add_argument("--version", action="version", version=f"redrootfuzz {VERSION}")
    return p


def _select_wordlist(args: argparse.Namespace) -> Optional[List[str]]:
    """
    Choose wordlist content based on priority:
      1) explicit -w / --wordlist path
      2) --wordlist-name selects a packaged file by name
      3) fallback to first available packaged file
    Returns list of words or None on error (caller should handle messaging).
    """
    # 1) explicit path
    if getattr(args, "wordlist", None):
        wl_path = Path(args.wordlist)
        if not wl_path.exists():
            print(f"[!] Wordlist not found: {wl_path}")
            return None
        return load_wordlist(str(wl_path))

    # 2) packaged filename
    if getattr(args, "wordlist_name", None):
        packaged = WORDLIST_DIR / args.wordlist_name
        if not packaged.exists():
            print(f"[!] Packaged wordlist not found: {args.wordlist_name}")
            names = available_wordlists()
            if names:
                print("Available packaged wordlists:")
                for n in names:
                    print("  -", n)
            else:
                print("No packaged wordlists found in package wordlists/ directory.")
            return None
        return load_wordlist(str(packaged))

    # 3) fallback to first packaged file
    names = available_wordlists()
    if not names:
        print("[!] No packaged wordlists found. Provide -w / --wordlist or add files to wordlists/")
        return None
    default_packaged = WORDLIST_DIR / names[0]
    return load_wordlist(str(default_packaged))


def main(argv: Optional[List[str]] = None) -> int:
    # Clear screen and show animated banner
    clear_screen()
    animate_typing_banner("RedRoot Fuzz Module", color="cyan")
    console.rule("[bold red] Welcome Mr. Agampreet - RedRoot Fuzzer [/]", style="bold red")

    parser = build_parser()
    args = parser.parse_args(argv)

    # list packaged wordlists and exit
    if getattr(args, "list_wordlists", False):
        names = available_wordlists()
        if not names:
            print("No packaged wordlists found.")
        else:
            print("Packaged wordlists:")
            for n in names:
                print("  -", n)
        return 0

    # select wordlist
    words = _select_wordlist(args)
    if words is None:
        return 2

    # create fuzzer
    f = Fuzzer(domain=args.domain,
               words=words,
               threads=args.threads,
               resolver_names=args.resolver,
               http=args.http_check)

    found = f.run(permutations=not args.no_perm)

    # output results
    if args.output:
        out_path = Path(args.output)
        try:
            with out_path.open("w", encoding="utf-8") as out:
                for fqdn, ips, status in found:
                    line = f"{fqdn},{';'.join(ips)}" + (f",HTTP:{status}" if status is not None else "")
                    out.write(line + "\n")
            print(f"[+] Results written to {out_path}")
        except Exception as e:
            print(f"[!] Failed to write output file: {e}")
            return 3
    else:
        for fqdn, ips, status in found:
            print(f"{fqdn} -> {', '.join(ips)}" + (f" | HTTP:{status}" if status is not None else ""))

    print(f"[+] Completed. {len(found)} hosts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
