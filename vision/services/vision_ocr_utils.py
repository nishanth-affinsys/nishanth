from __future__ import annotations

from itertools import groupby
from operator import itemgetter

from django.db.models import Count, Q, F, Window
from django.db.models.functions import Trunc, TruncDate, RowNumber

from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import (
    query,
)
from vision.models import StageLogOcr
from vision.serializers import VisionOCRSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

user_error = "User Error"
system_error = "System Error"


def add_row_number(request):
    dynamic_db_connection("analytics")
    qs = query(request, StageLogOcr, VisionOCRSerializer, get_db_name("analytics"))
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


def ocr_stage_bigno_generic(request, statuses):
    data = add_row_number(request)
    condition = lambda row: row.get("status", "") in statuses
    response = filter(condition, data)
    count = len(list(response))
    return {"count": count}


def successful_vs_failed_trendline_ocr_generic(request):
    items = (
        add_row_number(request)
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Successful=Count(
                1,
                filter=Q(status__in=["Success"]),
            ),
            Failed=Count(1, filter=Q(status__in=["User Error", "System Error"])),
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
            "Successful": sum(item["Successful"] for item in group_list),
            "Failed": sum(item["Failed"] for item in group_list),
        }
        grouped_data[date] = date_data

    response = list(grouped_data.values())

    return response, ["Date", "Successful", "Failed"], "aggregate_analysis"


def detailed_report_ocr_generic(request, statuses):
    qs1 = add_row_number(request).values(
        Application_number=F("external_reference"),
        Session_id=F("session_id"),
        Status=F("status"),
        Remark=F("remark"),
        Image_quality=F("image_quality_final"),
        Image_type=F("image_type_final"),
        Parsing_score=F("parsing_score"),
        Parsing_Threshold=F("parsing_threshold"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    response = []
    for data in qs1:
        if data.get("Status", "") in statuses:
            response.append(data)
    return (
        response,
        [
            "Application_number",
            "Session_id",
            "Status",
            "Remark",
            "Image_quality",
            "Image_type",
            "Parsing_score",
            "Parsing_Threshold",
            "Timestamp",
        ],
        "ocr_recognitions",
    )
