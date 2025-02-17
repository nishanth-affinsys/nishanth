import pytz
from django.db.models import (
    Count,
    Value,
    Case,
    When,
    DateTimeField,
    CharField,
)
from django.db.models import F
from django.db.models.functions import Cast, Trunc

from clickstream.models import (
    ClickstreamIpinformation,
    ClickstreamRecord,
    ClickstreamDevice,
)
from clickstream.serializers import (
    ClickStreamIpInformationSerializer,
    ClickStreamRecordSerializer,
    ClickStreamDeviceSerializer,
)
from main import settings
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import (
    query,
    get_generic_response,
)


def ip_information_generic(request):
    params = {
        "request": request,
        "models": ClickstreamIpinformation,
        "serializers": ClickStreamIpInformationSerializer,
        "db_schema": "clickstream",
        "values_kwargs": {
            "IP_address": F("ip_address"),
            "user_id": F("record__user_identifier__browser_id"),
            "session_id": F("record__session_id"),
            "Continent": F("continent"),
            "Country": F("country"),
            "Region": F("region"),
            "City": F("city"),
            "Location": F("location"),
        },
        "distinct_args": ["session_id"],
        "annotate": {
            "timestamp": Trunc(F("record__timestamp"), "second", tzinfo=get_timezone())
        },
        "query_set": True,
        "order_by": ["session_id", "timestamp"],
    }
    qs = get_generic_response(params)
    qs = sorted(list(qs), key=lambda x: x["timestamp"], reverse=True)
    return (
        qs,
        [
            "IP_address",
            "user_id",
            "session_id",
            "Continent",
            "Country",
            "Region",
            "City",
            "Location",
            "timestamp",
        ],
        "ip_information",
    )


def total_sessions_on_website_generic(request):
    params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "values": ["session_id"],
        "distinct": True,
        "count": True,
    }
    return params


def total_users_on_website_generic(request):
    params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "values": ["user_identifier__browser_id"],
        "distinct": True,
        "count": True,
    }
    return params


def location_based_visits_details_generic(request):
    qs = query(
        request,
        ClickstreamIpinformation,
        ClickStreamIpInformationSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values("country", "city")
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count("city"))
        .values("country", "city", "count")
        .order_by("-count")
    )
    return qs1


def device_based_visits_generic(request):
    qs = query(
        request,
        ClickstreamDevice,
        ClickStreamDeviceSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values("device_type")
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count("device_type"))
        .values("device_type", "count")
        .order_by("-count")
    )
    return qs1


def user_country_geo_generic(request):
    qs = query(
        request,
        ClickstreamIpinformation,
        ClickStreamIpInformationSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values(
            name=Case(
                When(country="United States", then=Value("United States of America")),
                default=F("country"),
            )
        )
        .filter(id__in=list(get_distinct_id))
        .annotate(value=Count("country"))
        .values("name", "value")
    )
    return qs1


def user_country_funnel_generic(request):
    qs = query(
        request,
        ClickstreamIpinformation,
        ClickStreamIpInformationSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values(label=F("country"))
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count("country"))
        .values("label", "count")
        .order_by("count")
    )
    if len(qs1) > 0:
        response = []
        length = 100 / len(qs1)
        position = 1
        display = []
        value = []
        for i in qs1:
            name = i.get("label")
            count = i.get("count")
            size = position * length
            if count in display:
                data = {
                    "name": name,
                    "display": count,
                    "value": value[display.index(count)],
                }
                position += 1
                response.append(data)
            else:
                data = {"name": name, "display": count, "value": size}
                position += 1
                display.append(count)
                value.append(size)
                response.append(data)
        return response
    else:
        return qs1
