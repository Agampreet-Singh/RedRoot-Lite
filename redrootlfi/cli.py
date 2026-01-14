import argparse
from .banner import show_banner
from .scanner import scan_lfi
from .utils import colors

def main():
    show_banner()

    parser = argparse.ArgumentParser(
        description="RedRoot LFI Scanner"
    )
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="Target URL (example: http://site/page.php?file=)"
    )

    args = parser.parse_args()

    results = scan_lfi(args.url)

    if results:
        print(colors.CRED + "\n[!] LFI Vulnerability Found:" + colors.ENDC)
        for r in results:
            print(" -", r)
    else:
        print(colors.CWHITE + "\n[-] No LFI Vulnerability Found." + colors.ENDC)