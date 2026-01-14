#!/usr/bin/env python3
# Copyright 2026 Agampreet Singh
import argparse
from datetime import datetime
from .scanner.ports import scan_target
from .scanner.services import enrich_services
from .scanner.osdetect import os_detect
from .utils.display import animate_typing_banner, display_scan_report, console
from .utils.output import save_output


def main():
    animate_typing_banner()

    parser = argparse.ArgumentParser(
        description="RedRoot - Advanced Python Port Scanner",
        epilog="Example:\n  python -m redrootps 192.168.1.1 -p 22-443 -O --save report.txt",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (default: 1-1000)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of scan threads (default: 100)")
    parser.add_argument("-O", "--osdetect", action="store_true", help="Enable OS detection")
    parser.add_argument("--save", help="Save output to file")

    args = parser.parse_args()
    start = datetime.now()

    # Parse port range
    port_range = []
    if "-" in args.ports:
        start_p, end_p = map(int, args.ports.split("-"))
        port_range = range(start_p, end_p + 1)
    else:
        port_range = [int(args.ports)]

    # Report object
    report = {
        "ip": args.target,
        "hostname": args.target,
        "ports": []
    }

    # Run scanning
    console.print(f"[+] Scanning {args.target} on ports {args.ports}", style="bold cyan")
    report["ports"] = scan_target(args.target, port_range, args.threads)

    # Try service enrichment
    enrich_services(report["ports"])

    # Run OS detection
    if args.osdetect:
        console.print("\n[+] Performing basic OS detection...", style="bold cyan")
        os_result = os_detect(args.target)
        report["os"] = os_result
    else:
        report["os"] = {"os": "Unknown", "method": "None", "ttl": None, "window": None}

    # Display report
    display_scan_report(report)

    # Save if requested
    if args.save:
        save_output(report, args.save)

    duration = datetime.now() - start
    console.print(f"[+] Scan completed in {duration}", style="bold yellow")


if __name__ == "__main__":
    main()
