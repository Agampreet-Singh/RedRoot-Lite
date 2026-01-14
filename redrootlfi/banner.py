import sys
import time
from .utils import colors

def show_banner():
    banner = f"""
{colors.CBLUE}
██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗ ████████╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝
██████╔╝█████╗  ██║  ██║██████╔╝██║   ██║██║   ██║   ██║   
██╔══██╗██╔══╝  ██║  ██║██╔══██╗██║   ██║██║   ██║   ██║   
██║  ██║███████╗██████╔╝██║  ██║╚██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   

        RedRoot LFI Scanner
{colors.ENDC}
"""
    for c in banner:
        print(c, end="")
        sys.stdout.flush()
        time.sleep(0.002)