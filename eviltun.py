import subprocess
import sys
from colorama import init, Fore, Style

init(autoreset=True)

OPERATORS = {
    "1": "Telecom",
    "2": "Orange",
    "3": "Ooredoo"
}

def show_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
███████╗██╗   ██╗██╗██╗     ████████╗██╗   ██╗██╗   ██╗
██╔════╝██║   ██║██║██║     ╚══██╔══╝██║   ██║██║   ██║
█████╗  ██║   ██║██║██║        ██║   ██║   ██║██║   ██║
██╔══╝  ██║   ██║██║██║        ██║   ██║   ██║██║   ██║
███████╗╚██████╔╝██║███████╗   ██║   ╚██████╔╝╚██████╔╝
╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ 
{Fore.YELLOW}             ⚡ EVILTUN OTP FLOODER ⚡
{Style.RESET_ALL}
"""
    print(banner)

def main():
    show_banner()

    script_map = {
        "1": "assets/telecom.py",
        "2": "assets/orange.py",
        "3": "assets/ooredoo.py"
    }

    while True:
        print(Fore.RED + "Choose Operator:")
        print(Fore.YELLOW + "1 - Telecom")
        print(Fore.YELLOW + "2 - Orange")
        print(Fore.YELLOW + "3 - Ooredoo")

        choice = input(Fore.CYAN + "Your choice: ").strip()

        if choice in OPERATORS:
            print(Fore.GREEN + f"Running {OPERATORS[choice]} script...\n")
            subprocess.run([sys.executable, script_map[choice]])
            break
        else:
            print(Fore.RED + "This is not a valid command. Please try again.\n")

if __name__ == "__main__":
    main()
