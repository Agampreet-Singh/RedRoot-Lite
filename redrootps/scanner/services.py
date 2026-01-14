# Basic service name guessing based on common ports

COMMON_SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    3306: "mysql",
    3389: "rdp",
    8080: "http-alt"
}


def enrich_services(ports):
    for p in ports:
        portnum = int(p["port"])
        if portnum in COMMON_SERVICES:
            p["service"] = COMMON_SERVICES[portnum]
