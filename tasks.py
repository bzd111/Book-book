# coding: utf-8
from __future__ import absolute_import
import logging

import redis

from .celery import app
from .utils import parser_url, parser_article
from .config import (URLS_DICT, REDIS_DB, REDIS_PORT, REDIS_HOST)

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

log = logging.getLogger('tasks')
log.info('tasks.name: {}'.format(__name__))

@app.task
def check():
    for name, url in URLS_DICT.items():
        latest_url = parser_url(url)
        if url == latest_url:
            return
        cache_url, IS_SEND = cache.hmget(name, ['url', 'send'])
        log.info('Before cache_url: {}, IS_SEND: {}'.format(cache_url, IS_SEND))
        if cache_url == None and IS_SEND == None:
            result = parser_article(latest_url, name)
            cache.hmset(name, {'url': latest_url, 'send': result})
        elif cache_url != latest_url and not IS_SEND:
            result = parser_article(cache_url, name)
            cache.hset(name, 'send', result)
        elif cache_url == latest_url and not IS_SEND:
            result = parser_article(latest_url, name)
            cache.hset(name, 'send', result)
        log.info('After cache_url: {}, IS_SEND: {}'.format(cache_url, IS_SEND))
