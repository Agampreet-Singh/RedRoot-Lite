#!/usr/bin/env python3
from rich.console import Console
from rich.prompt import Prompt
from .utils import animate_typing_banner
from .union_sqli import run_union_sqli
from .blind_sqli import run_blind_sqli
from .auth_bypass import run_auth_bypass
import argparse

console = Console()

def main():
    animate_typing_banner()

    parser = argparse.ArgumentParser(description="RedRoot - SQL Injection Tool")
    parser.add_argument("url", help="Base URL like 'http://example.com'")
    args = parser.parse_args()

    if not args.url.startswith("http"):
        console.print("[-] URL must start with http or https", style="bold red")
        return

    console.print("\n[bold yellow]Select the SQL Injection Attack Type:[/bold yellow]")
    console.print("[1] Union-based SQLi")
    console.print("[2] Blind SQLi")
    console.print("[3] Authentication Bypass SQLi")
    choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3"])

    if choice == "1":
        run_union_sqli(args.url)
    elif choice == "2":
        run_blind_sqli(args.url)
    elif choice == "3":
        run_auth_bypass(args.url)

if __name__ == "__main__":
    main()
