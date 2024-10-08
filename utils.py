import os
import asyncio
import inspect
import random
import time
from datetime import datetime

import pytz

from Logger import Logger


def get_current_time():
    uk_tz = pytz.timezone('Europe/London')
    return datetime.now(uk_tz).strftime('%d %B %Y, %I:%M:%S %p %Z')


async def sleep_randomly(base_sleep: float, randomness: float = 0, message: str = None):
    delay = base_sleep + random.uniform(-randomness, randomness)
    delay = max(delay, 0)
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back
    file_name = caller_frame.f_code.co_filename
    line_number = caller_frame.f_lineno
    project_root = Logger.get_project_root()
    relative_file_name = os.path.relpath(file_name, project_root)
    relative_file_name = f"./{relative_file_name.replace(os.sep, '/')}"
    if message is None:
        Logger.debug(f'Sleeping for {delay:.2f} seconds - {relative_file_name}:{line_number})')
    else:
        Logger.debug(f'Sleeping for {delay:.2f} seconds - {message} - {relative_file_name}:{line_number})')
    await asyncio.sleep(delay)

    del current_frame, caller_frame


cookies = {}


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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-anonymous-consents': '%5B%5D',
    }
