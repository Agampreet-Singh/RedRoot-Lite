import json
from rich.console import Console

console = Console()


def save_output(report, filename):
    try:
        if filename.endswith(".json"):
            with open(filename, "w") as f:
                json.dump(report, f, indent=4)
        else:
            with open(filename, "w") as f:
                f.write(f"RedRoot Portscanner Report\n")
                f.write(f"Target IP: {report['ip']}\n")
                f.write(f"Hostname: {report['hostname']}\n")
                if "os" in report:
                    os_info = report["os"]
                    f.write(
                        f"Detected OS: {os_info['os']} "
                        f"(Method: {os_info['method']}, TTL: {os_info['ttl']})\n"
                    )
                f.write("\nOpen Ports:\n")
                for p in report["ports"]:
                    f.write(
                        f" - {p['port']}/{p['protocol']} {p['service']} Version: {p['version']}\n"
                    )
        console.print(f"[+] Output saved to {filename}", style="bold green")
    except Exception as e:
        console.print(f"[-] Could not save the output file. Error: {e}", style="bold red")
