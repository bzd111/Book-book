import asyncio

from config import SLEEP_TIME, URLS_DICT
from utils import parser_article


async def main():
    while True:
        tasks = [parser_article(name, url) for url, name in URLS_DICT.items()]
        # await parser_articles(list(URLS_DICT.keys()))
        # await asyncio.gather(*tasks)
        done, undo = await asyncio.wait(tasks)
        await asyncio.sleep(SLEEP_TIME)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    loop.run_forever()
