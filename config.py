#!/usr/bin python
# -*- coding: utf-8 -*-


SHENG_URL = "http://www.biquge.cc/html/156/156129/"
YI_URL = "http://www.biquge.cc/html/9/9378/"
YUAN_URL_1 = "http://www.biquge.cc/html/0/291/"
FEI_URL = "http://www.biquge.cc/html/139/139744/"

SHENG_URL_1 = "http://www.qu.la/book/24868/"
YI_URL_1 = "http://www.qu.la/book/16431/"
YUAN_URL = "http://www.qu.la/book/3137/"

URLS_DICT = {
    "sheng_url": SHENG_URL,
    "yi_url": YI_URL,
    "yuan_url": YUAN_URL,
    "fei_url": FEI_URL
}

REDIS_DB = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

try:
    from local_settings import *  # noqa
except ImportError:
    pass
