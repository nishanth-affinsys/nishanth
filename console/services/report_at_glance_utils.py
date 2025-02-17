from itertools import groupby
from operator import itemgetter

from django.db.models import (
    Count,
    Max,
    Min,
    ExpressionWrapper,
    IntegerField,
    TextField,
)
from django.db.models.functions import Cast, TruncDate

from console.models import MessageLogDetails
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.common_utils import convert_seconds_to_hhmmss
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.utils.common_utils import custom_filters

tz_info = get_timezone()


def active_customer_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None, "customer_type__in")
    qs = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(message__isnull=False, source="user")
        .values(Date=TruncDate("timestamp", tzinfo=tz_info))
        .annotate(Active_Customer=Count("channel_id", distinct=True))
        .order_by("-Date")
    )
    return qs, ["Date", "Active_Customer"], "active_customers"


def session_per_day_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None, "customer_type__in")
    qs = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(message__isnull=False, source="user")
        .values(Date=TruncDate("timestamp", tzinfo=tz_info))
        .annotate(Total_sessions=Count("session_id", distinct=True))
        .order_by("Date")
    )
    return qs, ["Date", "Total_sessions"], "number_of_sessions"


def session_per_user_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None, "customer_type__in")
    qs = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(message__isnull=False, source="user")
        .values(Date=TruncDate("timestamp", tzinfo=tz_info))
        .annotate(
            sessions_per_user=Count("session_id", distinct=True)
                              / Count("channel_id", distinct=True)
        )
        .order_by("Date")
    )
    return qs, ["Date", "sessions_per_user"], "sessions_per_user"


def message_per_session_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None, "customer_type__in")
    qs = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(message__isnull=False, source="user")
        .annotate(message_as_text=Cast("message", output_field=TextField()))
        .values(Date=TruncDate("timestamp", tzinfo=tz_info))
        .annotate(
            message_per_session=ExpressionWrapper(
                Count("message_as_text") / Count("session_id", distinct=True),
                output_field=IntegerField(),
            )
        )
        .order_by("Date")
    )
    return qs, ["Date", "message_per_session"], "messages_per_session"


def average_session_time_linechart_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None, "customer_type__in")
    qs = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(message__isnull=False)
        .filter(source="user")
        .values("session_id", Date=TruncDate("timestamp", tzinfo=tz_info))
        .annotate(
            max_time=Max("timestamp"),
            min_time=Min("timestamp"),
            difference=(Max("timestamp") - Min("timestamp")),
        )
        .order_by("-Date")
    )
    q = sorted(qs, key=itemgetter("Date"))
    response = []
    export_list = []
    hhmmss = ""
    for key, value in groupby(q, key=itemgetter("Date")):
        total_session_time_seconds = 0
        length = 0
        for k in value:
            total_session_time_seconds += k.get("difference").total_seconds()
            length += 1
        if length == 0:
            data = {"Date": key, "Average Session Time": "00:00:00"}
        else:
            average_session_time_seconds = total_session_time_seconds / length
            hhmmss = convert_seconds_to_hhmmss(average_session_time_seconds)
            data = {
                "Date": key,
                "Average Session Time": average_session_time_seconds,
                "displayAverage Session Time": hhmmss,
            }
        response.append(data)
        export_dict = {"Date": key, "Average Session Time": hhmmss}
        export_list.append(export_dict)
    return (
        response,
        export_list,
        ["Date", "Average Session Time"],
        "average_session_time",
    )
