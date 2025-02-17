from django.conf import settings

import pytz

from django.db.models import Count, DateTimeField, CharField, F
from django.db.models.functions import Cast, Trunc

from console.models import ApiLogDetails
from console.serializers import ApiLogDetailSerializer

from main.tenant_middleware import get_current_tenant_name, get_timezone

from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def api_calls_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ApiLogDetails,
        "serializers": ApiLogDetailSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {"API": F("api")},
        "annotate": {"count": Count("api")},
        "order_by": ["-count"],
    }
    return add_args(params, key, value)


def api_details_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ApiLogDetails,
        "serializers": ApiLogDetailSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "Internal_reference": F("internal_reference"),
            "API": F("api"),
            "Stage": F("stage"),
            "Status": F("status"),
            "Endpoint": F("endpoint"),
            "Channel": F("channel"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone())
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def api_exceptions_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ApiLogDetails,
        "serializers": ApiLogDetailSerializer,
        "db_schema": get_db_name("analytics"),
        "exclude": {"exception__isnull": True},
        "values_kwargs": {
            "Internal_reference": F("internal_reference"),
            "API": F("api"),
            "Stage": F("stage"),
            "Status": F("status"),
            "Exception": F("exception"),
            "Details": F("data"),
            "Channel": F("channel"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone())
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def api_stage_details_generic(request, stage, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ApiLogDetails,
        "serializers": ApiLogDetailSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"stage": stage},
        "values_kwargs": {
            "Internal_reference": F("internal_reference"),
            "API": F("api"),
            "Endpoint": F("endpoint"),
            "Status": F("status"),
            "Details": F("data"),
            "Request_Id": F("request_id"),
            "Session_Id": F("session_id"),
            "Channel_Id": F("channel_id"),
            "Channel": F("channel"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone())
        },
        "order_by": ["-Timestamp"],
    }
    if stage == "Response":
        params["values_kwargs"]["Exception"] = F("exception")
    params["values_kwargs"]["External_reference"] = F("external_reference")
    return add_args(params, key, value)
