#!/usr/bin python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import timedelta
from celery import DIRNAME
BROKER_URL = "redis://redis:6379/5"
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERYBEAT_SCHEDULE = {
    'check':{
        'task': '{}.tasks.check'.format(DIRNAME),
        'schedule': timedelta(seconds=20),
    }
}


if __name__ == '__main__':
    pass
