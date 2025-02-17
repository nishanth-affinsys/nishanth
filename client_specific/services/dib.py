from celery.concurrency import custom
from django.db.models import F, Q, Count, CharField
from django.db.models.functions import Trunc, TruncDate, Cast

from console.models import StageLog, MessageLogDetails, StageLogDetails
from console.serializers import (
    TransactionSerializer,
    MessageLogSessionsSerializer,
    StageLogDetailsSerializer,
)
from main.utils.boiler_plate import query
from main.utils.common_utils import add_args
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.tenant_middleware import get_timezone

change_dict_customer_type = {"etb": "NTB-ETB", "ntb": "ETB-NTB"}

data_net_reg_dict = {
    "etb": "etb subscription,etb unsubscription,NTB-ETB",
    "ntb": "ntb subscription,ntb unsubscription,ETB-NTB",
}

data_yes_subscription_dict = {
    "etb": "etb subscription,NTB-ETB",
    "ntb": "ntb subscription,ETB-NTB",
}

data_no_subscription_dict = {"etb": "etb unsubscription", "ntb": "ntb unsubscription"}


def subscription_new_generic(request):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")

    filters = {
        "stage": "subscription",
        "remarks": "new subscription",
    }
    if customer_type:
        filters["stage_result__in"] = [f"{item} subscription" for item in customer_type]

    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "count": True,
        "distinct": True,
    }
    return params


def subscription_new_details_generic(request, key=None, value=None):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "subscription",
        "remarks": "new subscription",
    }
    if customer_type:
        filters["stage_result__in"] = [f"{key} subscription" for key in customer_type]
    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
    }
    return add_args(params, key, value)


def unsubscription_new_generic(request):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "unsubscription",
        "remarks__in": ["new unsubscription", "unsubscription"],
    }
    if customer_type:
        filters["stage_result__in"] = [f"{item} unsubscription" for item in customer_type]
    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "count": True,
        "distinct": True,
    }
    return params


def unsubscription_new_details_generic(request, key=None, value=None):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "unsubscription",
        "remarks__in": ["new unsubscription", "unsubscription"],
    }
    if customer_type:
        filters["stage_result__in"] = [f"{item} unsubscription" for item in customer_type]

    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Remarks": F("remarks"),
        },
    }
    return add_args(params, key, value)


def resubscription_generic(request):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "resubscription",
        "remarks": "resubscription",
    }
    if customer_type:
        filters["stage_result__in"] = [f"{item} subscription" for item in customer_type]

    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "count": True,
        "distinct": True,
    }
    return params


def resubscription_details_generic(request, key=None, value=None):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "resubscription",
        "remarks": "resubscription",
    }
    if customer_type:
        filters["stage_result__in"] = [f"{key} subscription" for key in customer_type]

    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
    }
    return add_args(params, key, value)


def subscription_etb_change_generic(request):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "subscription",
        "remarks__in": ["already existing customer", "new customer"],
    }
    if customer_type:
        filters["stage_result__in"] = [
            change_dict_customer_type[item] for item in customer_type
        ]

    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "count": True,
        "distinct": True,
    }
    return params


def subscription_etb_change_details(request, key=None, value=None):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    filters = {
        "stage": "subscription",
        "remarks__in": ["already existing customer", "new customer"],
    }
    if customer_type:
        filters["stage_result__in"] = [
            change_dict_customer_type[item] for item in customer_type
        ]
    params = {
        "request": request,
        "models": StageLog,
        "serializers": TransactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": filters,
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Remarks": F("remarks"),
        },
    }
    return add_args(params, key, value)


def net_subscription_generic(request):
    customer_type = request.data.get("customer_type")
    filter_data = request.data
    dynamic_db_connection("analytics")
    if customer_type is None:
        customer_type = ["etb", "ntb"]
    queryset = (
        StageLog.objects.using(get_db_name("analytics"))
        .filter(
            timestamp__range=filter_data.get("timestamp__range"),
            stage_result__in=[
                value
                for item in customer_type
                for value in data_net_reg_dict[item].split(",")
            ],
        )
        .values(
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(
            Subscriptions=Count(
                1,
                filter=(
                    Q(
                        stage_result__in=[
                            value
                            for item in customer_type
                            for value in data_yes_subscription_dict[item].split(",")
                        ]
                    )
                ),
            ),
            Unsubscriptions=Count(
                1,
                filter=(
                    Q(
                        stage_result__in=[
                            value
                            for item in customer_type
                            for value in data_no_subscription_dict[item].split(",")
                        ]
                    )
                ),
            ),
        )
        .values("Date", "Subscriptions", "Unsubscriptions")
    )
    return (
        queryset,
        ["Date", "Subscriptions", "Unsubscriptions"],
        "Net Subscriptions Activity ",
    )


def subscription_messages_wordcloud(request):
    customer_type = request.data.get("customer_type")
    dynamic_db_connection("analytics")
    if customer_type is None:
        customer_type = ["etb", "ntb"]
    qs = query(
        request,
        MessageLogDetails,
        MessageLogSessionsSerializer,
        db_schema=get_db_name("analytics"),
    )
    items = (
        qs.filter(source="user", message__isnull=False, customer_type__in=customer_type)
        .annotate(Message=Cast("message", output_field=CharField()))
        .values("Message")
        .annotate(count=Count("Message"))
        .order_by("-count")
    )
    items = [{"name": item["Message"], "count": item["count"]} for item in items]
    return items


def distinct_open_account_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"source": "user", "intent": "applyAccount"},
        "count": True,
        "distinct": True,
    }
    return params


def distinct_open_account_details(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"source": "user", "intent": "applyAccount"},
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Intent": F("intent"),
            "Customer_type": F("customer_type"),
            "Message": F("message"),
            "Channel": F("channel"),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def subscription_leads_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"source": "user", "intent": "lead"},
        "values_kwargs": {
            "Channel_id": F("channel_id"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Intent": F("intent"),
            "Customer_type": F("customer_type"),
            "Message": F("message"),
        },
        "distinct": True,
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def subscription_check_status(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    qs = (
        StageLogDetails.objects.using(get_db_name("analytics")).
        filter(**filter_data)
        .count()
    )
    return qs
