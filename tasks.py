# coding: utf-8
from __future__ import absolute_import
import logging

import redis

from .celery import app
from .utils import parser_url, parser_article
from .config import (URLS_DICT, REDIS_DB, REDIS_PORT, REDIS_HOST)

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

log = logging.getLogger("tasks")
log.info("tasks.name: {}".format(__name__))

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
            log.info("Before cache_url: {}, IS_SEND: {}".format(cache_url, IS_SEND))
            IS_SEND = int(True if int(IS_SEND) else False)
            log.info("After cache_url: {}, IS_SEND: {}".format(cache_url, IS_SEND))
            if cache_url != all_url and IS_SEND:
                # cache.set(name, all_url)
                cache.hset(name, "url", all_url)
                result = parser_article(all_url, name)
                cache.hset(name, "send", result)
            elif not IS_SEND and cache_url == all_url:
                result = parser_article(cache_url, name)
                if result == "None" or result == None:
                    result = 0
                log.info("result: {}".format(result))
                cache.hset(name, "send", result)
