#!/usr/bin python
# -*- coding: utf-8 -*-
import logging.config
import os
import sys
import json
from pathlib import Path

from yarl import URL

ROOT_PATH = Path.cwd()
LOGS_DIR = ROOT_PATH / 'logs'
JSON_FILE = ROOT_PATH / 'urls.json'

DATA_DB = os.path.join(ROOT_PATH, 'fake_useragent.json')

URLS_DICT = {
    "https://www.xbiquge.so/book/55233/":"择日飞升",
}

URLS_DICT = os.getenv("URLS_DICT", URLS_DICT)

if type(URLS_DICT) == str:
    URLS_DICT = json.loads(URLS_DICT)

SLEEP_TIME = 10

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

# read from ENV
mail_to_list = os.getenv('MAIL_TO_LIST', ['zxc@bzd111.me'])
if type(mail_to_list) == str:
    mail_to_list = json.loads(mail_to_list)
mail_host = 'smtp.qq.com'
mail_user = os.getenv('MAIL_USER')
mail_pass = os.getenv('MAIL_PASS')
mail_postfix = 'qq.com'
mail_port = 465

# import from local file
try:
    from local_settings import *  # noqa
except ImportError:
    pass
