from scapy.all import wrpcap, ARP, IP, TCP, UDP, ICMP, DNS
from collections import Counter
from datetime import datetime
from rich.console import Console
from redrootsniffer.parser import captured_packets
import os

console = Console()

def print_summary_and_save(save_path=None):
    if not captured_packets:
        console.print("[!] No packets captured.", style="bold yellow")
        return

    proto_counts = Counter()
    for pkt in captured_packets:
        if ARP in pkt: proto_counts["ARP"] += 1
        elif IP in pkt:
            if TCP in pkt:
                if pkt[TCP].dport in (80,8080,8000) or pkt[TCP].sport in (80,8080,8000):
                    proto_counts["HTTP"] += 1
                elif pkt[TCP].dport == 443 or pkt[TCP].sport == 443:
                    proto_counts["HTTPS"] += 1
                else: proto_counts["TCP"] += 1
            elif UDP in pkt:
                if pkt[UDP].dport==53 or pkt[UDP].sport==53: proto_counts["DNS"] += 1
                else: proto_counts["UDP"] += 1
            elif ICMP in pkt: proto_counts["ICMP"] += 1
            else: proto_counts["IP"] += 1
        else: proto_counts["OTHER"] += 1

    console.print(f"\n[+] Capture Summary: {len(captured_packets)} packets", style="bold cyan")
    for proto, count in proto_counts.items():
        console.print(f"   • {proto}: {count}")

    if not save_path:
        save_path = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"

    wrpcap(save_path, captured_packets)
    console.print(f"[+] Packets saved to [bold green]{os.path.abspath(save_path)}[/bold green]")
