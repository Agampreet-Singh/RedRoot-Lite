import time
from rich.console import Console
from rich.text import Text

console = Console()


def print_banner():
    banner = """
    """
    console.print(Text(banner, style="bold cyan"))
    console.print(Text("Welcome Mr. Agampreet\n", style="bold green"))
    time.sleep(0.5)


def color_text(msg, color):
    return f"[{color}]{msg}[/{color}]"
