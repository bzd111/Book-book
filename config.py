#!/usr/bin python
# -*- coding: utf-8 -*-
import logging.config
import os
import sys
from pathlib import Path

# ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = Path.cwd()
LOGS_DIR = ROOT_PATH / 'logs'

DATA_DB = os.path.join(ROOT_PATH, 'fake_useragent.json')

SHENG_URL = 'https://www.qu.la/book/24868/'
FEI_URL = 'http://www.biquge.cc/html/139/139744/'
DIAN_URL = 'https://www.qu.la/book/242/'
YUAN_URL = 'http://www.qu.la/book/3137/'
SAN_URL = 'https://www.gu.la/html/3/3815/'
TIAN_URL = 'https://www.qu.la/book/646/'
LONG_URL = 'https://www.qu.la/book/87702/'

URLS_DICT = {
    # SHENG_URL: '圣墟',
    YUAN_URL: '元尊',
    DIAN_URL: '点道为止',
    SAN_URL: '三寸人间',
    TIAN_URL: '天下第九',
    LONG_URL: '龙族Ⅴ:悼亡者的归来',
}

SLEEP_TIME = 5

LOG_LEVEL = 'DEBUG' if os.getenv('BOOK_DEBUG') else 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            # flake8: noqa
            '[%(levelname)s][%(asctime)s][%(module)s][%(process)d] %(message)s'
        },
        'simple': {'format': '[%(levelname)s] %(message)s'},
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'tasks': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'tasks.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'utils': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'utils.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'tasks': {
            'handlers': ['console', 'tasks'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'utils': {
            'handlers': ['console', 'utils'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}


def exists(path):
    '''Test whether a path exists.  Returns False for broken symbolic links'''
    try:
        os.stat(path)
    except os.error:
        return False
    return True


def makedirs(name, mode=0o777):
    if not exists(name):
        os.makedirs(name, mode)


makedirs(LOGS_DIR)
logging.config.dictConfig(LOGGING)

try:
    from local_settings import *  # noqa
except ImportError:
    pass
