# -*- coding: utf-8 -*-
# pylint: skip-file

from flask import Flask
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        borker=app.config['CELERY_BROCKER_URL']
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

VERSION_MAJOR = 0
VERSION_MINOR = 2

app = Flask(__name__)
app.config.update(
    CELERY_BROCKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    VERSION_MAJOR=0,
    VERSION_MINOR=2
)

import sogreenit.scan
import sogreenit.results

