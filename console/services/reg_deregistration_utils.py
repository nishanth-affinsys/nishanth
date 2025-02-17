from main import settings
import pytz
from django.db.models import Count, CharField, F, Q, Value, When, Case
from django.db.models.functions import TruncDate
from django.db.models import Max
from main.tenant_middleware import get_timezone, get_current_tenant_name
from console.models import EtbUserDetails, EtbUserDetailsOracle, StageLogAuth
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

tz_info = pytz.timezone(settings.TIME_ZONE)


def net_registration_activity_generic(request):
    filter_data = request.data
    dynamic_db_connection("analytics")
    stage_log_fs = (
        StageLogAuth.objects.using(get_db_name("analytics"))
        .filter(Q(action="register") | Q(action="deregister"))
        .filter(
            tenant=get_current_tenant_name(),
            timestamp__range=filter_data.get("timestamp__range"),
        )
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Registrations=Count(1, filter=Q(action="register")),
            DeRegistrations=Count(1, filter=Q(action="deregister")),
        )
        .values("Date", "Registrations", "DeRegistrations")
    )

    return (
        stage_log_fs,
        ["Date", "Registrations", "DeRegistrations"],
        "net_registration_activities",
    )


def number_of_registrations_bigno_generic(request, status):
    filter_data = request.data
    if "postgres" in settings.DB_ENGINE:
        items = list(
            EtbUserDetails.objects.using("etbprovider")
            .filter(is_active=status)
            .values_list("mobile_number", flat=True)
        )
    else:
        items = list(
            EtbUserDetailsOracle.objects.using("etbprovider")
            .filter(is_active=int(status))
            .values_list("mobile_number", flat=True)
        )
    stage_log_fs = (
        StageLogAuth.objects.using("analytics")
        .filter(
            tenant=get_current_tenant_name(),
            timestamp__range=filter_data.get("timestamp__range"),
            mobile_number__in=items,
        )
        .values("mobile_number", "action")
        .annotate(timestamp=Max("timestamp"))
        .values("mobile_number", "timestamp", "action")
        .filter(action="register" if status else "deregister")
        .count()
    )
    return stage_log_fs


def number_of_registrations_list_generic(request, status):
    filter_data = request.data
    if "postres" in settings.DB_ENGINE:
        items = (
            EtbUserDetails.objects.using("etbprovider")
            .filter(is_active=status, account_number__isnull=False)
            .values("mobile_number", "account_number")
        )
    else:
        items = list(
            EtbUserDetails.objects.using("etbprovider")
            .filter(is_active=int(status), account_number__isnull=False)
            .values("mobile_number", "account_number")
        )
    mobile_number_qs = [item["mobile_number"] for item in items]
    stage_log_fs = (
        StageLogAuth.objects.using("analytics")
        .filter(
            tenant=get_current_tenant_name(),
            timestamp__range=filter_data.get("timestamp__range"),
            mobile_number__in=mobile_number_qs,
        )
        .values("mobile_number", "action")
        .annotate(timestamp=Max("timestamp"))
        .values("mobile_number", "timestamp", "action")
        .filter(action="register" if status else "deregister")
    )
    etb_dict = {item["mobile_number"]: item["account_number"] for item in items}
    result = []
    for log_item in stage_log_fs:
        mobile_number = log_item["mobile_number"]
        if mobile_number in etb_dict:
            result.append(
                {
                    "mobile_number": mobile_number,
                    "account_number": etb_dict[mobile_number],
                    "timestamp": log_item["timestamp"],
                }
            )

    return (
        result,
        ["mobile_number", "account_number", "timestamp"],
        "registrations_list",
    )
