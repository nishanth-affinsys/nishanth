import requests
import logging
from datetime import timedelta
from django.utils import timezone
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from scheduler.models import Schedule
from main.tenant_middleware import set_current_tenant_name
from django.conf import settings
from django.http.response import HttpResponse

logger = logging.getLogger(__name__)


def abort_schedule_notification(schedule_id, tenant, reason):
    response = requests.patch(
        url=f"{settings.EVENTLOGGER_SCHEDULE_UPDATE}{schedule_id}/",
        cookies={"tenant": tenant},
        json={"status": "ABORTED", "abort_reason": reason},
    )
    logger.debug(f"Response from EventLogger: {response}")
    return HttpResponse(f"Schedule {schedule_id} aborted")


def schedule_information(pk, tenant):
    set_current_tenant_name(tenant)
    dynamic_db_connection("analytics")
    try:
        qs = (
            Schedule.objects.using(get_db_name("analytics", tenant))
            .filter(id=pk)
            .values()[0]
        )
        return qs
    except IndexError:
        logger.error(f"Schedule not found")


def calculate_timestamp_filters(request_body):
    filters = {}
    current_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if request_body["schedule_time"] == "DAILY":
        filters["timestamp__range"] = [current_time - timedelta(days=1), current_time]
    elif request_body["schedule_time"] == "WEEKLY":
        filters["timestamp__range"] = [current_time - timedelta(days=7), current_time]
    elif request_body["schedule_time"] == "MONTHLY":
        filters["timestamp__range"] = [current_time - timedelta(days=30), current_time]
    elif request_body["schedule_time"] == "QUARTERLY":
        filters["timestamp__range"] = [current_time - timedelta(days=120), current_time]
    logger.error(f"Timestamp filters applied are : {filters['timestamp__range']}")
    return filters


def handle_request_body(qs, tenant):
    request_body = dict()
    request_body["chart_name"] = qs.get("chart_name").split(",")
    request_body["recipient_name"] = qs.get("recipient_name").split(",")
    request_body["tenant"] = tenant
    request_body["schedule_type"] = qs.get("schedule_type")
    request_body["schedule_time"] = qs.get("schedule_time")
    request_body["end_type"] = qs.get("end_time")
    if request_body["schedule_time"] == "NOW" and qs.get("starts_on"):
        request_body["starts_on"] = timezone.now()
    else:
        request_body["starts_on"] = qs.get("starts_on")
    if qs.get("ends_on"):
        request_body["ends_on"] = qs.get("ends_on")
    request_body["occurrences"] = qs.get("occurrences")
    if request_body["schedule_time"] == "WEEKLY":
        request_body["day"] = qs.get("day", "").split(",")
    if request_body["schedule_type"] == "ONETIME":
        request_body["filters"] = {
            "timestamp__range": [qs.get("from_timerange"), qs.get("to_timerange")]
        }
    return request_body
