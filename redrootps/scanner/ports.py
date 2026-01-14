import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
            except:
                banner = ""
            return {
                "port": str(port),
                "protocol": "tcp",
                "state": "open",
                "service": "unknown",
                "version": banner
            }
    except:
        return {
            "port": str(port),
            "protocol": "tcp",
            "state": "closed",
            "service": "unknown",
            "version": ""
        }


def scan_target(ip, ports, threads=100):
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in as_completed(futures):
            result = future.result()
            if result["state"] == "open":
                results.append(result)
    return results
