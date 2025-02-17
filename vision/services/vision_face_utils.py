from __future__ import annotations

from itertools import groupby
from operator import itemgetter

from django.db.models import (
    Count,
    Q,
    F,
    Case,
    When,
    CharField,
    Value,
    Window,
    FloatField,
)
from django.db.models.functions import Trunc, TruncDate, RowNumber

from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import (
    query,
)
from vision.models import StageLogFace
from vision.serializers import VisionFaceSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def add_row_number(request):
    dynamic_db_connection("analytics")
    qs = query(request, StageLogFace, VisionFaceSerializer, get_db_name("analytics"))
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


def face_stage_bigno_generic(request, status):
    data = add_row_number(request)
    condition = lambda row: row.get("status", "") in status
    response = filter(condition, data)
    count = len(list(response))
    return {"count": count}


def success_face_stage_bigno_generic(request, remark):
    data = add_row_number(request)
    condition = (
        lambda row: row.get("remark", "") in remark and row.get("status") == "Success"
    )
    response = filter(condition, data)
    count = len(list(response))
    return {"count": count}


def successful_vs_failed_trendline_face_generic(request):
    items = (
        add_row_number(request)
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Successful=Count(
                1,
                filter=Q(status="Success"),
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


def face_success_details_generic(request):
    qs1 = add_row_number(request).values(
        Application_number=F("external_reference"),
        Session_id=F("session_id"),
        Status=F("status"),
        Action=Case(
            When(action="info", then=Value("Detection")),
            When(action="verify", then=Value("Verification")),
            output_field=CharField(),
        ),
        Remark=F("remark"),
        Score=Case(
            When(action="info", then=F("face_detection_score")),
            When(action="verify", then=F("face_verification_score")),
            output_field=FloatField(),
        ),
        Threshold=Case(
            When(action="info", then=F("face_detection_threshold")),
            When(action="verify", then=F("face_verification_threshold")),
            output_field=FloatField(),
        ),
        Image_quality=F("image_quality_final"),
        Gender=F("gender"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    response = []
    for data in qs1:
        if data.get("Status", "") in ["Success"]:
            response.append(data)
    return (
        response,
        [
            "Application_number",
            "Session_id",
            "Status",
            "Action",
            "Remark",
            "Score",
            "Threshold",
            "Image_quality",
            "Gender",
            "Timestamp",
        ],
        "successful_recognitions",
    )


def face_failed_details_generic(request):
    qs1 = add_row_number(request).values(
        Application_number=F("external_reference"),
        Session_id=F("session_id"),
        Status=F("status"),
        Remark=F("remark"),
        Action=Case(
            When(action="info", then=Value("Detection")),
            When(action="verify", then=Value("Verification")),
            output_field=CharField(),
        ),
        Detection_score=F("face_detection_score"),
        Detection_threshold=F("face_detection_threshold"),
        Verification_score=F("face_verification_score"),
        Verification_threshold=F("face_verification_threshold"),
        Image_quality=F("image_quality_final"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    response = []
    for data in qs1:
        if data.get("Status", "") in ["User Error", "System Error"]:
            response.append(data)
    return (
        response,
        [
            "Application_number",
            "Session_id",
            "Status",
            "Remark",
            "Action",
            "Detection_score",
            "Detection_threshold",
            "Verification_score",
            "Verification_threshold",
            "Image_quality",
            "Timestamp",
        ],
        "failed_recognitions",
    )
