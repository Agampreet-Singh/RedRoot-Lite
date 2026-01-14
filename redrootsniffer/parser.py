from scapy.all import IP, TCP, UDP, ICMP, ARP, DNS
from datetime import datetime
from rich.console import Console

console = Console()
captured_packets = []

def parse_packet(pkt):
    timestamp = datetime.now().strftime('%H:%M:%S')
    proto = "OTHER"
    summary = ""

    try:
        if ARP in pkt:
            proto = "[yellow]ARP[/yellow]"
            summary = f"{pkt[ARP].psrc} → {pkt[ARP].pdst}"

        elif IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            length = len(pkt)

            if TCP in pkt:
                dport = pkt[TCP].dport
                sport = pkt[TCP].sport
                if dport == 80 or sport == 80:
                    proto = "[bright_green]HTTP[/bright_green]"
                elif dport == 443 or sport == 443:
                    proto = "[cyan]HTTPS[/cyan]"
                else:
                    proto = "[blue]TCP[/blue]"
                summary = f"{src}:{sport} → {dst}:{dport} | {length} bytes"

            elif UDP in pkt:
                dport = pkt[UDP].dport
                sport = pkt[UDP].sport
                if dport == 53 or sport == 53:
                    proto = "[bright_magenta]DNS[/bright_magenta]"
                    if DNS in pkt and pkt[DNS].qd is not None:
                        qname = pkt[DNS].qd.qname.decode(errors="ignore")
                        summary = f"{src}:{sport} → {dst}:{dport} | Query: {qname}"
                    else:
                        summary = f"{src}:{sport} → {dst}:{dport} | {length} bytes"
                else:
                    proto = "[green]UDP[/green]"
                    summary = f"{src}:{sport} → {dst}:{dport} | {length} bytes"

            elif ICMP in pkt:
                proto = "[magenta]ICMP[/magenta]"
                summary = f"{src} → {dst} | Type {pkt[ICMP].type}"

            else:
                proto = "[white]IP[/white]"
                summary = f"{src} → {dst} | {length} bytes"

        console.print(f"[{timestamp}] {proto} | {summary}")
        captured_packets.append(pkt)

    except Exception as e:
        console.print(f"[!] Error parsing packet: {e}", style="bold red")
