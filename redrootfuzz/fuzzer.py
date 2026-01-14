"""
Fuzzer core.

Dependencies:
 - Optional: dnspython (pip install dnspython) for better DNS resolution
 - Optional: requests (pip install requests) for HTTP checks

This file is self-contained and importable by other RedRoot modules.
"""
from __future__ import annotations
import random
import socket
import string
import time
import threading
import concurrent.futures
from typing import Iterable, List, Optional, Set, Tuple

# optional imports
try:
    import dns.resolver  # type: ignore
except Exception:
    dns = None  # fallback to socket

try:
    import requests  # type: ignore
except Exception:
    requests = None

_lock = threading.Lock()

def load_wordlist(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def generate_permutations(words: Iterable[str], max_numbers: int = 2) -> Iterable[str]:
    prefixes = ["", "dev", "staging", "test", "www"]
    suffixes = ["", "dev", "staging", "test"]
    for w in words:
        yield w
        # numeric postfixes
        for i in range(1, max_numbers + 1):
            yield f"{w}{i}"
        # prefix/suffix combos
        for p in prefixes:
            if p:
                yield f"{p}-{w}"
                yield f"{w}-{p}"
        for s in suffixes:
            if s:
                yield f"{w}-{s}"

def resolve_with_dnspython(name: str, resolver: "dns.resolver.Resolver") -> List[str]:
    ips: List[str] = []
    try:
        answers = resolver.resolve(name, "A", lifetime=4)
        for r in answers:
            ips.append(r.address)
    except Exception:
        pass
    try:
        answers6 = resolver.resolve(name, "AAAA", lifetime=4)
        for r in answers6:
            if r.address not in ips:
                ips.append(r.address)
    except Exception:
        pass
    return ips

def resolve_with_socket(name: str) -> List[str]:
    try:
        results = socket.getaddrinfo(name, None)
        ips: List[str] = []
        for res in results:
            ip = res[4][0]
            if ip not in ips:
                ips.append(ip)
        return ips
    except Exception:
        return []

def detect_wildcard(domain: str, resolver: Optional["dns.resolver.Resolver"]) -> Set[str]:
    sample_ips: Set[str] = set()
    for _ in range(3):
        token = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        name = f"{token}.{domain}"
        if resolver and dns:
            ips = resolve_with_dnspython(name, resolver)
        else:
            ips = resolve_with_socket(name)
        sample_ips.update(ips)
        time.sleep(0.15)
    return sample_ips

def http_check(host: str, timeout: float = 3.0) -> Tuple[bool, Optional[int]]:
    if requests is None:
        return False, None
    # try HTTP then HTTPS
    try:
        r = requests.get(f"http://{host}/", timeout=timeout)
        return True, r.status_code
    except Exception:
        try:
            r = requests.get(f"https://{host}/", timeout=timeout, verify=False)
            return True, r.status_code
        except Exception:
            return False, None

class Fuzzer:
    def __init__(self,
                 domain: str,
                 words: Iterable[str],
                 threads: int = 30,
                 resolver_names: Optional[List[str]] = None,
                 http: bool = False,
                 timeout: float = 5.0):
        self.domain = domain.strip().lower()
        self.words = list(words)
        self.threads = max(1, threads)
        self.http = http
        self.timeout = timeout
        self.resolver = None
        if dns and resolver_names:
            self.resolver = dns.resolver.Resolver(configure=False)
            self.resolver.nameservers = resolver_names
        elif dns:
            self.resolver = dns.resolver.Resolver()

        self.found: List[Tuple[str, List[str], Optional[int]]] = []
        self._seen: Set[str] = set()
        self.wildcard_ips: Set[str] = set()

    def _resolve(self, fqdn: str) -> List[str]:
        if self.resolver and dns:
            return resolve_with_dnspython(fqdn, self.resolver)
        return resolve_with_socket(fqdn)

    def _worker(self, token: str):
        fqdn = f"{token}.{self.domain}"
        try:
            ips = self._resolve(fqdn)
        except Exception:
            ips = []

        if not ips:
            return

        # if wildcard IPs exactly match, skip (likely catch-all)
        if self.wildcard_ips and set(ips) == self.wildcard_ips:
            return

        http_status = None
        if self.http:
            ok, status = http_check(fqdn, timeout=self.timeout)
            if ok:
                http_status = status

        with _lock:
            if fqdn not in self._seen:
                self._seen.add(fqdn)
                self.found.append((fqdn, ips, http_status))

    def run(self, permutations: bool = True, show_progress: bool = True) -> List[Tuple[str, List[str], Optional[int]]]:
        tokens = generate_permutations(self.words) if permutations else (w for w in self.words)
        tokens = list(tokens)

        # detect wildcard/catch-all
        self.wildcard_ips = detect_wildcard(self.domain, self.resolver)

        if show_progress:
            print(f"[*] Starting fuzz: domain={self.domain}, candidates={len(tokens)}, threads={self.threads}")
            if self.wildcard_ips:
                example = ', '.join(list(self.wildcard_ips)[:3])
                print(f"[!] Wildcard DNS detected, example IPs: {example}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as ex:
            futures = [ex.submit(self._worker, t) for t in tokens]
            try:
                for _ in concurrent.futures.as_completed(futures):
                    pass
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user")

        return self.found
