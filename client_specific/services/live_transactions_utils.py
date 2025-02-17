from datetime import date, time, timedelta, datetime
from django.db.models.functions import Substr, Concat, Length
from django.db.models import (
    Value,
    Q,
    Max,
    Case,
    When,
    IntegerField,
    F,
    CharField,
)

from console.models import StageLog, ApiLog
from console.serializers import TransactionSerializer, ApiLogsSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.utils.boiler_plate import query


def api_login_services(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(
            Customer=Concat(
                Substr("channel_id", 1, 5, output_field=CharField()),
                Value("XXXX"),
                Substr(
                    "channel_id",
                    Length("channel_id", output_field=CharField()) - 1,
                    2,
                    output_field=CharField(),
                ),
                output_field=CharField(),
            ),
            Time=F("timestamp")
        )
        .filter(
            stage="Final Response",
            stage_result__in=["CIF Found Successful", "CIF Not Found Unsuccessful"],
            Time__gt=datetime.now() - timedelta(minutes=60),
        )
        .values("Customer", "transaction_id", "transaction_intent", "stage_result", "Time")
    )
    items2 = (
        qs.annotate(
            Customer=Concat(
                Substr("channel_id", 1, 5, output_field=CharField()),
                Value("XXXX"),
                Substr(
                    "channel_id",
                    Length("channel_id", output_field=CharField()) - 1,
                    2,
                    output_field=CharField(),
                ),
                output_field=CharField(),
            ),
            Time=F("timestamp")
        )
        .filter(
            stage="Final Response",
            stage_result="System Aborted",
            remarks="Get Customer Information API Failed",
            Time__gt=datetime.now() - timedelta(minutes=60),
        )
        .values("Customer", "transaction_id", "transaction_intent", "stage_result", "Time")
    )
    response = items.union(items2).order_by("-Time")

    return (
        response,
        [
            "Customer",
            "transaction_id",
            "transaction_intent",
            "stage_result",
            "Time"
        ],
        "Api-login"
    )


def successful_transaction_generic(request):
    dynamic_db_connection("analytics")
    qs = query(request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics"))

    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60),
        )
        .filter(Q(stage_result="Goal Completed") | Q(stage_result="Success"))
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    items1 = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            stage_result__in=["Goal Not Completed", "Unsuccessful Transaction"],
            Time__gt=datetime.now() - timedelta(minutes=60),
        )
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    response = items + items1
    return response


def successful_transaction_goal_completed_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60)
        ).filter(Q(stage_result="Goal Completed") | Q(stage_result="Success"))
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    return items


def successful_transaction_goal_not_completed(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60),
            stage_result__in=["Goal Not Completed", "Unsuccessful Transaction"]
        )
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    return items


def failed_transaction(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60),
            stage_result__in=["User Aborted", "System Aborted"]
        )
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    return items


def system_aborted(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60),
            stage_result="System Aborted"
        )
        .exclude(transaction_intent="welcome")
        .values("transaction_id")
        .distinct()
        .count()
    )
    return items


def user_aborted(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(Time=F("timestamp"))
        .filter(
            stage="Final Response",
            Time__gt=datetime.now() - timedelta(minutes=60),
            stage_result="User Aborted"
        )
        .exclude(transaction_intent="welcome")
        .distinct()
        .count()
    )
    return items


# def detailed_report(request):
#     dynamic_db_connection("analytics")
#     qs = query(
#         request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
#     )
#     items = (
#         qs.annotate(Time=F("timestamp"))
#         .filter(
#             stage="Final Response",
#             stage_result__in=[
#                 "System Aborted",
#                 "User Aborted",
#                 "Goal Completed",
#                 "Goal Not Completed",
#                 "Unsuccessful Transaction",
#             ],
#             Time__gt=datetime.now() - timedelta(minutes=60),
#         )
#         .exclude(transaction_intent="welcome")
#         .annotate(
#             Stage_result=Case(
#                 When(
#                     stage_result__in=[
#                         "Goal Not Completed",
#                         "Unsuccessful Transaction",
#                     ],
#                     then=Value("Goal Not Completed"),
#                 ),
#                 default=F("stage_result"),
#             ),
#             Intent_Used=Case(
#                 When(transaction_intent="suggestion", then=Value("IPO")),
#                 default=F("transaction_intent"),
#             ),
#         )
#         .values("Stage_result", "stage_response", "transaction_id", "Intent_Used")
#     )
#     api_log_qs = query(
#         request, ApiLog, ApiLogsSerializer, db_schema=get_db_name("analytics")
#     )
#     api_items = (
#         api_log_qs
#         .annotate(Time=F("timestamp"))
#         .filter(
#             stage="Response",
#             Time__gt=datetime.now() - timedelta(minutes=60),
#         )
#         .values("api", "internal_reference", "channel_id", "request_id")
#         .annotate(Time=Max("Time"))
#         .order_by("-Time")
#     )
#     response = []
#     for i in items:
#         for j in api_items:
#             if i["transaction_id"] == j["internal_reference"]:
#                 values = {
#                     "customer": j["channel_id"],
#                     "bb_txn_reference": j["internal_reference"],
#                     "stage_result": i["stage_result"],
#                     "stage_response": i["stage_response"],
#                     "api": j["api"],
#                     "request_id": j["request_id"],
#                     "timestamp": j["Time"],
#                     "Intent_Used": i["Intent_Used"],
#                 }
#                 response.append(values)
#     return (
#         response,
#         [
#             "customer", "bb_txn_reference", "stage_result", "stage_response", "api", "request_id", "timestamp",
#             "Intent_Used"
#         ],
#         "Detailed_report"
#     )


def detail_report_new_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLog, TransactionSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.annotate(
            Time=F("timestamp"),
            Customer=Concat(
                Substr("channel_id", 1, 5, output_field=CharField()),
                Value("XXXXX"),
                Substr(
                    "channel_id",
                    Length("channel_id", output_field=IntegerField()) - 1,
                    2,
                    output_field=CharField(),
                ),
                output_field=CharField(),
            )
        )
        .filter(
            Time__gt=datetime.now() - timedelta(minutes=60),
            stage="Final Response",
            stage_result__in=[
                "System Aborted",
                "User Aborted",
                "Goal Completed",
                "Goal Not Completed",
                "Unsuccessful Transaction",
            ],
        ).exclude(transaction_intent="welcome")
        .annotate(
            Stage_result=Case(
                When(
                    stage_result__in=[
                        "Goal Not Completed",
                        "Unsuccessful Transaction",
                    ],
                    then=Value("Goal Not Completed"),
                ),
                default=F("stage_result"),
            ),
            Intent_Used=Case(
                When(transaction_intent="suggestion", then=Value("IPO")),
                default=F("transaction_intent"),
            ),
        )
        .values(
            "Customer",
            "transaction_id",
            "Stage_result",
            "remarks",
            "Intent_Used",
        ).annotate(Time=Max("Time"))
    )
    return (items, ["Customer", "transaction_id", "Stage_result", "remarks", "Intent_Used"], "Detailed Report")
