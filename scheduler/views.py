from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
import requests
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from django.http.response import HttpResponse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SchedulerViewSet(GenericViewSet):
    @extend_schema(
        operation_id="schedule-complete",
        tags=[AuthTags.AUTHORIZE],
        description="details of all the actions performed in the console",
    )
    @action(methods=["POST"], detail=False, url_path="schedule-complete")
    def scheduler_complete(self, request, *args, **kwargs):
        _, _, schedule_id, tenant = request.data.get("task_id").split("_")
        response = requests.patch(
            url=f"{settings.EVENTLOGGER_SCHEDULE_UPDATE}{schedule_id}/",
            json={"status": "COMPLETED"},
            headers={"tenant": tenant},
        )
        logger.info(f"Schedule {schedule_id} completed with response {response}")
        return HttpResponse(f"Schedule {schedule_id} completed")
