#!/usr/bin python
# -*- coding: utf-8 -*-
import logging.config
import os
import sys
from pathlib import Path

ROOT_PATH = Path.cwd()
LOGS_DIR = ROOT_PATH / 'logs'
JSON_FILE = ROOT_PATH / 'urls.json'

DATA_DB = os.path.join(ROOT_PATH, 'fake_useragent.json')

SHENG_URL = 'https://www.biquge.com.cn/book/23488/'
DIAN_URL = 'https://www.biquge.com.cn/book/31583/'
YUAN_URL = 'https://www.biquge.com.cn/book/15517/'
SAN_URL = 'https://www.biquge.com.cn/book/31833/'
TIAN_URL = 'https://biquge.com.cn/book/32101/'
LONG_URL = 'https://www.biquge.com.cn/book/36825/'

URLS_DICT = {
    SHENG_URL: '圣墟',
    YUAN_URL: '元尊',
    DIAN_URL: '点道为止',
    SAN_URL: '三寸人间',
    TIAN_URL: '天下第九',
    LONG_URL: '龙族Ⅴ:悼亡者的归来',
}

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
mail_to_list = ['zxc@gogogozxc.xyz', '528475283@qq.com']
mail_host = 'smtp.qq.com'
mail_user = os.environ['MailUser']
mail_pass = os.environ['MailPass']
mail_postfix = 'qq.com'
mail_port = 465

# import from local file
try:
    from local_settings import *  # noqa
except ImportError:
    pass
