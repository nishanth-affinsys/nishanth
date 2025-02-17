from django.db.models import Q, F, Count
from django.db.models.functions import Trunc, TruncDate

from console.services.transaction_reports_utils import add_args
from wallet.models import AccountingMerchant
from wallet.serializers import AccMerchantSerializer

from main.utils.boiler_plate import query, get_generic_response
from main.tenant_middleware import get_timezone
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def wallet_transactions_bigno(request, transaction_type):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": AccountingMerchant,
        "serializers": AccMerchantSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "transaction_status": transaction_type,
        },
        "count": True,
        "distinct": True,
    }
    return params


def wallet_transactions_details(request, transaction_type, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": AccountingMerchant,
        "serializers": AccMerchantSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"transaction_status": transaction_type},
        "values_kwargs": {
            "Transaction_id": F("transaction_id"),
            "Currency": F("currency"),
            "Amount": F("transaction_amount"),
            "Sender": F("sender_name"),
            "Receiver": F("receiver_name"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def wallet_transactions_multilinechart_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request,
        AccountingMerchant,
        AccMerchantSerializer,
        db_schema=get_db_name("analytics"),
    )
    items = (
        get_qs.values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Successful_transactions=Count(1, filter=Q(transaction_status="S")),
            Failed_transactions=Count(1, filter=Q(transaction_status="F")),
        )
        .order_by("-Date")
    )
    return items


def wallet_transactions_percentage(request, transaction_type):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": AccountingMerchant,
        "serializers": AccMerchantSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"transaction_status__in": ["S", "F"]},
        "annotate": {"count": Count("transaction_status")},
        "values": ["transaction_status"],
        "not_paginated": True,
        "query_set": True,
    }
    results = get_generic_response(params)
    total_count = 0
    for item in results:
        total_count += item["count"]
    response = [
        {
            "count": "{0:.3f}".format(item["count"] / total_count),
            "display": f"{'{0:.2f}'.format(item['count'] / total_count * 100)}%",
        }
        for item in results
        if item["transaction_status"] == transaction_type
    ]
    return response[0] if len(response) > 0 else {}
