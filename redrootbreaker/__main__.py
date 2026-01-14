import argparse
from .utils import print_banner
import sys


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog="redroot",
        description="RedRoot Hacking Framework - Cracker & BruteForce Modules"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Cracker subcommand
    cracker_parser = subparsers.add_parser("cracker", help="Password hash & ZIP cracker")
    cracker_parser.add_argument("--hashfile", help="File with hashes")
    cracker_parser.add_argument("--algorithm", help="Hash type (md5, sha1, sha256...)")
    cracker_parser.add_argument("--dictionary", help="Dictionary file")
    cracker_parser.add_argument("--brute", action="store_true", help="Enable brute-force mode")
    cracker_parser.add_argument("--mask", help="Mask attack pattern (e.g., ?l?l?d?d)")
    cracker_parser.add_argument("--rules", action="store_true", help="Enable rule-based mutations")
    cracker_parser.add_argument("--incremental", action="store_true", help="Enable incremental attack")
    cracker_parser.add_argument("--maxlen", type=int, default=4, help="Max length for brute-force")
    cracker_parser.add_argument("--session", help="Session file for saving results")
    cracker_parser.add_argument("--show", action="store_true", help="Show cracked hashes from session")
    cracker_parser.add_argument("--test", action="store_true", help="Benchmark cracking speed")
    cracker_parser.add_argument("--zipfile", help="Target ZIP archive")
    cracker_parser.add_argument("--zip-dict", help="Dictionary for ZIP cracking")
    cracker_parser.add_argument("--extract-shadow", nargs=2, metavar=("PASSWD", "SHADOW"), help="Extract UNIX hashes")
    cracker_parser.add_argument("--extract-sam", nargs=2, metavar=("SYSTEM", "SAM"), help="Extract Windows SAM hashes")

    # BruteForce subcommand
    brute_parser = subparsers.add_parser("bruteforce", help="Multi-service login brute-force")
    brute_parser.add_argument("--service", required=True, help="Target service (http, ssh, ftp, mysql, etc.)")
    brute_parser.add_argument("--target", required=True, help="Target host/IP")
    brute_parser.add_argument("--port", type=int, help="Target port (default depends on service)")
    brute_parser.add_argument("--users", required=True, help="User list file")
    brute_parser.add_argument("--passwords", required=True, help="Password list file")

    args = parser.parse_args()

    # Route commands
    if args.command == "cracker":
        from .cracker import run_cracker
        run_cracker(args)
    elif args.command == "bruteforce":
        from .bruteforce import run_bruteforce
        run_bruteforce(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
