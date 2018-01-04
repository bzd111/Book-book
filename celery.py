from __future__ import absolute_import
import os
from celery import Celery

DIRNAME = os.path.basename(os.path.dirname(os.path.abspath("__file__")))
app = Celery(DIRNAME, include=['{}.tasks'.format(DIRNAME)])

app.config_from_object('{}.celeryconfig'.format(DIRNAME))


if __name__ == "__main__":
    app.start()
