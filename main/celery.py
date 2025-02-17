import os
from celery import Celery

# importing once so that tasks is initialized once, making sure pubsub is initialized once, hence re-using broker connections
from tasks.lib.publisher.utils import background

# for running tasks
from tasks.lib.workers._celery.main import run_consumer

import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

app = Celery("main")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
