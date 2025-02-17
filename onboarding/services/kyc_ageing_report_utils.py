from datetime import datetime

from django.db.models import (
    Q,
    Value,
    F,
    CharField,
)
from django.db.models.functions import Cast, Concat, Trunc

from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from onboarding.models import KycMaster
from onboarding.models import SingleCifRetailData
from main.utils.time_zone_utils import get_business_days
from onboarding.serializers import OnboardingSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def kyc_ageing_report_generic(request):
    dynamic_db_connection("kyc")
    qs = query(request, KycMaster, OnboardingSerializer, get_db_name("kyc"))
    qs1 = (
        qs.filter(tenant=get_current_tenant_name())
        .annotate(
            Kyc_reference=Cast(F("internal_reference"), output_field=CharField()),
            Customer_name=Cast(
                Concat(
                    F("first_name"),
                    Value(" "),
                    F("middle_name"),
                    Value(" "),
                    F("last_name"),
                ),
                output_field=CharField(),
            ),
            Stage=Cast(F("queue_name"), output_field=CharField()),
            Channel=Cast(F("channel"), output_field=CharField()),
            Created_timestamp=Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "Kyc_reference",
            "Customer_name",
            "Stage",
            "Channel",
            "Created_timestamp",
            "create_timestamp",
        )
        .filter(
            Q(queue_code="QVERIFY")
            | Q(queue_code="QEXCEPTION")
            | Q(queue_code="QAPPROVE")
        )
        .order_by("-create_timestamp")
    )
    now = datetime.now(get_timezone())
    result = [
        {
            "Kyc_reference": row.get("Kyc_reference"),
            "Customer_name": row.get("Customer_name"),
            "Stage": row.get("Stage"),
            "Ageing(in days)": str((now - row.get("create_timestamp")).days),
            "Channel": row.get("Channel"),
            "Created_timestamp": row.get("Created_timestamp"),
        }
        for row in qs1
        if (now - row.get("create_timestamp")).days > 0
    ]
    return (
        result,
        [
            "Kyc_reference",
            "Customer_name",
            "Stage",
            "Ageing(in days)",
            "Channel",
            "Created_timestamp",
        ],
        "kyc_ageing_report",
    )


def onboarding_short_kyc_exception_generic(request, days=2):
    dynamic_db_connection("kyc")
    previous_timestamp = get_business_days(days)
    query = (
        KycMaster.objects.using(get_db_name("kyc"))
        .filter(
            last_action_perform_timestamp__isnull=False,
            last_action_perform_timestamp__gte=previous_timestamp,
            queue_code="QEXCEPTION",
        )
        .values(
            Kyc_Reference=F("internal_reference"),
            Last_Action=F("last_action"),
            Last_Action_Performed_By=F("last_action_performed_by"),
            Last_action_perform_timestamp=Trunc(
                F("last_action_perform_timestamp"), "second", tzinfo=get_timezone()
            ),
            Primary_Contact_Number=F("primary_contact_number"),
            Primary_Email_Address=F("primary_email_address"),
            First_Name=F("first_name"),
            Last_Name=F("last_name"),
        )
    )
    return (
        query,
        [
            "Kyc_Reference",
            "Last_Action",
            "Last_Action_Performed_By",
            "Primary_Contact_Number",
            "Primary_Email_Address",
            "First_Name",
            "Last_Name",
            "Last_action_perform_timestamp",
        ],
        "Applications_exception_two_days" if days == 2 else "Applications_exception_five_days",
    )
