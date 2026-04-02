# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

from redrootsqli.runner import run_sqlmap
from redrootsqli.utils import typewriter_print, fast_print


def scan_target(url: str, deep: bool = False):
    fast_print("[~] Starting real-time scan...\n")

    result = {
        "target": url,
        "vulnerable": False,
        "parameter": None,
        "dbms": None,
        "injection_types": [],
        "payloads": []
    }

    injection_detected = False

    def handle_output(line: str):
        nonlocal injection_detected

        lower = line.lower().strip()
        clean = line.strip()

        if "[info]" in lower or "[warning]" in lower:
            typewriter_print(f"[~] {clean}")

        if "parameter:" in lower:
            result["vulnerable"] = True
            result["parameter"] = clean.split(":", 1)[1].strip()

        if "type:" in lower:
            inj = clean.split(":", 1)[1].strip()
            if inj not in result["injection_types"]:
                result["injection_types"].append(inj)

        if "payload:" in lower:
            payload = clean.split(":", 1)[1].strip()
            if payload not in result["payloads"]:
                result["payloads"].append(payload)

        if "dbms" in lower:
            if ":" in clean:
                result["dbms"] = clean.split(":", 1)[1].strip()

        if not injection_detected and (
            "injectable" in lower or "appears to be" in lower
        ):
            injection_detected = True
            fast_print("\n[!!!] ⚠ Injection detected!\n")

    run_sqlmap(url, mode="scan", deep=deep, callback=handle_output)

    fast_print("\n[~] Scan complete.\n")
    return result


# -------------------------
# DATABASES
# -------------------------
def dump_target(url: str, deep: bool = False):
    fast_print("[~] Fetching databases...\n")

    result = {"target": url, "vulnerable": True, "databases": []}

    def handle_output(line: str):
        clean = line.strip()
        if "[*]" in clean:
            db = clean.replace("[*]", "").strip()
            if db and db not in result["databases"]:
                result["databases"].append(db)

    run_sqlmap(url, mode="dump", deep=True, callback=handle_output)
    return result


# -------------------------
# TABLES
# -------------------------
def tables_target(url: str, db: str):
    fast_print(f"[~] Fetching tables for database: {db}\n")

    result = {"target": url, "vulnerable": True, "tables": []}

    def handle_output(line: str):
        clean = line.strip()

        if clean.startswith("|") and clean.endswith("|"):
            table = clean.strip("|").strip()

            if table.lower().startswith("tables_in"):
                return

            if table and table not in result["tables"]:
                result["tables"].append(table)

    run_sqlmap(url, mode="tables", db=db, callback=handle_output)
    return result


# -------------------------
# COLUMNS
# -------------------------
def columns_target(url: str, db: str, table: str):
    fast_print(f"[~] Fetching columns for {db}.{table}\n")

    result = {"target": url, "vulnerable": True, "columns": []}

    def handle_output(line: str):
        clean = line.strip()

        if clean.startswith("|") and clean.endswith("|"):
            col = clean.strip("|").strip()

            if col.lower() in ["column", "type"]:
                return

            if col not in result["columns"]:
                result["columns"].append(col)

    run_sqlmap(url, mode="columns", db=db, table=table, callback=handle_output)
    return result


# -------------------------
# DUMP DATA (NEW)
# -------------------------
def dump_data_target(url: str, db: str, table: str):
    fast_print(f"[~] Dumping data from {db}.{table}\n")

    result = {
        "target": url,
        "vulnerable": True,
        "rows": []
    }

    def handle_output(line: str):
        clean = line.strip()

        if clean.startswith("|") and clean.endswith("|"):
            row = [x.strip() for x in clean.strip("|").split("|")]

            if any("---" in x for x in row):
                return

            if not any(row):
                return

            result["rows"].append(row)

    run_sqlmap(
        url,
        mode="dump_data",
        db=db,
        table=table,
        callback=handle_output
    )

    return result
