"""
redrootfuzz package

Expose a simple API so other RedRoot modules can import:
from redrootfuzz import main, Fuzzer
"""
__version__ = "Mark X"

from .cli import main  # convenience: allow python -m redrootfuzz to call main
from .fuzzer import Fuzzer, load_wordlist

__all__ = ["main", "Fuzzer", "load_wordlist", "__version__"]
