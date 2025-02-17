from django.db.models import (
    Count,
)
from django.db.models import F

from clickstream.models import ClickstreamDevice, ClickstreamBrowser
from clickstream.serializers import (
    ClickStreamDeviceSerializer,
    ClickStreamBrowserSerializer,
)
from main.utils.boiler_plate import (
    query,
)


def device_information_generic(request):
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
    )
    items = qs1.annotate(label=F("device_type")).values("count", "label")
    return items


def sessions_per_device_generic(request):
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
        .annotate(count=Count("record__session_id"))
    )
    items = qs1.annotate(label=F("device_type")).values("count", "label")
    return items


def operating_system_info_generic(request):
    qs = query(
        request,
        ClickstreamDevice,
        ClickStreamDeviceSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values("device_os_name")
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count("device_os_name"))
    )
    items = qs1.annotate(label=F("device_os_name")).values("count", "label")
    return items


def browser_info_generic(request):
    qs = query(
        request,
        ClickstreamBrowser,
        ClickStreamBrowserSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values("browser_name")
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count("browser_name"))
    )
    items = qs1.annotate(label=F("browser_name")).values("count", "label")
    return items
