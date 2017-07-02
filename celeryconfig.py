#!/usr/bin python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import timedelta

BROKER_URL = "redis://127.0.0.1:6379/5"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'check':{
        'task': 'book.tasks.check',
        'schedule': timedelta(seconds=10),
    }
}


if __name__ == '__main__':
    pass
