import pytz
from django.db.models import (
    Count,
    Value,
    Case,
    When,
    F,
    DateTimeField,
    CharField,
)
from django.db.models.functions import Cast, Concat, Trunc

from main import settings
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from onboarding.models import KycMaster
from onboarding.serializers import OnboardingSerializer
from onboarding.services.onboarding_detailed_report_utils import add_args
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def kyc_total_applications_self_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "channel": "Self",
            "queue_code__in": [
                "QTEMP",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
                "QDISCARD",
                "QEXCEPTION",
                "QREAPPLYEDIT",
                "QREAPPLY",
                "QAMEND",
                "QVISITBRANCH",
            ],
        },
        "values": ["internal_reference"],
        "count": True,
        "distinct": True,
    }
    return params


def kyc_total_applications_staff_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "channel": "Staff",
            "queue_code__in": [
                "QAMEND",
                "QVERIFY",
                "QSUCCESS",
                "QAPPROVE",
                "QREJECT",
                "QEXCEPTION",
                "QDISCARD",
            ],
        },
        "values": ["internal_reference"],
        "count": True,
        "distinct": True,
    }
    return params


def self_queuecodes_pie_kyc_generic(request):
    dynamic_db_connection("kyc")
    qs1 = query(request, KycMaster, OnboardingSerializer, get_db_name("kyc"))
    items = (
        qs1.filter(channel="Self")
        .filter(
            queue_code__in=[
                "QTEMP",
                "QAMEND",
                "QAPPROVE",
                "QEXCEPTION",
                "QSUCCESS",
                "QDISCARD",
                "QREJECT",
                "QVERIFY",
                "QVISITBRANCH",
                "QREAPPLY",
                "QREAPPLYEDIT"                
            ]
        )
        .annotate(
            labels=Case(
                When(queue_code="QTEMP", then=Value("In Progress")),
                When(queue_code="QAPPROVE", then=Value("Pending Approval")),
                When(queue_code="QVERIFY", then=Value("Pending Verification")),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QDISCARD", then=Value("Discarded")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
                When(queue_code="QREAPPLY", then=Value("Reapply")),
                When(queue_code="QREAPPLYEDIT", then=Value("Reapply")),
                When(queue_code="QVISITBRANCH", then=Value("Visit branch")),
                When(queue_code="QAMEND", then=Value("In Progress"))
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("label")
        .annotate(count=Count("labels"))
        .order_by("-count")
    )
    return items


def queuecodes_pie_kyc_generic(request, channel):
    dynamic_db_connection("kyc")
    qs1 = query(request, KycMaster, OnboardingSerializer, get_db_name("kyc"))
    items = (
        qs1.filter(channel=channel)
        .filter(
            queue_code__in=[
                "QAMEND",
                "QVERIFY",
                "QSUCCESS",
                "QAPPROVE",
                "QREJECT",
                "QEXCEPTION",
                "QDISCARD",
            ]
        )
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value("In Progress")),
                When(queue_code="QVERIFY", then=Value("Pending Verification")),
                When(queue_code="QAPPROVE", then=Value("Pending Approval")),
                When(queue_code="QDISCARD", then=Value("Discarded")),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("label")
        .annotate(count=Count("labels"))
        .order_by("-count")
    )
    return items


def kyc_discarded_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QDISCARD",
        },
        "values": ["internal_reference"],
        "count": True,
    }
    return params


def kyc_discarded_details_generic(request, key=None, value=None):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QDISCARD",
        },
        "values_kwargs": {
            "Kyc_reference": F("internal_reference"),
            "KYC_number": F("kyc_number"),
            "Customer_name": Concat(
                F("first_name"),
                Value(" "),
                F("middle_name"),
                Value(" "),
                F("last_name"),
            ),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Channel": F("channel"),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Abandoned_by": F("discarded_by"),
            "Abandoned_timestamp": Trunc(
                F("discarded_timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Created_timestamp"],
    }
    return add_args(params, key, value)
