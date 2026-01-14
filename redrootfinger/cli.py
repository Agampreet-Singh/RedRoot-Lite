import argparse
import json
import asyncio
from colorama import Fore, Style, init

from .scanner import scan
from .banner import show_banner


def main():
    init(autoreset=True)
    show_banner()

    parser = argparse.ArgumentParser(
        description="RedRootFinger Mark 50 – Advanced Web Fingerprinting"
    )
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="Target URL (e.g. https://example.com)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    try:
        results = asyncio.run(scan(args.url))
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        return
    except Exception as e:
        print(f"\n[!] Scan failed: {e}")
        return

    if args.json:
        print(json.dumps(results, indent=4))
        return

    print(f"{Fore.GREEN}[+] Server Headers:{Style.RESET_ALL}")
    if results.get("server_headers"):
        for k, v in results["server_headers"].items():
            print(f"  {k}: {v}")
    else:
        print("  None")

    print(f"\n{Fore.GREEN}[+] JavaScript Frameworks:{Style.RESET_ALL}")
    js = results.get("js_frameworks", [])
    print(", ".join(js) if js else "None")

    print(f"\n{Fore.GREEN}[+] CMS Detected:{Style.RESET_ALL}")
    cms = results.get("cms", {})
    if cms and "error" not in cms:
        for name, versions in cms.items():
            version_str = ", ".join(versions) if versions else "Unknown version"
            print(f"  {name} ({version_str})")
    else:
        print("None")

    print(f"\n{Fore.GREEN}[+] WAF (Passive):{Style.RESET_ALL}")
    waf_passive = results.get("waf_passive", [])
    print(", ".join(waf_passive) if waf_passive else "None")

    print(f"{Fore.GREEN}[+] WAF (Active):{Style.RESET_ALL}")
    print("Detected" if results.get("waf_active") else "Not detected")


if __name__ == "__main__":
    main()
