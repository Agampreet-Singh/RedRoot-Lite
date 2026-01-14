import os, time
from rich.console import Console
from rich.text import Text

console = Console()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def animate_typing_banner():
    clear()
    msg = "Welcome Mr. Agampreet"
    colors = ["red", "gold1"]
    text = Text()
    for i, char in enumerate(msg):
        text.append(char, style=f"bold {colors[i % 2]}")
        console.print(text, end="\r")
        time.sleep(0.02)
    console.print()
    time.sleep(0.2)
