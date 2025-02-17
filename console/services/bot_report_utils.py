from __future__ import annotations
from itertools import groupby
from operator import itemgetter

from django.db.models import (
    Count,
    Value,
    Max,
    Min,
    CharField,
    F,
    FloatField,
    TextField,
)
from django.db.models.functions import Cast, Trunc, Concat, TruncDate

from console.models import MessageLogDetails, UserFlow
from console.serializers import MessageLogSessionsSerializer, DailyTrafficSerializer

from main.utils.date_range import get_date_ranges
from main.utils.boiler_plate import query
from main.utils.common_utils import convert_seconds_to_hhmmss

from main.tenant_middleware import get_timezone
from console.services.api_logs_utils import add_args
from main.utils.common_utils import custom_filters
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from django.db import connections


def messages_faq_generic(request):
    dynamic_db_connection("analytics")
    # converted to text to handle oracle error
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user", message__isnull=False)
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("channel")
        .annotate(count=Count("Message"))
        .order_by("-count")
    )
    return items, ["channel", "count"], "bot_messages"


def total_message_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source__in=["user", "llm"], message__isnull=False)
        .annotate(message_as_text=Cast("message", output_field=TextField()))
        .values("session_id", "channel")
        .annotate(total_messages=Count("message_as_text"))
        .order_by("-total_messages")
    )
    return items, ["session_id", "channel", "total_messages"], "messages_by_session"


def top_intents_generic(request):  # top matched intents
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source__in=["user", "llm"], message__isnull=False, handled="Y")
        .annotate(message_as_text=Cast("message", output_field=TextField()))
        .values("intent", "channel")
        .annotate(count=Count("message_as_text"))
        .order_by("-count")
    )
    return items, ["intent", "channel", "count"], "top_matched_intents"


def top_ten_matched_intents_by_channel_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    channels_list = qs.values_list("channel", flat=True).distinct().order_by("-channel")
    result = []
    for channel in channels_list:
        channel_items = (
            qs.filter(channel=channel)
            .filter(source__in=["user", "llm"], message__isnull=False, handled="Y")
            .annotate(message_as_text=Cast("message", output_field=TextField()))
            .values(
                "channel",
                "intent",
            )
            .annotate(count=Count("message_as_text"))
            .order_by("-count", "channel")[:10]
        )
        for final_channel in channel_items:
            result.append(final_channel)
    return result, ["channel", "intent", "count"], "top10_matched_intents"


def top_messages_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source__in=["user", "llm"], message__isnull=False)
        .exclude(session_id__isnull=True)
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("Message"))
        .order_by("-count")
    )
    return items, ["Message", "count"], "top_messages"


def total_matched_intents_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "handled": "Y",
            "source__in": ["user", "llm"],
            "message__isnull": False,
        },
        "values_kwargs": {"Channel": F("channel")},
        "annotate": {"Count": Count("intent")},
        "order_by": ["-Count"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def total_unmatched_intents_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "handled": "N",
            "source__in": ["user", "llm"],
            "message__isnull": False,
        },
        "values_kwargs": {"Channel": F("channel")},
        "annotate": {"Count": Count("intent")},
        "order_by": ["-Count"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def total_active_customers_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, DailyTrafficSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(message__isnull=False, source__in=["user", "llm"])
        .values("channel")
        .annotate(count=Count("channel_id", distinct=True))
    )

    return items, ["channel", "count"], "active_customers"


def number_of_users_interactions_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, DailyTrafficSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(message__isnull=False, source__in=["user", "llm"])
        .values("channel")
        .annotate(count=Count("session_id", distinct=True))
    )
    return items, ["channel", "count"], "no_of_user_sessions"


def average_session_time_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs2 = (
        MessageLogDetails.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(source__in=["user", "llm"])
        .filter(message__isnull=False)
        .values("session_id", "channel")
        .annotate(
            max_time=Max("timestamp"),
            min_time=Min("timestamp"),
            difference=(Max("timestamp") - Min("timestamp")),
        )
        .order_by()
    )
    q = sorted(qs2, key=itemgetter("channel"))
    response = []
    for key, value in groupby(q, key=itemgetter("channel")):
        total_session_time_seconds = 0
        length = 0
        for k in value:
            total_session_time_seconds += k.get("difference").total_seconds()
            length += 1
        if length == 0:
            data = {"Channel": key, "Average Session Time": "00:00:00"}
        else:
            average_session_time = total_session_time_seconds / length
            hhmmss = convert_seconds_to_hhmmss(average_session_time)
            data = {"Channel": key, "Average Session Time": hhmmss}
        response.append(data)
    return response, ["Channel", "Average Session Time"], "avg_session_time"


def average_message_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    qs1 = (
        get_qs.filter(source__in=["user", "llm"])
        .filter(
            message__isnull=False,
        )
        .values("message", "channel")
    )
    qs2 = (
        get_qs.filter(source__in=["user", "llm"])
        .filter(
            message__isnull=False,
        )
        .values("session_id")
        .distinct()
        .count()
    )
    q = sorted(qs1, key=itemgetter("channel"))
    response = []
    for key, value in groupby(q, key=itemgetter("channel")):
        totalmessage = 0
        for _ in value:
            totalmessage += 1
        if qs2 == 0:
            data = {"Channel": key, "Average Messages per Session": 0}
        else:
            data = {
                "Channel": key,
                "Average Messages per Session": round(totalmessage / qs2, 2),
            }

        response.append(data)
    return response, ["Channel", "Average Messages per Session"], "avg_msg_per_session"


def new_user_in_bot_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    result = (
        get_qs.filter(source__in=["user", "llm"])
        .filter(
            message__isnull=False,
        )
        .values("channel_id")
        .annotate(
            visits=Count("session_id", distinct=True),
            Channel=F("channel"),
            Customer=F("channel_id"),
            Time=Min(
                Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            ),
        )
        .filter(visits=1)
        .values("Customer", "Channel", "Time")
        .order_by("-Time")
    )
    return result, ["Customer", "Channel", "Time"], "new_user_in_BOT"


def conversation_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source__in": ["user", "llm"],
            "message__isnull": False,
        },
        "values_kwargs": {
            "Customer_Id": F("channel_id"),
            "User_Session_Id": F("session_id"),
            "Channel": F("channel"),
            "Message": F("message"),
            "Intent": F("intent"),
            "Handled": F("handled"),
            "Score": Cast(F("score"), output_field=FloatField()),
            "Source": F("source"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def returning_user_in_bot_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    result = (
        get_qs.filter(source__in=["user", "llm"])
        .filter(
            message__isnull=False,
        )
        .values("channel_id")
        .annotate(
            visits=Count("session_id", distinct=True),
            Customer=F("channel_id"),
            Channel=F("channel"),
            Time=Max(
                Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            ),
        )
        .filter(visits__gt=1)
        .values("Customer", "Channel", "Time")
        .order_by("-Time")
    )
    return result, ["Customer", "Channel", "Time"], "Return_user_in_BOT"


def user_flow_shankey_chart_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, UserFlow, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    values = (
        qs.values("target", "rank")
        .annotate(
            Target=Concat("target", Value(" "), F("rank"), output_field=CharField())
        )
        .annotate(value=Count("Target"))
        .distinct()
        .values("Target", "value")
    )
    qs1 = (
        qs.filter(source__isnull=False)
        .values("source", "target", "rank")
        .annotate(
            Source=Concat(
                "source", Value(" "), F("rank") - 1, output_field=CharField()
            ),
            Target=Concat("target", Value(" "), F("rank"), output_field=CharField()),
            Rank=F("rank"),
        )
        .annotate(value=Count("target"))
        .values("Source", "Target", "value")
    )
    response = {"values": values, "links": qs1}
    return response


def user_messages_heatmap_generic(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    date_range = get_date_ranges(
        filter_data.get("timestamp__range")[1],
        filter_data.get("timestamp__range")[0],
        4,
    )
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    qs1 = (
        qs.filter(
            source__in=["user", "llm"],
            message__isnull=False,
        )
        .annotate(date=TruncDate("timestamp", tzinfo=get_timezone()))
        .values("date")
        .annotate(count=Count("date"))
        .values("date", "count")
        .order_by("-date")
    )
    response = {"date_range": date_range, "values": qs1}
    return response
