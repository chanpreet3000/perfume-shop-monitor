import requests
import random
import time
from requests.exceptions import ProxyError, SSLError, ConnectionError


def read_proxies(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]


def get_random_proxy(proxies):
    proxy = random.choice(proxies)
    ip, port, username, password = proxy.split(':')
    return {
        'http': f'http://{username}:{password}@{ip}:{port}',
        'https': f'http://{username}:{password}@{ip}:{port}'
    }


proxies = read_proxies('proxies.txt')

cookies = {}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    'occ-personalization-id': '00825c91-4354-45cc-b4f2-176ebe96e709',
    'occ-personalization-time': '1728457217462',
    'origin': 'https://www.theperfumeshop.com',
    'priority': 'u=1, i',
    'referer': 'https://www.theperfumeshop.com/',
    'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Mac"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_8; en-US) AppleWebKit/601.29 (KHTML, like Gecko) Chrome/53.0.3214.218 Safari/536',
    'x-anonymous-consents': '%5B%5D',
}

params = {
    'fields': 'FULL',
    'searchType': 'PRODUCT',
    'categoryCode': 'C102',
    'lang': 'en_GB',
    'curr': 'GBP',
}

max_retries = 5
retry_delay = 2

for attempt in range(max_retries):
    try:
        proxy = get_random_proxy(proxies)
        print(f"Attempt {attempt + 1} using proxy: {proxy['https']}")

        session = requests.Session()
        session.trust_env = False  # Disable any environment proxy settings

        response = session.get(
            'https://api.theperfumeshop.com/api/v2/tpsgb/search',
            params=params,
            cookies=cookies,
            headers=headers,
            proxies=proxy,
            timeout=30,  # Increased timeout
            verify=False  # Disable SSL verification (use with caution)
        )

        print(f"Status Code: {response.status_code}")
        print(response.json())
        break  # If successful, break out of the retry loop

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if isinstance(e, (ProxyError, SSLError, ConnectionError)):
            print(f"Proxy or connection error. Retrying with a different proxy...")
        else:
            print(f"Unexpected error. Retrying...")

        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Unable to complete the request.")

# Disable SSL warnings (only if you've disabled SSL verification)
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
