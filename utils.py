import os
import asyncio
import inspect
import random
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
