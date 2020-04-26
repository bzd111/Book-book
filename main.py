import asyncio
import functools
import signal

from config import SLEEP_TIME, URLS_DICT
from utils import parser_article


async def main():
    tasks = [parser_article(name, url) for url, name in URLS_DICT.items()]
    # await parser_articles(list(URLS_DICT.keys()))
    # await asyncio.gather(*tasks)
    done, undo = await asyncio.wait(tasks)


def handle_signal(loop):
    print('loop close....')
    loop.stop()


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.add_signal_handler(signal.SIGTERM, functools.partial(handle_signal, loop=loop))
    # loop.add_signal_handler(
    # signal.SIGINT, lambda: asyncio.ensure_future(handle_signal(loop=loop))
    # )
    # asyncio.ensure_future(main())
    # loop.run_forever()
    asyncio.run(main())
