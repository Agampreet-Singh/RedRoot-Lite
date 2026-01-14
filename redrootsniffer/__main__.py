from redrootsniffer.banner import animate_typing_banner
from redrootsniffer.sniffer import start_sniff
from redrootsniffer.summary import print_summary_and_save
import argparse
from rich.console import Console

console = Console()

if __name__ == '__main__':
    animate_typing_banner()

    parser = argparse.ArgumentParser(description='RedRootSniffer - Professional Packet Sniffer')
    parser.add_argument('--iface', required=True, help='Interface to sniff on (e.g., eth0)')
    parser.add_argument('--count', type=int, default=0, help='Number of packets to capture (0 = unlimited)')
    parser.add_argument('--proto', choices=['tcp','udp','icmp','arp','dns','http','https','all'], default='all', help='Protocol filter')
    parser.add_argument('--bpf', default='', help='BPF-style filter (e.g., "port 80")')
    parser.add_argument('--save', help='Path to save captured packets as .pcap (default: auto-generated)')
    args = parser.parse_args()

    try:
        start_sniff(args.iface, args.count, args.proto, args.bpf)
    except KeyboardInterrupt:
        console.print("\n[!] Stopped by user.", style="bold red")
    finally:
        print_summary_and_save(args.save)
