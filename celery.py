from __future__ import absolute_import

from celery import Celery

app = Celery('book', include=['book.tasks'])

app.config_from_object('book.celeryconfig')


if __name__ == "__main__":

    app.start()
