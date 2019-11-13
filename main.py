import asyncio
import time

from config import SLEEP_TIME, URLS_DICT
from utils import parser_articles


async def main():
    while True:
        await parser_articles(list(URLS_DICT.keys()))
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
