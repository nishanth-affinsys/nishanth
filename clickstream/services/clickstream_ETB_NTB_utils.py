import pytz
from django.db.models import (
    Value,
    F,
    Sum,
    DateTimeField,
    CharField,
    Q,
)
from django.db.models.functions import Cast, Trunc, Coalesce

from main.tenant_middleware import get_current_tenant_name, get_timezone
from main import settings
from clickstream.models import (
    ClickstreamRecord,
    ClickstreamIpinformation,
    ClickstreamDevice,
    ClickstreamAction,
    ClickstreamBrowser,
)
from clickstream.serializers import (
    ClickStreamRecordSerializer,
    ClickStreamIpInformationSerializer,
    ClickStreamDeviceSerializer,
    ClickStreamBrowserSerializer,
)

from main.utils.boiler_plate import (
    query,
    get_generic_response,
)


def number_of_etb_cust_generic(request):
    params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "exclude": {"user_identifier__user_id": F("user_identifier__browser_id")},
        "distinct_args": ["session_id"],
        "count": True,
    }
    return params


def number_of_ntb_cust_generic(request):
    params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "filter_kwargs": {"user_identifier__user_id": F("user_identifier__browser_id")},
        "distinct_args": ["session_id"],
        "count": True,
    }
    return params


def etb_cust_per_ntb_cust_generic(request):
    etb_params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "exclude": {"user_identifier__user_id": F("user_identifier__browser_id")},
        "distinct_args": ["session_id"],
        "query_set": True,
        "count": True,
    }
    ntb_params = {
        "request": request,
        "models": ClickstreamRecord,
        "serializers": ClickStreamRecordSerializer,
        "db_schema": "clickstream",
        "filter_kwargs": {"user_identifier__user_id": F("user_identifier__browser_id")},
        "distinct_args": ["session_id"],
        "query_set": True,
        "count": True,
    }
    etb_res = get_generic_response(etb_params)
    ntb_res = get_generic_response(ntb_params)
    return etb_res, ntb_res


def uservice_ipinformation_details_generic(request, user_type):
    params = {
        "request": request,
        "models": ClickstreamIpinformation,
        "serializers": ClickStreamIpInformationSerializer,
        "db_schema": "clickstream",
        "exclude": {
            "record__user_identifier__user_id": F("record__user_identifier__browser_id")
        },
        "values": [
            "ip_address",
            "continent",
            "country",
            "city",
            "region",
            "location",
        ],
        "values_kwargs": {
            "user_id": F("record__user_identifier__user_id"),
            "session_id": F("record__session_id"),
        },
        "distinct_args": ["session_id"],
        "annotate": {
            "timestamp": Trunc(F("record__timestamp"), "second", tzinfo=get_timezone())
        },
        "query_set": True,
        "order_by": ["session_id", "timestamp"],
    }
    if user_type == "NTB":
        params["filter_kwargs"] = {
            "record__user_identifier__user_id": F("record__user_identifier__browser_id")
        }
    elif user_type == "ETB":
        params["exclude"] = {
            "record__user_identifier__user_id": F("record__user_identifier__browser_id")
        }

    qs = get_generic_response(params)
    qs = sorted(list(qs), key=lambda x: x["timestamp"], reverse=True)
    return (
        qs,
        [
            "ip_address",
            "continent",
            "country",
            "city",
            "region",
            "location",
            "timestamp",
            "user_id",
            "session_id",
        ],
        "ip_information",
    )


def uservice_device_details_generic(request, user_type):
    params = {
        "request": request,
        "models": ClickstreamDevice,
        "serializers": ClickStreamDeviceSerializer,
        "db_schema": "clickstream",
        "values": [
            "device_type",
            "device_brand",
            "device_model",
            "device_os_name",
            "device_price_range",
        ],
        "values_kwargs": {
            "user_id": F("record__user_identifier__user_id"),
            "session_id": F("record__session_id"),
        },
        "distinct_args": ["session_id"],
        "annotate": {
            "timestamp": Trunc(F("record__timestamp"), "second", tzinfo=get_timezone())
        },
        "query_set": True,
        "order_by": ["session_id", "timestamp"],
    }
    if user_type == "NTB":
        params["filter_kwargs"] = {
            "record__user_identifier__user_id": F(
                "record__user_identifier__browser_id"
            ),
        }
    elif user_type == "ETB":
        params["exclude"] = {
            "record__user_identifier__user_id": F(
                "record__user_identifier__browser_id"
            ),
        }
    qs = get_generic_response(params)
    qs = sorted(list(qs), key=lambda x: x["timestamp"], reverse=True)
    return (
        qs,
        [
            "device_type",
            "device_brand",
            "device_model",
            "device_os_name",
            "device_price_range",
            "timestamp",
            "user_id",
            "session_id",
        ],
        "uservice_device_ETB",
    )


def uservice_browser_details_generic(request, user_type):
    params = {
        "request": request,
        "models": ClickstreamBrowser,
        "serializers": ClickStreamBrowserSerializer,
        "db_schema": "clickstream",
        "values": ["browser_family", "browser_type", "browser_name", "language"],
        "values_kwargs": {
            "user_id": F("record__user_identifier__user_id"),
            "session_id": F("record__session_id"),
        },
        "distinct_args": ["session_id"],
        "annotate": {
            "timestamp": Trunc(F("record__timestamp"), "second", tzinfo=get_timezone())
        },
        "query_set": True,
        "order_by": ["session_id", "timestamp"],
    }
    if user_type == "ETB":
        params["exclude"] = {
            "record__user_identifier__user_id": F(
                "record__user_identifier__browser_id"
            ),
        }
    elif user_type == "NTB":
        params["filter_kwargs"] = {
            "record__user_identifier__user_id": F(
                "record__user_identifier__browser_id"
            ),
        }
    qs = get_generic_response(params)
    qs = sorted(list(qs), key=lambda x: x["timestamp"], reverse=True)

    return (
        qs,
        [
            "device_type",
            "device_brand",
            "device_model",
            "device_os_name",
            "device_price_range",
            "timestamp",
            "user_id",
            "session_id",
        ],
        "uservice_device_details",
    )


def clickstream_complete_user_details_generic(request, user_type):
    qs = query(
        request,
        ClickstreamRecord,
        ClickStreamRecordSerializer,
        db_schema="clickstream",
    )
    qs1 = None
    if user_type == "NTB":
        qs1 = (
            qs.filter(user_identifier__user_id=F("user_identifier__browser_id"))
            .values(
                "id", "session_id", "timestamp", user_id=F("user_identifier__user_id")
            )
            .distinct("session_id")
        )
    elif user_type == "ETB":
        qs1 = (
            qs.exclude(user_identifier__user_id=F("user_identifier__browser_id"))
            .values(
                "id", "session_id", "timestamp", user_id=F("user_identifier__user_id")
            )
            .distinct("session_id")
        )
    response = []
    for i in qs1:
        ip_info = (
            ClickstreamIpinformation.objects.using("clickstream")
            .filter(record_id=i.get("id"))
            .values("ip_address", "continent", "country", "city")
        )
        device_info = (
            ClickstreamDevice.objects.using("clickstream")
            .filter(record_id=i.get("id"))
            .values("device_type", "device_os_name")
        )
        browser_info = (
            ClickstreamBrowser.objects.using("clickstream")
            .filter(record_id=i.get("id"))
            .values("browser_name")
        )
        if ip_info and device_info and browser_info:
            data = {
                "user_id": i.get("user_id"),
                "session_id": i.get("session_id"),
                "IP_address": ip_info[0].get("ip_address") if len(ip_info) > 0 else "",
                "continent": ip_info[0].get("continent") if len(ip_info) > 0 else "",
                "country": ip_info[0].get("country") if len(ip_info) > 0 else "",
                "city": ip_info[0].get("city") if len(ip_info) > 0 else "",
                "device_type": (
                    device_info[0].get("device_type") if len(device_info) > 0 else ""
                ),
                "device_os_name": (
                    device_info[0].get("device_os_name") if len(device_info) > 0 else ""
                ),
                "browser_name": (
                    browser_info[0].get("browser_name") if len(browser_info) > 0 else ""
                ),
                "timestamp": i.get("timestamp").strftime("%Y-%m-%d %H:%M:%S"),
            }
            response.append(data)
            response.sort(key=lambda x: x["timestamp"], reverse=True)
    return (
        response,
        [
            "user_id",
            "session_id",
            "IP_address",
            "continent",
            "country",
            "city",
            "device_type",
            "device_os_name",
            "browser_name",
            "timestamp",
        ],
        "complete_user_details",
    )


def uservice_clicks_count_generic(request, user_type):
    qs = query(
        request,
        ClickstreamRecord,
        ClickStreamRecordSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = None
    if user_type == "ETB":
        get_distinct_id = (
            qs.exclude(user_identifier__user_id=F("user_identifier__browser_id"))
            .distinct("session_id")
            .values_list("id", flat=True)
        )
    elif user_type == "NTB":
        get_distinct_id = (
            qs.filter(user_identifier__user_id=F("user_identifier__browser_id"))
            .distinct("session_id")
            .values_list("id", flat=True)
        )

    qs1 = (
        ClickstreamAction.objects.using("clickstream")
        .filter(record_id__in=list(get_distinct_id))
        .values(
            user_id=F("record_id__user_identifier__user_id"),
            session_id=F("record_id__session_id"),
        )
        .annotate(count=Coalesce(Sum(1, filter=Q(action_type="click")), Value(0)))
        .order_by("-count")
    )
    return qs1, ["user_id", "session_id", "count"], "clicks_count_ETB"
