import os
import json
from datetime import datetime
from rich.table import Table
from rich.console import Console

console = Console()

def save_metadata(payload, lhost, lport, output):
    metadata = {
        "payload": payload,
        "lhost": lhost,
        "lport": lport,
        "output_file": output,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    logs = []
    if os.path.exists("payload_logs.json"):
        try:
            with open("payload_logs.json", "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    logs.append(metadata)
    with open("payload_logs.json", "w") as f:
        json.dump(logs, f, indent=4)

def show_logs():
    if not os.path.exists("payload_logs.json"):
        console.print("[yellow]No logs found[/yellow]")
        return

    with open("payload_logs.json") as f:
        logs = json.load(f)

    table = Table(title="Payload History")
    table.add_column("Payload")
    table.add_column("LHOST")
    table.add_column("LPORT")
    table.add_column("Output")
    table.add_column("Timestamp")

    for entry in logs:
        table.add_row(
            entry["payload"],
            str(entry["lhost"]),
            str(entry["lport"]),
            entry["output_file"],
            entry["timestamp"]
        )

    console.print(table)
