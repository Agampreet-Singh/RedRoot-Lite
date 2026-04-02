# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

import typer
from redrootsqli.scanner import (
    scan_target,
    dump_target,
    tables_target,
    columns_target,
    dump_data_target   # ✅ ADD THIS
)
from redrootsqli.formatter import print_banner, print_result

app = typer.Typer(help="RedRootSQLi - Advanced SQL Injection Scanner")


# -------------------------
# SCAN
# -------------------------
@app.command()
def scan(url: str, deep: bool = False):
    print_banner()
    result = scan_target(url, deep=deep)
    print_result(result)


# -------------------------
# DATABASES
# -------------------------
@app.command()
def dump(url: str):
    print_banner()
    result = dump_target(url)
    print_result(result)


# -------------------------
# TABLES
# -------------------------
@app.command()
def tables(url: str, db: str):
    print_banner()
    result = tables_target(url, db)
    print_result(result)


# -------------------------
# COLUMNS
# -------------------------
@app.command()
def columns(url: str, db: str, table: str):
    print_banner()
    result = columns_target(url, db, table)
    print_result(result)

# -------------------------
# DUMPING DATA
# -------------------------
@app.command()
def dump_data(url: str, db: str, table: str):
    print_banner()
    result = dump_data_target(url, db, table)
    print_result(result)

if __name__ == "__main__":
    app()
