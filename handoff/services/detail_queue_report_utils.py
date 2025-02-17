from itertools import groupby
from operator import itemgetter

from django.db.models import (
    Count,
    Value,
    Q,
    Max,
    Min,
    Case,
    When,
    F,
    CharField,
    Func,
)
from django.db.models.functions import (
    Extract,
    Trunc,
    TruncDate,
    ExtractHour,
    TruncHour,
)

from console.models import MessageLog
from console.serializers import (
    DailyTrafficSerializer,
)
from console.services.transaction_reports_utils import add_args
from main.utils.common_utils import convert_seconds_to_hhmmss

from handoff.models import (
    AnalyticsSocialevent,
    AbandonedDetails,
)
from handoff.serializers import (
    AgentReportSerializer,
)
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.utils.common_utils import custom_filters


def chatbot_message_interactions_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in")
    qs1 = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            **filters,
        )
        .filter(
            tenant=get_current_tenant_name(),
            event__in=["social-message", "chat-message"],
        )
        .values("channel", message=F("event"))
    )
    dynamic_db_connection("analytics")
    qs2 = (
        MessageLog.objects.using(get_db_name("analytics"))
        .filter(
            **filters,
        )
        .filter(
            source="user",
            tenant=get_current_tenant_name(),
            message__isnull=False,
            session_id__isnull=False,
        )
        .values("channel", "message")
    )
    q = [*qs1, *qs2]

    q = sorted(q, key=itemgetter("channel"))

    response = []
    for key, value in groupby(q, key=itemgetter("channel")):
        usertoagent = 0
        agenttouser = 0
        usertobot = 0
        for k in value:
            if k.get("message") == "social-message":
                usertoagent += 1
            elif k.get("message") == "chat-message":
                agenttouser += 1
            elif (
                k.get("message") not in ["social-message", "chat-message"]
                and k.get("message") is not None
            ):
                usertobot += 1
        data = {
            "Channel": key,
            "Total_messages_user_to_agent": usertoagent,
            "Total_messages_agent_to_user": agenttouser,
            "Total_messages_user_to_bot": usertobot,
        }
        response.append(data)
    return (
        response,
        [
            "Channel",
            "Total_messages_user_to_agent",
            "Total_messages_agent_to_user",
            "Total_messages_user_to_bot",
        ],
        "chatbot_messages_interactions",
    )


def total_session_time_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            **filters,
            tenant=get_current_tenant_name(),
        )
        .filter(
            event__in=[
                "agent-accept",
                "user-end-confirm",
                "agent-force-end",
                "agent-end-confirm",
                "user-inactive",
            ]
        )
        .values(
            "agent__username",
            "session",
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(duration=Max("timestamp") - Min("timestamp"))
        .values("agent__username", "Date", "duration")
        .order_by("-Date")
    )

    qs1 = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            **filters,
            tenant=get_current_tenant_name(),
        )
        .filter(event="agent-accept")
        .values("agent__username", Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .distinct()
        .order_by("-Date")
    )

    response = []
    for i in qs1:
        duration = 0
        for j in qs:
            if j.get("Date") == i.get("Date") and j.get("agent__username") == i.get(
                "agent__username"
            ):
                duration = duration + int(j.get("duration").total_seconds())
        formatted_duration = convert_seconds_to_hhmmss(duration)
        data = {
            "Agent Name": i.get("agent__username"),
            "Date": i.get("Date"),
            "Total Handling time": formatted_duration,
        }
        response.append(data)

    return (
        response,
        ["Agent Name", "Date", "Total Handling time"],
        "Total_handled_time",
    )


def cust_req_for_handoff_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-initial",
        },
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {
            "Hour(00-59minutes)": Extract("timestamp", "hour", tzinfo=get_timezone()),
            "count": Count("session"),
        },
        "order_by": ["-count"],
    }
    return params


def agent_interactions_generic(request):
    qs = query(request, AnalyticsSocialevent, AgentReportSerializer, "handoff")
    qs2 = (
        qs.filter(tenant=get_current_tenant_name(), event="agent-accept")
        .annotate(Date_Hour=TruncHour("timestamp", tzinfo=get_timezone()))
        .values("Date_Hour")
        .annotate(count=Count("session"))
        .annotate(
            Date_and_Hour=Func(
                F("Date_Hour"),
                Value("YYYY-MM-DD HH24"),
                function="TO_CHAR",
                output_field=CharField(),
            )
        )
        .values("Date_and_Hour", "count")
        .order_by("-Date_and_Hour")
    )
    return qs2


def agent_interactions_export_table_generic(request, key=None, value=None):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "agent-accept",
        },
        "values_kwargs": {
            "Date": TruncDate(F("timestamp"), tzinfo=get_timezone()),
            "Hour": ExtractHour(F("timestamp"), tzinfo=get_timezone()),
        },
        "annotate": {"count": Count("session")},
        "order_by": ["-Date", "-Hour"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def bot_interactions_generic(request):
    dynamic_db_connection("analytics")
    qs = query(request, MessageLog, DailyTrafficSerializer, get_db_name("analytics"))
    qs2 = (
        qs.filter(tenant=get_current_tenant_name(), source="user")
        .annotate(Date_Hour=TruncHour("timestamp", tzinfo=get_timezone()))
        .values("Date_Hour")
        .annotate(count=Count("session_id"))
        .annotate(
            Date_and_Hour=Func(
                F("Date_Hour"),
                Value("YYYY-MM-DD HH24"),
                function="TO_CHAR",
                output_field=CharField(),
            )
        )
        .values("Date_and_Hour", "count")
        .order_by("-Date_and_Hour")
    )
    return qs2


def bot_interactions_export_table_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLog,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"tenant": get_current_tenant_name(), "source": "user"},
        "serializers": DailyTrafficSerializer,
        "values_kwargs": {
            "Date": TruncDate(F("timestamp"), tzinfo=get_timezone()),
            "Hour": ExtractHour(F("timestamp"), tzinfo=get_timezone()),
        },
        "annotate": {"count": Count("session_id")},
        "order_by": ["-Date", "-Hour"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


# NewUserInHandoff
def user_in_handoff_generic(request, model_name, timestamp_field):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        model_name.objects.using("handoff")
        .annotate(timestamp=F(timestamp_field))
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .annotate(
            Customer_Id=F("channel_id"),
            Username=F("username"),
            Phone_Number=F("phone_number"),
            Email=F("email"),
            Channel=F("channel"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .values(
            "Customer_Id",
            "Username",
            "Phone_Number",
            "Email",
            "Channel",
            "Timestamp",
        )
        .order_by("-Timestamp")
    )
    return (
        qs,
        [
            "Customer_Id",
            "Username",
            "Phone_Number",
            "Email",
            "Channel",
            "Timestamp",
        ],
        "user_in_handoff",
    )


def abandoned_users_details_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AbandonedDetails.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(Q(event="user-fallout") | Q(event="user-cancel-routing"))
        .exclude(session="")
        .values(
            Customer_name=F("username"),
            Phone_Number=F("phone_number"),
            Email=F("email"),
            Channel=F("channel"),
            Session=F("session"),
        )
        .annotate(
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("-Timestamp")
    )
    return (
        qs,
        [
            "Customer_name",
            "Phone_Number",
            "Email",
            "Channel",
            "Session",
            "Timestamp",
        ],
        "abandoned_chat_details",
    )


def average_session_time_seconds_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(tenant=get_current_tenant_name(), **filters)
        .filter(
            event__in=[
                "agent-accept",
                "user-end-confirm",
                "agent-force-end",
                "agent-end-confirm",
                "user-inactive",
            ]
        )
        .values(
            "agent__username",
            "session",
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(max_val=Max("timestamp"), min_val=Min("timestamp"))
        .annotate(duration=F("max_val") - F("min_val"))
        .values("agent__username", "Date", "duration")
        .order_by("-Date")
    )

    qs1 = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(tenant=get_current_tenant_name(), **filters)
        .filter(event="agent-accept")
        .values("agent__username", Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .distinct()
        .order_by("-Date")
    )
    response = []
    for i in qs1:
        duration = 0
        count = 0
        for j in qs:
            if j.get("Date") == i.get("Date") and j.get("agent__username") == i.get(
                "agent__username"
            ):
                duration = duration + int(j.get("duration").total_seconds())
                count = count + 1
        formatted_duration = (
            convert_seconds_to_hhmmss(duration / count) if count > 0 else "00:00:00"
        )
        data = {
            "Agent Name": i.get("agent__username"),
            "Date": i.get("Date"),
            "Average Handling time": formatted_duration,
        }
        response.append(data)
    return (
        response,
        ["Agent Name", "Date", "Average Handling time"],
        "average_handling_time",
    )


def customer_activity_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    result = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(tenant=get_current_tenant_name(), **filters)
        .filter(event="handoff-initial")
        .values(
            Customer=F("social__username"),
            Skill=F("social__skill"),
            Phone_Number=F("social__phone_number"),
            Email=F("social__email"),
            Channel=F("channel"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("-Timestamp")
    )
    return (
        result,
        ["Customer", "Skill", "Phone_Number", "Email", "Channel", "Timestamp"],
        "customer_activity",
    )


def agent_handoff_details_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    result = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(tenant=get_current_tenant_name(), **filters)
        .filter(event="agent-accept")
        .values(
            Agent_Name=F("agent__username"),
            Customer_Name=F("social__username"),
            Phone_Number=F("social__phone_number"),
            Email=F("social__email"),
            Channel=F("channel"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("-Timestamp")
    )
    return (
        result,
        [
            "Agent_Name",
            "Customer_Name",
            "Phone_Number",
            "Email",
            "Channel",
            "Timestamp",
        ],
        "agent_handoff_details",
    )


def handled_ended_chats_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(
            Q(event="agent-end-confirm")
            | Q(event="user-end-confirm")
            | Q(event="agent-force-end")
            | Q(event="user-inactive")
        )
        .annotate(
            label=Case(
                When(event="agent-end-confirm", then=Value("Agent Ended Chats")),
                When(event="user-end-confirm", then=Value("User Ended Chats")),
                When(event="agent-force-end", then=Value("Agent Deleted Chats")),
                When(event="user-inactive", then=Value("Inactive User")),
                output_field=CharField(),
            )
        )
        .values("event", "label")
        .annotate(count=Count("event"))
        .values("label", "count")
    )
    return qs


def unhandled_chats_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(
            Q(event="agent-out-of-office")
            | Q(event="agent-unavailable")
            | Q(event="user-immediate-cancel")
        )
        .annotate(
            label=Case(
                When(event="agent-out-of-office", then=Value("Agent Out Of Office")),
                When(
                    event="agent-unavailable",
                    then=Value("Agent Unavailable or Busy"),
                ),
                When(
                    event="user-immediate-cancel",
                    then=Value("User Immediate Cancel"),
                ),
                output_field=CharField(),
            )
        )
        .values("event", "label")
        .annotate(count=Count("event"))
        .values("label", "count")
    )
    return qs
