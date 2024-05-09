import requests
from colorama import Fore, init
from random import choice
import re
import time
import os

init(autoreset=True)
colors = [
    Fore.RED,
    Fore.YELLOW,
    Fore.BLUE,
    Fore.MAGENTA,
    Fore.CYAN,
]

def get_common_word():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
        if response.status_code == 200:
            data = response.json()
            word = data[0]
            if len(word) >= 4 and re.match(r'^[a-zA-Z]+$', word):
                return word
    except Exception as e:
        print("Error fetching word:", e)
    return None

def ello(proxy_list):
    proxy_index = 0
    attempts = 0
    while True:
        proxy = proxy_list[proxy_index]
        word = get_common_word()
        if word:
            col = choice(colors)
            headers = {
                'authority'                : 'xboxgamertag.com',
                'accept'                   : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language'          : 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
                'referer'                  : 'https://xboxgamertag.com/',
                'sec-ch-ua'                : '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile'         : '?0',
                'sec-ch-ua-platform'       : '"Windows"',
                'sec-fetch-dest'           : 'document',
                'sec-fetch-mode'           : 'navigate',
                'sec-fetch-site'           : 'same-origin',
                'sec-fetch-user'           : '?1',
                'upgrade-insecure-requests': '1',
                'user-agent'               : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            }
            try:
                response = requests.get(f'https://xboxgamertag.com/search/{word}', headers=headers, proxies={'http': f'http://{proxy}', 'http': f'http://{proxy}'})
                if response.status_code == 200:
                    print(f"{Fore.RED}[Taken] {word} {Fore.CYAN}| Proxy: {proxy}")
                elif response.status_code == 404:
                    print(f"{Fore.GREEN}[Available] {word} {Fore.CYAN}| Proxy: {proxy}")
                    with open("Available.txt", 'a') as f:
                        f.write(word + '\n')
                else:
                    print(f"{Fore.YELLOW}[?] Ratelimit")
                    time.sleep(10)
                attempts += 1
                if attempts % 5 == 0:
                    proxy_index = (proxy_index + 1) % len(proxy_list)  # Cycle through proxies
                    print(f"{Fore.BLUE}[!] Changing Proxy...	")
            except Exception as e:
                print("Exception:", e)
        else:
            print("Failed to fetch word.")

def get_new_proxies():
    try:
        response = requests.get("https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/generated/http_proxies.txt")
        if response.status_code == 200:
            with open("proxies.txt", "w") as f:
                f.write(response.text)
            print("New proxies obtained and saved to proxies.txt")
            time.sleep(5)
            main()
        else:
            print("Failed to get new proxies.")
            time.sleep(5)
            main()
    except Exception as e:
        print("Error getting new proxies:", e)
        time.sleep(10)
        main()

def main():
    while True:
        print(f"{Fore.GREEN}1. {Fore.LIGHTBLUE_EX}Run Checker")
        print(f"{Fore.GREEN}2. {Fore.LIGHTBLUE_EX}Get New Proxies")
        print("")
        choice = input(">>> ")
        if choice == "1":
            os.system('clear')
            proxy_list = open('proxies.txt', 'r').read().splitlines()
            ello(proxy_list)
        elif choice == "2":
            os.system('clear')
            get_new_proxies()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()