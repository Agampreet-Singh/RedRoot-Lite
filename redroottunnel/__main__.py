import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()

def typing_effect(text, delay=0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def locked_module_screen():
    console.clear()

    title = Text("🔒 MODULE LOCKED", style="bold red")
    owner = Text("Owner: Mr. Agampreet Singh", style="bold cyan")
    info = Text(
        "\nThis module is currently restricted.\n"
        "Access requires explicit authorization from the owner.\n\n"
        "Please contact the owner to request permission.",
        style="white"
    )

    panel_content = Align.center(
        Text.assemble(title, "\n\n", owner, "\n", info),
        vertical="middle"
    )

    console.print(
        Panel(
            panel_content,
            border_style="red",
            padding=(1, 4),
            width=70
        )
    )

    time.sleep(0.5)
    typing_effect("\n[!] Security Notice: Unauthorized access is prohibited.", 0.03)
    typing_effect("[!] Logging attempt... Done.", 0.03)

if __name__ == "__main__":
    locked_module_screen()
