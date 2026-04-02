# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

from rich.console import Console

console = Console()


# -------------------------
# Banner
# -------------------------
def print_banner():
    console.print("[bold red]RedRootSQLi[/bold red]")


# -------------------------
# Result Output
# -------------------------
def print_result(result: dict):
    console.print("\n[bold cyan]==============================[/bold cyan]")
    console.print(f"[bold white][TARGET][/bold white] {result.get('target')}")
    console.print("[bold cyan]==============================[/bold cyan]")

    # -------------------------
    # STATUS
    # -------------------------
    if result.get("vulnerable"):
        console.print("[bold red][STATUS] ⚠ VULNERABLE[/bold red]\n")
    else:
        console.print("[bold green][STATUS] ✓ SAFE[/bold green]\n")

    # -------------------------
    # SCAN DETAILS
    # -------------------------
    if result.get("parameter"):
        console.print(f"[yellow][PARAMETER][/yellow] {result['parameter']}")

    if result.get("dbms"):
        console.print(f"[yellow][DBMS][/yellow] {result['dbms']}")

    if result.get("injection_types"):
        console.print("\n[bold magenta][INJECTION TYPES][/bold magenta]")
        for inj in result["injection_types"]:
            console.print(f"  → {inj}")

    if result.get("payloads"):
        console.print("\n[bold green][PAYLOADS][/bold green]")
        for payload in result["payloads"]:
            console.print(f"  → {payload}")

    # -------------------------
    # DATABASES
    # -------------------------
    if result.get("databases"):
        console.print("\n[bold blue][DATABASES][/bold blue]")
        for db in result["databases"]:
            console.print(f"  → {db}")

    # -------------------------
    # TABLES
    # -------------------------
    elif result.get("tables"):
        console.print("\n[bold blue][TABLES][/bold blue]")
        for table in result["tables"]:
            console.print(f"  → {table}")

    # -------------------------
    # COLUMNS
    # -------------------------
    elif result.get("columns"):
        console.print("\n[bold blue][COLUMNS][/bold blue]")
        for col in result["columns"]:
            console.print(f"  → {col}")

    # -------------------------
    # DATA (ROWS)
    # -------------------------
    elif result.get("rows"):
        console.print("\n[bold blue][DATA][/bold blue]")
        for row in result["rows"]:
            console.print("  → " + " | ".join(row))

    # -------------------------
    # NO DATA
    # -------------------------
    else:
        console.print("\n[dim][INFO] No data extracted[/dim]")

    console.print("\n[bold cyan]==============================[/bold cyan]\n")
