import os, time
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_typing_banner():
    clear()
    message = "Welcome Mr. Agampreet"
    colors = ["red", "gold1"]
    
    styled_text = Text()
    for i, char in enumerate(message):
        color = colors[i % 2]
        styled_text.append(char, style=f"bold {color}")
        console.print(styled_text, end="\r", soft_wrap=True)
        time.sleep(0.02)
    console.print()  
    time.sleep(0.2)


def display_scan_report(report):
    clear()
    console.rule("[bold red]RedRoot - Portscanner Report[/bold red]")
    console.print(f"[bold yellow]Target IP:[/bold yellow] {report['ip']}")
    console.print(f"[bold yellow]Hostname:[/bold yellow] {report['hostname']}")

    if "os" in report:
        os_info = report["os"]
        console.print(
            f"[bold yellow]Detected OS:[/bold yellow] {os_info['os']} "
            f"(Method: {os_info['method']}, TTL: {os_info['ttl']})\n"
        )

    table = Table(title="Open Ports", header_style="bold magenta")
    table.add_column("Port", justify="center")
    table.add_column("Protocol", justify="center")
    table.add_column("State", justify="center")
    table.add_column("Service", justify="center")
    table.add_column("Version", justify="left")

    if not report["ports"]:
        console.print("[bold red]No open ports found.[/bold red]")
        return

    for p in report["ports"]:
        version = p['version'] if p['version'] else "-"
        table.add_row(p['port'], p['protocol'], p['state'], p['service'], version)
    console.print(table)
    console.rule("[bold green]Scan Complete[/bold green]")
