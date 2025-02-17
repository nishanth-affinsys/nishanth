from django.db.models import F, Window
from django.db.models.functions import Trunc, RowNumber

from console.models import ServiceStatus
from console.serializers import ServiceStatusSerializer

from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import query


def add_row_number(request):
    qs = query(request, ServiceStatus, ServiceStatusSerializer, "analytics")
    qs1 = (
        qs.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=["service"],
                order_by=["-last_modified_timestamp"],
            )
        )
        .filter(row_number=1)
        .values()
    )
    return qs1


# shows service status of each service
def service_status_generic(request):
    qs1 = (
        add_row_number(request)
        .values(
            Service=F("service"),
            Health_Status=F("healthz_status"),
            Live_Status=F("livez_status"),
        )
        .annotate(
            Timestamp=Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            )
        )
        .order_by("Service")
    )
    return (
        qs1,
        ["Service", "Health_Status", "Live_Status", "Timestamp"],
        "service_status",
    )
