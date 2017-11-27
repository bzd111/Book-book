from __future__ import absolute_import

import redis

from book.celery import app
from book.utils import parser_url, parser_article
from book.config import (SHENG_URL, YI_URL, YUAN_URL,
                         REDIS_DB, REDIS_PORT, REDIS_HOST)

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
URLS_DICT = {
    "sheng_url": SHENG_URL,
    "yi_url": YI_URL,
    "yuan_url": YUAN_URL
}


@app.task
def check():
    for name, url in URLS_DICT.items():
        all_url = parser_url(url)
        if url == all_url:
            return
        if cache.hmget(name, ['url', 'send']) == [None, None]:
            cache.hmset(name, {"url": all_url, "send": 0})
            result = parser_article(all_url, name)
            cache.hset(name, "send", result)
        else:
            cache_url, IS_SEND = cache.hmget(name, ["url", "send"])
            IS_SEND = int(True if IS_SEND else False)
            if cache_url != all_url and IS_SEND:
                # cache.set(name, all_url)
                cache.hset(name, "url", all_url)
                result = parser_article(all_url, name)
                cache.hset(name, "send", result)
            elif not IS_SEND and cache_url == all_url:
                result = parser_article(cache_url, name)
                if result == "None" or result == None:
                    result = 0
                cache.hset(name, "send", result)
