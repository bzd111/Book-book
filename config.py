#!/usr/bin python
# -*- coding: utf-8 -*-


DA_URL_1 = "http://www.biquge.cc/html/60/60821/"
SHENG_URL = "http://www.biquge.cc/html/156/156129/"
YI_URL = "http://www.biquge.cc/html/9/9378/"

DA_URL = "http://www.qu.la/book/176/"
SHENG_URL_1 = "http://www.qu.la/book/24868/"
YI_URL_1 = "http://www.qu.la/book/16431/"


REDIS_DB = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

try:
    from local_settings import *  # noqa
except ImportError:
    pass
