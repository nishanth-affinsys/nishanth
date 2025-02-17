import logging
from django.core.management import BaseCommand
from pika_client.publisher import PikaPublisher
from tasks.lib.workers._celery.listener import Listener

from main.utils.publisher import publish_common

logger = logging.getLogger(__name__)


class CustomListener(Listener):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def callback(self, message):
        try:
            _, project, task_id, task_name, task_group, _, repeat_schedule = (
                message.split("~~")
            )
            if task_id.startswith("schedule_email"):
                publish_common(
                    data={"task_id": task_id},
                    exchange="scheduler_email",
                    routing_key="scheduler.email",
                )
                Listener.callback(message)
            elif task_id.startswith("create_views"):
                _, _, tenant = task_id.split("_")
                publish_common(
                    data={"tenant": tenant},
                    exchange="analytics_events",
                    routing_key="analytics.create.views",
                )
                Listener.callback(message)
            else:
                Listener.callback(message)
        except Exception as e:
            logger.exception("Not a listener event but key expire event")


class Command(BaseCommand):
    help = "used to run analytics listener"

    def handle(self, *args, **kwargs):
        listener = CustomListener()
        listener.listen()
