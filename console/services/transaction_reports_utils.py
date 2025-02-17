from collections import defaultdict

from django.db.models import (
    Q,
    F,
    Count,
)
from django.db.models.functions import Trunc, TruncDate

from console.models import StageLogDetails, MessageLog
from console.serializers import StageLogDetailsSerializer

from main.utils.boiler_plate import get_generic_response, query
from main.tenant_middleware import get_timezone
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

# constants
final_response = "Final Response"
goal_completed = "Goal Completed"
goal_not_completed = "Goal Not Completed"
user_aborted = "User Aborted"
system_aborted = "System Aborted"


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def get_intent_details(request):
    dynamic_db_connection("analytics")
    queryset = (
        MessageLog.objects.using(get_db_name("analytics"))
        .values_list("intent", flat=True).distinct()
    )
    items = [{"display_value": item, "api_value": item} for item in queryset]
    return items


def get_customer(request):
    response = [
        {
            "display_value": "ETB",
            "api_value": "etb"
        },
        {
            "display_value": "NTB",
            "api_value": "ntb"
        }
    ]
    return response


def successful_transaction_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": goal_completed,
        },
        "count": True,
        "distinct": True,
        "query_set": True,
    }
    params1 = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": goal_not_completed,
        },
        "count": True,
        "distinct": True,
        "query_set": True,
    }
    s = get_generic_response(params)
    s1 = get_generic_response(params1)
    add = s + s1
    return add


def successful_transaction_goal_completed_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": goal_completed,
        },
        "count": True,
        "distinct": True,
    }
    return params


def successful_transaction_goal_not_completed_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": goal_not_completed,
        },
        "count": True,
        "distinct": True,
    }
    return params


def failed_transaction_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": user_aborted,
        },
        "count": True,
        "distinct": True,
        "query_set": True,
    }
    params1 = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": system_aborted,
        },
        "count": True,
        "distinct": True,
        "query_set": True,
    }
    s = get_generic_response(params)
    s1 = get_generic_response(params1)
    add = s + s1
    return add


def system_aborted_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": system_aborted,
        },
        "count": True,
        "distinct": True,
    }
    return params


def user_aborted_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
            "stage_result": user_aborted,
        },
        "count": True,
        "distinct": True,
    }
    return params


def total_api_calls_faq_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "distinct": True,
        "count": True,
    }
    return params


def total_api_calls_trans_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "exclude": {"stage": "Initiate Agent handoff"},
        "distinct": True,
        "count": True,
    }
    return params


def transaction_report_details_generic(request, stage1, stage2, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": StageLogDetails,
        "serializers": StageLogDetailsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "stage": final_response,
        },
        "filter_args": [Q(stage_result=stage1) | Q(stage_result=stage2)],
        "values_kwargs": {
            "Customer_id": F("channel_id"),
            "Transaction_id": F("transaction_id"),
            "Transaction_intent": F("transaction_intent"),
            "Stage": F("stage"),
            "Stage_result": F("stage_result"),
            "Channel": F("channel"),
            "Details": F("details"),
            "Remarks": F("remarks"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)


def transactions_linechart_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request, StageLogDetails, StageLogDetailsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        get_qs.filter(stage="Final Response")
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Successfull_transactions=Count(
                1,
                filter=Q(stage_result__in=[goal_completed, goal_not_completed]),
            ),
            Failed_transactions=Count(
                1, filter=Q(stage_result__in=[user_aborted, system_aborted])
            ),
        )
        .order_by("-Date")
    )
    return items


def transaction_partition_generic(request, stage1, stage2):
    get_qs = query(
        request, StageLogDetails, StageLogDetailsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        get_qs.filter(stage=final_response)
        .filter(Q(stage_result=stage1) | Q(stage_result=stage2))
        .values("stage_result", "transaction_intent")
        .annotate(value=Count("transaction_intent"))
    )

    grouped_data = {}
    for item in items:
        stage_result = item["stage_result"]
        transaction_intent = item["transaction_intent"]
        value = item["value"]

        if stage_result not in grouped_data:
            grouped_data[stage_result] = {
                "name": stage_result,
                "value": 0,
                "children": [],
            }

        grouped_data[stage_result]["value"] += value
        grouped_data[stage_result]["children"].append(
            {"name": transaction_intent, "value": value, "children": []}
        )

    sunburst_data = {"level": 2, "value": list(grouped_data.values())}
    return sunburst_data


def all_transaction_breakdown_generic(request):
    dynamic_db_connection("analytics")
    get_qs = query(
        request, StageLogDetails, StageLogDetailsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        get_qs.filter(stage=final_response)
        .values("stage_result")
        .annotate(value=Count("stage_result"))
    )

    category_entries = defaultdict(lambda: {"name": "", "value": 0, "children": []})

    sunburst_data = {"level": 2, "value": []}
    category_mapping = {
        goal_completed: "Successful Transactions",
        goal_not_completed: "Successful Transactions",
        user_aborted: "Failed Transactions",
        system_aborted: "Failed Transactions",
    }

    for item in items:
        stage_result = item["stage_result"]
        value = item["value"]

        category = category_mapping.get(stage_result, " ")

        category_entry = category_entries[category]
        category_entry["name"] = category
        category_entry["value"] += value
        category_entry["children"].append(
            {"name": stage_result, "value": value, "children": []}
        )

    sunburst_data["value"] = list(category_entries.values())

    return sunburst_data
