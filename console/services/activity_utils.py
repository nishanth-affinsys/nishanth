from django.db.models import (
    F,
)
from django.db.models.functions import Trunc

from console.models import Activity, StageLogAuth
from console.serializers import ActivitySerializer, AuditLogSerializer
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def complete_activity_details_generic(request):
    if get_current_tenant_name() != "default":
        dynamic_db_connection("analytics")
        params = {
            "request": request,
            "models": Activity,
            "serializers": ActivitySerializer,
            "db_schema": get_db_name("analytics"),
            "filter_kwargs": {
                "username__isnull": False,
            },
            "annotate": {
                "request_timestamp": Trunc(
                    F("request_timestamp"), "second", tzinfo=get_timezone()
                ),
                "timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            },
            "order_by": ["-timestamp"],
        }
        return params
    else:
        params = {
            "request": request,
            "models": Activity,
            "serializers": ActivitySerializer,
            "db_schema": "analytics",
            "filter_kwargs": {
                "tenant": get_current_tenant_name(),
                "username__isnull": False,
            },
            "annotate": {
                "request_timestamp": Trunc(
                    F("request_timestamp"), "second", tzinfo=get_timezone()
                ),
                "timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            },
            "order_by": ["-timestamp"],
        }
        return params


def audit_log_details_generic(request):
    if get_current_tenant_name() != "default":
        dynamic_db_connection("analytics")
        provider = request.user.provider
        params = {
            "request": request,
            "models": StageLogAuth,
            "serializers": AuditLogSerializer,
            "db_schema": get_db_name("analytics"),
            "filter_kwargs": {"provider": provider},
            "values": [
                "user_id",
                "user_name",
                "action",
                "result",
                "result_detail",
                "ip_info",
                "payload",
            ],
            "annotate": {
                "timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            },
            "order_by": ["-timestamp"],
        }
        return params
    else:
        params = {
            "request": request,
            "models": Activity,
            "serializers": ActivitySerializer,
            "db_schema": "analytics",
            "filter_kwargs": {
                "tenant": get_current_tenant_name(),
                "username__isnull": False,
            },
            "annotate": {
                "request_timestamp": Trunc(
                    F("request_timestamp"), "second", tzinfo=get_timezone()
                ),
                "timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            },
            "order_by": ["-timestamp"],
        }
        return params
