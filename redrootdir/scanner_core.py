import argparse
import requests
from urllib.parse import urljoin
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from .banner import animate_typing_banner
from .utils import load_wordlist, choose_wordlist, signal_handler, found_paths
import signal

console = Console()
signal.signal(signal.SIGINT, signal_handler)


def normalize_url(url):
    return url if url.endswith("/") else url + "/"


def is_directory(path):
    return path.endswith("/")


def scan_directories(base_url, wordlist, extensions, codes, scanned):
    discovered_dirs = []
    total = len(wordlist) * len(extensions)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task(f"[cyan]Scanning {base_url}[/cyan]", total=total)

        for word in wordlist:
            for ext in extensions:
                path = urljoin(base_url, f"{word}{ext}")
                try:
                    r = requests.get(path, timeout=5, allow_redirects=False)
                    if r.status_code in codes:
                        console.print(
                            f"[green][+] Found:[/green] {path} (Status: {r.status_code})"
                        )
                        found_paths.append(path)

                        if is_directory(path):
                            normalized = normalize_url(path)
                            if normalized not in scanned:
                                discovered_dirs.append(normalized)

                except requests.RequestException:
                    pass

                progress.update(task, advance=1)

    return discovered_dirs


def main():
    animate_typing_banner()

    parser = argparse.ArgumentParser(
        description="🔍 RedRoot Recursive Directory Brute Forcing Tool"
    )
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
    parser.add_argument(
        "-e", "--extensions",
        nargs="*",
        default=["/", ".php", ".html", ".bak", ".txt"],
        help="List of extensions"
    )
    parser.add_argument(
        "-c", "--codes",
        nargs="*",
        type=int,
        default=[200, 301, 302, 403],
        help="Valid status codes"
    )

    args = parser.parse_args()

    base_url = normalize_url(args.url)
    wordlist_path = args.wordlist if args.wordlist else choose_wordlist()
    words = load_wordlist(wordlist_path)

    console.print(f"[bold cyan]🌐 Target:[/bold cyan] {base_url}")
    console.print(f"[bold cyan]📖 Wordlist:[/bold cyan] {wordlist_path}")
    console.print(f"[bold cyan]🧩 Extensions:[/bold cyan] {', '.join(args.extensions)}")
    console.print(f"[bold cyan]🔁 Recursive:[/bold cyan] Enabled\n")

    queue = [base_url]
    scanned = set()

    while queue:
        current = queue.pop(0)

        if current in scanned:
            continue

        scanned.add(current)
        console.print(f"\n[bold yellow]▶ Scanning:[/bold yellow] {current}")

        new_dirs = scan_directories(
            current,
            words,
            args.extensions,
            args.codes,
            scanned
        )

        queue.extend(new_dirs)

    console.print(
        f"\n[bold green]✔ Scan complete. Total paths found: {len(found_paths)}[/bold green]"
    )

