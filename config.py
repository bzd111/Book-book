#!/usr/bin python
# -*- coding: utf-8 -*-
import os
import sys
import logging.config


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(ROOT_PATH, 'logs')

SHENG_URL = 'http://www.biquge.cc/html/156/156129/'
YUAN_URL_1 = 'http://www.biquge.cc/html/0/291/'
FEI_URL = 'http://www.biquge.cc/html/139/139744/'
DIAN_URL = 'https://www.biquge.cc/html/4/4675/'
SHENG_URL_1 = 'http://www.qu.la/book/24868/'
YUAN_URL = 'http://www.qu.la/book/3137/'
SAN_URL = 'https://www.biquge.cc/html/3/3815/'
TIAN_URL = 'https://www.qu.la/book/646/'
LONG_URL = 'https://www.qu.la/book/87702/'

URLS_DICT = {
    'sheng_url': (SHENG_URL, '圣墟 '),
    'yuan_url': (YUAN_URL, '元尊'),
    'fei_url': (FEI_URL, '飞剑问道'),
    'dian_url': (DIAN_URL, '点道为止'),
    'san_url': (SAN_URL, '三寸人间'),
    'tian_url': (TIAN_URL, '天下第九'),
    'long_url': (LONG_URL, '龙族Ⅴ:悼亡者的归来')
}

REDIS_DB = 0
REDIS_HOST = 'redis'
REDIS_PORT = 6379

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
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
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
        }
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
    }
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
    from settings import *  # noqa
