from django.db.models import F, Q, Count, CharField
from django.db.models.functions import Trunc, TruncDate, Cast

from console.models import MessageLogDetails
from console.serializers import MessageLogSessionsSerializer
from main.utils.common_utils import add_args
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.tenant_middleware import get_timezone


def leads_generated_count(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"intent": "lead", "source": "user"},
        "distinct": True,
        "count": True,
    }
    return params


def leads_generated_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"intent": "lead", "source": "user"},
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Message": F("message"),
            "Intent": F("intent"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Customer_type": F("customer_type"),
        },
    }
    return add_args(params, key, value)
