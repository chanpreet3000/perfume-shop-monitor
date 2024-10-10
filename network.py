import os
import random
import time
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

from Logger import Logger

load_dotenv()

WEBSHARE_API_TOKEN = os.getenv('WEBSHARE_API_TOKEN')

USER_AGENTS: List[str] = [
    "Mozilla/5.0 (Windows NT 10.3; x64; en-US) AppleWebKit/537.18 (KHTML, like Gecko) Chrome/47.0.3018.326 Safari/602",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; x64) AppleWebKit/536.34 (KHTML, like Gecko) Chrome/53.0.3729.200 Safari/535.7 Edge/18.45296",
    "Mozilla/5.0 (Windows; Windows NT 10.0;) Gecko/20130401 Firefox/45.1",
    "Mozilla/5.0 (Windows; U; Windows NT 10.4; Win64; x64; en-US) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/54.0.1149.120 Safari/601",
    "Mozilla/5.0 (Windows; Windows NT 10.1;; en-US) AppleWebKit/533.45 (KHTML, like Gecko) Chrome/47.0.1286.312 Safari/537",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.9 (KHTML, like Gecko) Chrome/50.0.1924.339 Safari/602.2 Edge/16.61010",
    "Mozilla/5.0 (Windows; Windows NT 6.0; x64; en-US) AppleWebKit/536.12 (KHTML, like Gecko) Chrome/54.0.2432.396 Safari/537",
    "Mozilla/5.0 (Windows NT 6.2; x64) Gecko/20100101 Firefox/70.4",
    "Mozilla/5.0 (Windows; U; Windows NT 10.4; x64; en-US) Gecko/20130401 Firefox/59.7",
    "Mozilla/5.0 (compatible; MSIE 7.0; Windows; U; Windows NT 6.3; x64 Trident/4.0)",
    "Mozilla/5.0 (Windows; Windows NT 10.3; WOW64) AppleWebKit/600.15 (KHTML, like Gecko) Chrome/52.0.1630.193 Safari/600",
    "Mozilla/5.0 (Windows NT 6.1;) AppleWebKit/600.7 (KHTML, like Gecko) Chrome/47.0.1876.234 Safari/602",
    "Mozilla/5.0 (Windows NT 10.4;; en-US) AppleWebKit/601.30 (KHTML, like Gecko) Chrome/47.0.2603.240 Safari/533",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/600.45 (KHTML, like Gecko) Chrome/50.0.1513.227 Safari/534",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 10.3; x64 Trident/6.0)",
    "Mozilla/5.0 (Windows NT 6.3;) AppleWebKit/600.41 (KHTML, like Gecko) Chrome/51.0.1865.139 Safari/534",
    "Mozilla/5.0 (Windows NT 10.0; x64; en-US) Gecko/20100101 Firefox/71.8",
    "Mozilla/5.0 (Windows; U; Windows NT 10.4; x64; en-US) AppleWebKit/603.20 (KHTML, like Gecko) Chrome/47.0.2060.332 Safari/536",
    "Mozilla/5.0 (Windows NT 6.0;; en-US) AppleWebKit/533.21 (KHTML, like Gecko) Chrome/54.0.1535.147 Safari/537.3 Edge/10.48402",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/55.0.2262.172 Safari/537.6 Edge/16.66798",
]


def getHeader():
    current_time_ms = int(time.time() * 1000)
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'occ-personalization-id': 'cf7088c4-b393-41b1-94d4-0ad108d5fb72',
        'occ-personalization-time': str(current_time_ms),
        'origin': 'https://www.theperfumeshop.com',
        'priority': 'u=1, i',
        'referer': 'https://www.theperfumeshop.com/',
        'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': get_random_user_agent(),
        'x-anonymous-consents': '%5B%5D',
    }


def get_random_proxy(proxies: List[Dict[str, str]]) -> Dict[str, str]:
    return random.choice(proxies)


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def get_proxies_from_webshare() -> List[Dict[str, str]]:
    response = requests.get(
        "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100",
        headers={"Authorization": f"Token {WEBSHARE_API_TOKEN}"}
    )

    proxies_data = response.json()
    proxies_list = proxies_data.get('results', [])

    formatted_proxies = []
    for proxy in proxies_list:
        proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}"
        formatted_proxies.append({'http': proxy_url, 'https': proxy_url})

    if len(formatted_proxies) == 0:
        raise Exception("No proxies available")
    Logger.info(f"Loaded {len(formatted_proxies)} proxies from Webshare")
    return formatted_proxies


def fetch_with_proxy(proxies: List[Dict[str, str]], url: str, method: str = 'GET', data: Dict[str, Any] = None,
                     params: Dict[str, Any] = None, max_retries: int = 3, timeout: int = 8,
                     cookies=None) -> requests.Response:
    if cookies is None:
        cookies = {}

    proxy = None
    for attempt in range(max_retries):
        try:
            headers = getHeader()
            proxy = get_random_proxy(proxies)
            Logger.debug(f"Attempt {attempt + 1}/{max_retries} - Using proxy: {proxy['http']}")

            response = requests.request(
                method,
                url,
                headers=headers,
                proxies=proxy,
                data=data,
                params=params,
                timeout=timeout,
                cookies=cookies
            )

            response.raise_for_status()
            Logger.info(f"Successfully fetched data from {url}")
            return response

        except requests.RequestException as e:
            Logger.warn(f"Attempt {attempt + 1}/{max_retries} failed for {url}", {
                "error": str(e),
                "proxy": proxy['http']
            })

            if attempt == max_retries - 1:
                Logger.error(f"All attempts failed for {url}", {
                    "last_error": str(e),
                    "total_attempts": max_retries
                })
                raise Exception(f"All attempts failed for {url}. Last error: {str(e)}")
            else:
                retry_delay = random.uniform(1, 3)
                Logger.info(f"Retrying in {retry_delay:.2f} seconds...")
                time.sleep(retry_delay)

    raise Exception("Unexpected error in fetch_with_proxy")
