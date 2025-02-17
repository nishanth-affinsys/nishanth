import json

from pika_client.consumers.standard import PikaConsumer

from django.core.management import call_command
from console.management.utils.utils import schedule_views
from console.management.utils.cta_checker import check_if_cta_exists
from scheduler.utils.scheduler_task import handle_scheduler_task, run_task
import logging

logger = logging.getLogger(__name__)


class Command(PikaConsumer):
    help = "Consumer that handles deletion and creation of views"

    EXCHANGES = [
        {"NAME": "project_events", "TYPE": "direct", "DURABLE": True},
        {"NAME": "analytics_cta", "TYPE": "direct", "DURABLE": True},
        {"NAME": "scheduler_task", "TYPE": "direct", "DURABLE": True},
        {"NAME": "scheduler_email", "TYPE": "direct", "DURABLE": True},
        {"NAME": "analytics_events", "TYPE": "direct", "DURABLE": True},
    ]
    QUEUES = [
        {
            "NAME": "analytics",
            "DURABLE": True,
            "BINDINGS": [
                {
                    "EXCHANGE": "project_events",
                    "ROUTING_KEY": "project.create",
                },
                {
                    "EXCHANGE": "analytics_cta",
                    "ROUTING_KEY": "analytics.cta",
                },
                {
                    "EXCHANGE": "scheduler_task",
                    "ROUTING_KEY": "scheduler.task",
                },
                {
                    "EXCHANGE": "scheduler_email",
                    "ROUTING_KEY": "scheduler.email",
                },
                {
                    "EXCHANGE": "analytics_events",
                    "ROUTING_KEY": "analytics.create.views",
                },
            ],
        },
    ]

    @staticmethod
    def handle_create_views(data: dict):
        schedule_views(data)

    @staticmethod
    def handle_cta_check(data: dict):
        check_if_cta_exists(data)

    @staticmethod
    def handle_scheduler_task(data: dict):
        handle_scheduler_task(data)

    @staticmethod
    def run_email_task(data: dict):
        run_task(data)

    @staticmethod
    def analytics_event(data: dict):
        tenant = data.get("tenant")
        call_command("create_views", tenant=tenant)

    def handle_message(self, body, *args, **options):
        try:
            data = json.loads(body)
            routing_key = options.get("method").routing_key
            logger.info(
                f"Data received from consumer for routing_key {routing_key}: {json.dumps(data, indent=4)}"
            )
            if routing_key == "project.create":
                self.handle_create_views(data)
            elif routing_key == "analytics.cta":
                self.handle_cta_check(data)
            elif routing_key == "scheduler.task":
                self.handle_scheduler_task(data)
            elif routing_key == "scheduler.email":
                self.run_email_task(data)
            elif routing_key == "analytics.create.views":
                self.analytics_event(data)
        except Exception as e:
            logger.exception(
                f"Exception raised while consuming message queue: {e}", exc_info=True
            )
