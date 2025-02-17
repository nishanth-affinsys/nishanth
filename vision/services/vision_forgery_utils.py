from __future__ import annotations

from itertools import groupby
from operator import itemgetter

import pytz
from django.db.models import Count, Q, F, Window
from django.db.models.functions import Trunc, TruncDate, RowNumber

from main import settings
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from vision.models import StageLogForgery
from vision.serializers import VisionForgerySerializer

from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def add_row_number(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, StageLogForgery, VisionForgerySerializer, get_db_name("analytics")
    )
    qs1 = (
        qs.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=["session_id"],
                order_by=["-timestamp"],
            )
        )
        .filter(row_number=1)
        .values()
    )
    return qs1


def forgery_check_big_no(request, status):
    data = add_row_number(request)
    condition = lambda row: row.get("status", "") in status
    response = filter(condition, data)
    count = len(list(response))
    return {"count": count}


def successful_vs_failed_trendline_forgery_generic(request):
    items = (
        add_row_number(request)
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Genuine=Count(
                1,
                filter=Q(status="Success"),
            ),
            Forged=Count(1, filter=Q(status="User Error")),
            System_error=Count(1, filter=Q(status="System Error")),
        )
        .order_by("-Date")
    )
    response = []
    date_getter = itemgetter("Date")
    grouped_data = {}

    for date, group in groupby(items, key=date_getter):
        group_list = list(group)
        date_data = {
            "Date": date,
            "Genuine": sum(item["Genuine"] for item in group_list),
            "Forged": sum(item["Forged"] for item in group_list),
            "System_error": sum(item["System_error"] for item in group_list),
        }
        grouped_data[date] = date_data
    response = list(grouped_data.values())
    return response, ["Date", "Genuine", "Forged", "System_error"], "aggregate_analysis"


def forgery_details_generic(request, status):
    qs1 = add_row_number(request).values(
        Application_number=F("external_reference"),
        Session_id=F("session_id"),
        Status=F("status"),
        Remark=F("remark"),
        Document_class=F("document_class"),
        Prediction_score=F("prediction_score"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    response = []
    for data in qs1:
        if data.get("Status", "") in status:
            response.append(data)
    return (
        response,
        [
            "Application_number",
            "Session_id",
            "Status",
            "Remark",
            "Document_class",
            "Prediction_score",
            "Timestamp",
        ],
        "forgery_detections",
    )


# system error = api failed
def system_error_forgery_details_generic(request):
    qs1 = add_row_number(request).values(
        Application_number=F("external_reference"),
        Session_id=F("session_id"),
        Status=F("status"),
        Remark=F("remark"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    response = []
    for data in qs1:
        if data.get("Status", "") in ["System Error"]:
            response.append(data)
    return (
        response,
        [
            "Application_number",
            "Session_id",
            "Status",
            "Remark",
            "Timestamp",
        ],
        "forgery_detections",
    )
