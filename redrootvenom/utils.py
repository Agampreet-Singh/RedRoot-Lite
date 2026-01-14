from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def redroot_banner():
    console.print(
        Panel.fit(
            "[bold red]💉 REDROOT VENOM[/bold red]\n"
            "[cyan]Payload Generator • MSFvenom-style[/cyan]"
        )
    )

def show_payload_options():
    table = Table(title="Available Payloads", box=None)
    table.add_column("Payload", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("windows/exec", "Windows reverse TCP executable")
    table.add_row("windows/powershell", "Windows PowerShell reverse TCP")
    table.add_row("linux/elf", "Linux ELF reverse shell")
    table.add_row("linux/bash", "Bash reverse shell")
    table.add_row("linux/busybox", "BusyBox reverse shell")
    table.add_row("python", "Python reverse shell")
    table.add_row("perl", "Perl reverse shell")
    table.add_row("php", "PHP reverse shell")
    table.add_row("ruby", "Ruby reverse shell")
    table.add_row("android", "Android Meterpreter payload")
    table.add_row(
        "xsl/xslt-webshell",
        "XSLT EXSLT file-write web shell"
    )

    console.print(table)
