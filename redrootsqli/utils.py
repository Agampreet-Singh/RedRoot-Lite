# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

import time
from rich.console import Console
from rich.text import Text

console = Console()


def typewriter_print(line: str, delay=0.003):
    """
    Prints text with typing animation and color based on log type
    """

    styled = Text()
    lower = line.lower()

    # 🎨 Color logic
    if "[info]" in lower:
        style = "cyan"
    elif "[warning]" in lower:
        style = "yellow"
    elif "[error]" in lower:
        style = "bold red"
    elif "[!!!]" in lower:
        style = "bold red"
    else:
        style = "white"

    for char in line:
        styled.append(char, style=style)
        console.print(styled, end="\r", soft_wrap=True)
        time.sleep(delay)

    console.print(styled)  # final line


def fast_print(line: str):
    """
    Instant colored print (for important messages)
    """
    lower = line.lower()

    if "vulnerable" in lower:
        console.print(line, style="bold red")
    elif "safe" in lower:
        console.print(line, style="bold green")
    else:
        console.print(line)
