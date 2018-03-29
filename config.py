#!/usr/bin python
# -*- coding: utf-8 -*-
import os
import sys
import logging.config


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(ROOT_PATH, 'logs')

YI_URL = "http://www.biquge.cc/html/9/9378/"
YUAN_URL_1 = "http://www.biquge.cc/html/0/291/"
FEI_URL = "http://www.biquge.cc/html/139/139744/"

YI_URL_1 = "http://www.qu.la/book/16431/"
YUAN_URL = "http://www.qu.la/book/3137/"

URLS_DICT = {
    "yi_url": YI_URL,
    "yuan_url": YUAN_URL,
    "fei_url": FEI_URL
}

ARTICLES_DICT = {
    'yi_url': "一念永恒  ",
    'yuan_url': "元尊",
    "fei_url": "飞剑问道"
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
            '[%(levelname)s][%(asctime)s][%(module)s][%(process)d] %(message)s'  # flake8: noqa
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
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except os.error:
        return False
    return True


def makedirs(name, mode=0777):
    if not exists(name):
        os.makedirs(name, mode)


makedirs(LOGS_DIR)
logging.config.dictConfig(LOGGING)


try:
    from local_settings import *  # noqa
except ImportError:
    from settings import  * # noqa
