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


COOKIES = {
    'cookie': 'cookie'
}


def getHeader():
    base_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'occ-personalization-id': 'cf7088c4-b393-41b1-94d4-0ad108d5fb72',
        'occ-personalization-time': str(time.time_ns()),
        'origin': 'https://www.theperfumeshop.com',
        'priority': 'u=1, i',
        'referer': 'https://www.theperfumeshop.com/',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'x-anonymous-consents': '%5B%5D',
    }

    # List of browser user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 OPR/115.0.0.0',
    ]
    # Randomly select a user agent
    user_agent = random.choice(user_agents)

    # Update the headers with the selected user agent
    base_headers['user-agent'] = user_agent

    if 'Chrome' in user_agent:
        base_headers['sec-ch-ua'] = '"Chromium";v="129", "Not=A?Brand";v="8"'
    elif 'Firefox' in user_agent:
        base_headers['sec-ch-ua'] = '"Firefox";v="123", "Not=A?Brand";v="8"'
    elif 'Safari' in user_agent:
        base_headers['sec-ch-ua'] = '"Safari";v="17", "Not=A?Brand";v="8"'
    elif 'OPR' in user_agent:
        base_headers['sec-ch-ua'] = '"Opera";v="115", "Chromium";v="129", "Not=A?Brand";v="8"'
    elif 'Edg' in user_agent:
        base_headers['sec-ch-ua'] = '"Chromium";v="129", "Microsoft Edge";v="129", "Not=A?Brand";v="8"'

    return base_headers
