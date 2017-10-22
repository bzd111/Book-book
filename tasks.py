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
        if not cache.get(name):
            cache.set(name, all_url)
            parser_article(all_url, name)
        else:
            cache_url = cache.get(name)
            if cache_url != all_url:
                cache.set(name, all_url)
                parser_article(all_url, name)
