import time
import random
import requests
from pathlib import Path
from .utils import colors

def scan_lfi(base_url):
    payload_file = Path(__file__).parent / "payloads" / "lfi.txt"

    if not payload_file.exists():
        print(colors.CRED + "[-] Payload file missing" + colors.ENDC)
        return []

    payloads = payload_file.read_text().splitlines()

    indicators = [
        "root:x:",
        "daemon:x:",
        "bin:x:",
        "/bin/bash"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (RedRoot LFI Scanner)"
    }

    vulnerable = []

    print(colors.CBLUE + "[*] Starting LFI scan..." + colors.ENDC)

    for payload in payloads:
        if not payload.strip():
            continue

        target = base_url + payload
        print(colors.CGREEN + "[+] Testing: " + payload + colors.ENDC)

        try:
            r = requests.get(target, headers=headers, timeout=8)

            for sign in indicators:
                if sign in r.text:
                    print(colors.CRED + "[!] LFI FOUND: " + target + colors.ENDC)
                    vulnerable.append(target)
                    break

        except requests.RequestException:
            print(colors.WARNING + "[!] Request failed" + colors.ENDC)

        time.sleep(random.uniform(0.5, 1.5))

    return vulnerable
