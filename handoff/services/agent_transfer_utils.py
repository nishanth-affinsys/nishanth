from django.db.models import (
    Count,
    Q,
    F,
)
from django.db.models.functions import Trunc, TruncDate
from main.utils.boiler_plate import query
from handoff.serializers import AgentReportSerializer
from main.tenant_middleware import get_current_tenant_name, get_timezone
from handoff.models import AnalyticsSocialevent, AgentTransfer
from main.utils.common_utils import custom_filters


def total_transfer_initiated_bigno_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-from",
        },
        "exclude": {"parent_session_id": ""},
        "count": True,
    }
    return params


def total_successful_transfer_bigno_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-to",
        },
        "exclude": {"parent_session_id": ""},
        "count": True,
    }
    return params


def total_failed_transfer_bigno_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-fail",
        },
        "exclude": {"parent_session_id": ""},
        "count": True,
    }
    return params


def transfers_initiated_linechart_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-from",
        },
        "exclude": {"parent_session_id": ""},
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {"transfers_initiated": Count("event")},
        "order_by": ["Date"],
        "not_paginated": True,
    }
    return params


def transfers_accepted_linechart_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-to",
        },
        "exclude": {"parent_session_id": ""},
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {"transfers_accepted": Count("event")},
        "order_by": ["Date"],
        "not_paginated": True,
    }
    return params


def transfers_failed_linechart_generic(request):
    params = {
        "request": request,
        "models": AnalyticsSocialevent,
        "serializers": AgentReportSerializer,
        "db_schema": "handoff",
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "event": "handoff-transfer-fail",
        },
        "exclude": {"parent_session_id": ""},
        "values_kwargs": {"Date": TruncDate("timestamp", tzinfo=get_timezone())},
        "annotate": {"transfers_failed": Count("event")},
        "order_by": ["Date"],
        "not_paginated": True,
    }
    return params


def agent_initiated_transfers_generic(request):
    qs = query(
        request, AnalyticsSocialevent, AgentReportSerializer, db_schema="handoff"
    )
    items = (
        qs.filter(tenant=get_current_tenant_name())
        .filter(event="handoff-transfer-from")
        .exclude(parent_session_id="")
        .values(Agent_Name=F("agent__username"))
        .annotate(count=Count("event"))
        .values("Agent_Name", "count")
    )
    return items


def transfer_details_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "initial_time__range", "channel__in", None)
    values = {
        "Initialized_time": Trunc(F("initial_time"), "second", tzinfo=get_timezone()),
        "Total_session_time": F("total_session"),
    }

    qs = (
        AgentTransfer.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .exclude(initial_agent__icontains="{}")
        .exclude(initial_agent__isnull=True)
        .values(
            Username=F("username"),
            Parent_Session_Id=F("parent_session_id"),
            Initial_Agent=F("initial_agent"),
            Agents_Transferred=F("transferred_agents"),
            Channel=F("channel"),
            **values,
        )
        .order_by("-Initialized_time")
    )
    return (
        qs,
        [
            "Username",
            "Parent_Session_Id",
            "Initial_Agent",
            "Agents_Transferred",
            "Channel",
            "Initialized_time",
            "Total_session_time",
        ],
        "handoff_duration",
    )


def only_transfer_details_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "initial_time__range", "channel__in", None)
    values = {
        "Initialized_time": Trunc(F("initial_time"), "second", tzinfo=get_timezone()),
        "Accept_time": Trunc(F("accept_time"), "second", tzinfo=get_timezone()),
        "Total_session_time": F("total_session"),
    }

    qs = (
        AgentTransfer.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .exclude(
            Q(initial_agent__icontains="{}") | Q(transferred_agents__icontains="{}")
        )
        .exclude(Q(transferred_agents__isnull=True) | Q(initial_agent__isnull=True))
        .values(
            Username=F("username"),
            Parent_Session_Id=F("parent_session_id"),
            Initial_Agent=F("initial_agent"),
            Agents_Transferred=F("transferred_agents"),
            Channel=F("channel"),
            **values,
        )
        .order_by("-Initialized_time")
    )
    return (
        qs,
        [
            "Username",
            "Parent_Session_Id",
            "Initial_Agent",
            "Agents_Transferred",
            "Channel",
            "Initialized_time",
            "Accept_time",
            "Total_session_time",
        ],
        "Agent_transfer_details",
    )
