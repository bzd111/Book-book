#!/usr/bin python
# -*- coding: utf-8 -*-


DA_URL = "http://www.biquge.cc/html/60/60821/"
SHENG_URL = "http://www.biquge.cc/html/156/156129/"
YI_URL = "http://www.biquge.cc/html/9/9378/"

REDIS_DB = 0
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

try:
    from local_settings import *  # noqa
except ImportError:
    pass
