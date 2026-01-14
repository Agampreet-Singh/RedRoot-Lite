import os
import sys
import glob
import signal
from rich.console import Console

console = Console()
found_paths = []

def signal_handler(sig, frame):
    console.print("\n[yellow]⛔ Scan interrupted by user. Exiting...[/yellow]")
    if found_paths:
        console.print("\n[bold green]✔ Directories found before exit:[/bold green]")
        for path in found_paths:
            console.print(f"[green]{path}[/green]")
    sys.exit(0)

def load_wordlist(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip().split('#', 1)[0].strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        console.print(f"[red]❌ Wordlist not found: {path}[/red]")
        sys.exit(1)

def find_wordlists(directories=["/usr/share/wordlists", "/opt", "/usr/share/dirb", "/usr/share/seclists"]):
    found = []
    for dir in directories:
        for ext in ("*.txt", "*.lst"):
            found.extend(glob.glob(f"{dir}/**/{ext}", recursive=True))
    return sorted(set(found))

def choose_wordlist():
    console.print("[bold cyan]📂 Scanning for available wordlists...[/bold cyan]")
    wordlists = find_wordlists()

    if not wordlists:
        console.print("[red]❌ No wordlists found automatically.[/red]")
        sys.exit(1)

    for idx, path in enumerate(wordlists, 1):
        console.print(f"[{idx}] {path}")

    console.print("\n[bold yellow]Select a wordlist:[/bold yellow]")
    console.print("[green]→ Enter number to select from list[/green]")
    console.print("[green]→ Enter 'm' to input a custom path manually[/green]")

    choice = console.input("[bold magenta]> Your choice: [/bold magenta] ").strip()

    if choice.lower() == 'm':
        custom_path = console.input("[bold cyan]Enter full path: [/bold cyan]").strip()
        if os.path.isfile(custom_path):
            return custom_path
        console.print("[red]❌ Invalid file path.[/red]")
        sys.exit(1)
    elif choice.isdigit() and 0 < int(choice) <= len(wordlists):
        return wordlists[int(choice) - 1]
    else:
        console.print("[red]❌ Invalid input.[/red]")
        sys.exit(1)
