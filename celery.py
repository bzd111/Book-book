from __future__ import absolute_import
import os
from celery import Celery

BASENAME = os.path.basename(__file__)
app = Celery(BASENAME, include=['{}.tasks'.format(BASENAME)])

app.config_from_object('{}.celeryconfig'.format(BASENAME))


if __name__ == "__main__":

    app.start()
