from scapy.all import sniff
from redrootsniffer.parser import parse_packet
from rich.console import Console

console = Console()

def start_sniff(interface, count, proto_filter, bpf_filter):
    console.print(f"[*] Sniffing on [bold cyan]{interface}[/bold cyan] | Protocol: [bold yellow]{proto_filter.upper()}[/bold yellow] | Count: [bold yellow]{count or '∞'}[/bold yellow]")
    if bpf_filter:
        console.print(f"[*] BPF Filter: [bold green]{bpf_filter}[/bold green]")

    def filter_fn(pkt):
        if proto_filter == 'all': return True
        from scapy.all import TCP, UDP, ICMP, ARP, DNS
        if proto_filter == 'tcp': return TCP in pkt
        if proto_filter == 'udp': return UDP in pkt
        if proto_filter == 'icmp': return ICMP in pkt
        if proto_filter == 'arp': return ARP in pkt
        if proto_filter == 'dns': return DNS in pkt
        if proto_filter == 'http': return TCP in pkt and (pkt[TCP].dport in (80,8080,8000) or pkt[TCP].sport in (80,8080,8000))
        if proto_filter == 'https': return TCP in pkt and (pkt[TCP].dport==443 or pkt[TCP].sport==443)
        return False

    try:
        sniff(
            iface=interface,
            prn=parse_packet,
            lfilter=filter_fn,
            filter=bpf_filter if bpf_filter else None,
            count=count if count > 0 else 0,
            store=False
        )
    except Exception as e:
        console.print(f"[!] Error: {e}", style="bold red")
