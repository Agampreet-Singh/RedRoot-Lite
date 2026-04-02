# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

import subprocess


def run_sqlmap(url, mode="scan", deep=False, callback=None, db=None, table=None):
    cmd = [
        "sqlmap",
        "-u", url,
        "--batch",
        "--flush-session",
        "--timeout", "10",
        "--retries", "1"
    ]

    if deep:
        cmd += [
            "--level", "3",
            "--risk", "2"
        ]

    # -------------------------
    # Mode handling
    # -------------------------
    if mode == "dump":
        cmd.append("--dbs")

    elif mode == "tables":
        cmd.append("--tables")

    elif mode == "columns":
        cmd.append("--columns")

    elif mode == "dump_data":
        cmd.append("--dump")

    # -------------------------
    # Target DB / Table
    # -------------------------
    if db:
        cmd += ["-D", db]

    if table:
        cmd += ["-T", table]

    # -------------------------
    # Run sqlmap
    # -------------------------
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in iter(process.stdout.readline, ''):
        if callback:
            callback(line)

    process.stdout.close()
    process.wait()
