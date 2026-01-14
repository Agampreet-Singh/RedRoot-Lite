from scapy.all import sr1, IP, ICMP, TCP

# TTL-based rough fingerprinting
OS_TTL_FINGERPRINTS = {
    "Linux": range(60, 65),      # TTL ~64
    "Windows": range(120, 129),  # TTL ~128
    "FreeBSD/Unix": range(254, 256), # TTL ~255
}


def guess_os_from_ttl(ttl):
    for os_name, ttl_range in OS_TTL_FINGERPRINTS.items():
        if ttl in ttl_range:
            return os_name
    return "Unknown"


def os_detect(target, port=80, timeout=1):
    """
    Try OS detection using ICMP Echo and TCP SYN probes.
    """
    result = {
        "os": "Unknown",
        "method": "None",
        "ttl": None,
        "window": None
    }

    try:
        # ICMP Echo (ping)
        icmp_resp = sr1(IP(dst=target)/ICMP(), timeout=timeout, verbose=0)
        if icmp_resp:
            ttl = int(icmp_resp.ttl)
            os_guess = guess_os_from_ttl(ttl)
            result.update({"os": os_guess, "method": "ICMP", "ttl": ttl})
            return result
    except Exception:
        pass

    try:
        # TCP SYN probe
        tcp_resp = sr1(IP(dst=target)/TCP(dport=port, flags="S"), timeout=timeout, verbose=0)
        if tcp_resp and tcp_resp.haslayer(TCP):
            ttl = int(tcp_resp.ttl)
            window = tcp_resp[TCP].window
            os_guess = guess_os_from_ttl(ttl)
            result.update({"os": os_guess, "method": "TCP SYN", "ttl": ttl, "window": window})
            return result
    except Exception:
        pass

    return result
