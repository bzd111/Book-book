# coding: utf-8
from __future__ import absolute_import
import logging
import os

import redis

from .celery import app
from .utils import parser_url, parser_article
from .config import (URLS_DICT, REDIS_DB, REDIS_PORT, REDIS_HOST)

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

log = logging.getLogger('tasks')
log.info('tasks.name: {}'.format(__name__))


@app.task
def check():
    for name, info in URLS_DICT.items():
        url = info[0]
        latest_url = parser_url(url)
        if url == latest_url:
            return
        cache_url = cache.lrange(name, -10, -1)
        if not cache_url or deal_url(latest_url) not in cache_url:
            result = parser_article(latest_url, name)
            if result:
                cache.rpush(name, deal_url(latest_url))


def deal_url(url):
    url = url if not url.endswith('/') else url[:-1]
    return os.path.basename(url)
