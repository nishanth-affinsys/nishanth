from django.db.models import (
    Count,
    Max,
    Min,
    F,
    DateField,
    ExpressionWrapper,
    TextField,
    IntegerField,
)
from django.db.models.functions import Cast, TruncDate
from rest_framework.response import Response

from console.models import MessageLogDetails
from console.serializers import MessageLogSessionsSerializer
from console.services.api_logs_utils import add_args

from main.utils.boiler_plate import get_generic_response, query
from main.utils.common_utils import convert_seconds_to_hhmmss

from main.tenant_middleware import get_current_tenant_name, get_timezone

from main.utils.dynamic_db import get_db_name, dynamic_db_connection


def total_users_periodic_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "db_schema": get_db_name("analytics"),
        "values": ["channel_id"],
        "count": True,
        "distinct": True,
    }
    return params


def total_users_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {"count": Count("channel_id", distinct=True)},
        "order_by": ["-Date"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def total_sessions_periodic_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "values": ["session_id"],
        "count": True,
        "distinct": True,
    }
    return params


def total_sessions_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {"count": Count("session_id", distinct=True)},
        "order_by": ["-Date"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def sessions_per_users_periodic_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "aggregate": {
            "count": (
                Count("session_id", distinct=True) / Count("channel_id", distinct=True)
            )
        },
        "query_set": True,
    }
    return params


def sessions_per_user_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "annotate": {
            "count": Count("session_id", distinct=True)
            / Count("channel_id", distinct=True)
        },
        "order_by": ["-Date"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def message_per_session_periodic_generic(request):
    dynamic_db_connection("analytics")
    try:
        qs = query(
            request,
            MessageLogDetails,
            MessageLogSessionsSerializer,
            db_schema=get_db_name("analytics"),
        )
        items = (
            qs.filter(
                source="user",
                message__isnull=False,
            )
            .annotate(message_as_text=Cast("message", output_field=TextField()))
            .annotate(count_message=Count("message_as_text"))
        )

        count = items.aggregate(
            count=ExpressionWrapper(
                Cast(Count("count_message"), output_field=IntegerField())
                / Count("session_id", distinct=True),
                output_field=IntegerField(),
            )
        )["count"]
        return count
    except Exception:
        return 0


def message_per_session_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(
            source="user",
            message__isnull=False,
        )
        .annotate(message_as_text=Cast("message", output_field=TextField()))
        .annotate(count_message=Count("message_as_text"))
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            count=ExpressionWrapper(
                Cast("count_message", output_field=IntegerField())
                / Count("session_id", distinct=True),
                output_field=IntegerField(),
            )
        )
        .order_by("-Date")
    )
    return items, ["Date", "count"], "messages_per_session"


def total_session_time_periodic_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user")
        .filter(
            message__isnull=False,
        )
        .values("session_id")
        .annotate(count=(Max("timestamp") - Min("timestamp")))
    )
    total_time_seconds = 0
    for i in items:
        total_time_seconds = total_time_seconds + i.get("count").total_seconds()
    total_session_time = convert_seconds_to_hhmmss(total_time_seconds)
    return total_session_time, total_time_seconds


def total_session_time_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    qs1 = (
        qs.filter(source="user")
        .filter(
            message__isnull=False,
        )
        .values("session_id", Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(count=(Max("timestamp") - Min("timestamp")))
        .order_by("-Date")
    )
    items = qs1.values("Date", "count")
    response = []
    export_list = []
    unique_dates = sorted(list(set(k.get("Date") for k in items)), reverse=True)
    for i in unique_dates:
        total_seconds = sum(
            [j.get("count").total_seconds() for j in items if j.get("Date") == i]
        )
        hhmmss = convert_seconds_to_hhmmss(total_seconds)
        r = {"Date": i, "display": hhmmss, "count": total_seconds}
        response.append(r)
        export_dict = {
            "Date": i,
            "count": hhmmss,
        }
        export_list.append(export_dict)
    return response, export_list, ["Date", "count"], "total_session_time"


def handled_or_not_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "values_kwargs": {"label": F("handled")},
        "annotate": {"count": Count("label")},
        "order_by": ["-count"],
        "not_paginated": True,
    }
    return params


def handled_message_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user", message__isnull=False, handled="Y")
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("handled"))
        .order_by("-count")[:5]
    )
    return items, ["Message", "count"], "handled_messages"


def unhandled_message_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user", message__isnull=False, handled="N")
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("handled"))
        .order_by("-count")[:5]
    )
    return items, ["Message", "count"], "unhandled_messages"
