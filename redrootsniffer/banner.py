from rich.console import Console
from rich.text import Text
import time, os

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
        time.sleep(0.03)
    console.print()
    time.sleep(0.2)
