# ==================================================
# Project: RedRoot
# Author: Agampreet Singh
# Copyright (c) 2026 Agampreet Singh
# License: Proprietary – All Rights Reserved
#
# Unauthorized copying, modification, distribution,
# or use of this file is strictly prohibited.
# ==================================================

import os


def parse_output(url: str):
    target = url.replace("http://", "").replace("https://", "").split("/")[0]

    base_path = os.path.expanduser("~/.local/share/sqlmap/output")
    path = os.path.join(base_path, target)

    result = {
        "target": target,
        "vulnerable": False,
        "parameter": None,
        "dbms": None,
        "injection_types": [],
        "payloads": [],
        "databases": []
    }

    if not os.path.exists(path):
        return result

    log_file = os.path.join(path, "log")

    if not os.path.exists(log_file):
        return result

    with open(log_file, "r", errors="ignore") as f:
        lines = f.readlines()

    capture_databases = False

    for line in lines:
        lower = line.lower().strip()

        # -------------------------
        # Parameter + vulnerability
        # -------------------------
        if "parameter:" in lower:
            result["vulnerable"] = True
            try:
                result["parameter"] = line.split(":", 1)[1].strip()
            except:
                pass

        # -------------------------
        # Injection types
        # -------------------------
        if "type:" in lower:
            try:
                inj = line.split(":", 1)[1].strip()
                if inj not in result["injection_types"]:
                    result["injection_types"].append(inj)
            except:
                pass

        # -------------------------
        # Payloads
        # -------------------------
        if "payload:" in lower:
            try:
                payload = line.split(":", 1)[1].strip()
                if payload not in result["payloads"]:
                    result["payloads"].append(payload)
            except:
                pass

        # -------------------------
        # DBMS
        # -------------------------
        if "back-end dbms" in lower:
            try:
                result["dbms"] = line.split(":", 1)[1].strip()
            except:
                pass

        # -------------------------
        # Database extraction
        # -------------------------
        if "available databases" in lower:
            capture_databases = True
            continue

        if capture_databases:
            if lower.startswith("[*]"):
                db = lower.replace("[*]", "").strip()
                if db and db not in result["databases"]:
                    result["databases"].append(db)
            else:
                if lower == "" or not lower.startswith("[*]"):
                    capture_databases = False

    return result
