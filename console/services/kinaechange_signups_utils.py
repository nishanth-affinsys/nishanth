from console.models import StageLogAuth
from console.serializers import AuditLogSerializer
from main.utils.boiler_plate import query
from onboarding.models import SingleCifRetailData
from onboarding.serializers import OnboardingSerializer
from django.db.models.functions import Trunc
from django.db.models import F
from main.tenant_middleware import get_timezone


def users_signups_generic(request, result_type, bigno):
    qs2 = query(
        request, SingleCifRetailData, OnboardingSerializer, db_schema="onboarding"
    )
    user_id_lists = list(
        qs2.filter(queue_code="QSUCCESS")
        .values_list("created_by_uuid", flat=True)
        .distinct()
    )
    qs = query(request, StageLogAuth, AuditLogSerializer, db_schema="analytics")
    qs = qs.filter(user_id__in=user_id_lists, action=result_type).values(
        User_id=F("user_id"),
        User_name=F("user_name"),
        Mobile_number=F("mobile_number"),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    if bigno:
        return qs.distinct("user_id").count(), "", ""

    else:
        return (
            qs,
            ["user_id", "user_name", "mobile_number", "timestamp"],
            "Successfully Onboarded Applications",
        )
