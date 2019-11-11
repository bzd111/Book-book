import asyncio

import aiohttp

from utils import fetch, get_resps, parser_urls

YUAN_URL = 'http://www.qu.la/book/3137/'
SAN_URL = 'https://www.qu.la/book/1983/'
TIAN_URL = 'https://www.qu.la/book/646/'
LONG_URL = 'https://www.qu.la/book/87702/'

loop = asyncio.get_event_loop()


async def main():
    urls = [YUAN_URL, SAN_URL, TIAN_URL, LONG_URL]
    # urls = [YUAN_URL]

    result = await parser_urls(urls)
    print(result)


if __name__ == '__main__':
    loop.run_until_complete(main())
