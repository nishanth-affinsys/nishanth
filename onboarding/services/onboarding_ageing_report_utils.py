from datetime import datetime

from django.db.models import (
    Q,
    Case,
    When,
    Value,
    F,
    CharField,
)
from django.db.models.functions import Cast, Concat, Trunc, TruncDate

from main.settings import ENABLE_BRANCH_FILTER
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import query
from onboarding.models import SingleCifRetailData, SingleCifSpData
from onboarding.serializers import OnboardingSerializer
from onboarding.services.onboarding_detailed_report_utils import (
    get_branch_wise_users_data,
)
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

agent_fields = [
    "Application_number",
    "Application_type",
    "Application_source",
    "Application_status",
    "Agent_email",
    "Ageing(in days)",
    "Branch_code",
    "CIF",
    "Account_number_1",
    "Account_number_2",
    "Customer_type",
    "Created_by",
    "Created_date",
]

staff_self_fields = [
    "Application_number",
    "Application_type",
    "Application_source",
    "Application_status",
    "Ageing(in days)",
    "Branch_code",
    "CIF",
    "Account_number_1",
    "Account_number_2",
    "Customer_type",
    "Created_by",
    "Created_date",
]


def application_ageing_report_rt_generic(request):
    dynamic_db_connection("onboarding")
    qs = query(
        request, SingleCifRetailData, OnboardingSerializer, get_db_name("onboarding")
    )
    qs1 = (
        qs.annotate(
            Application_number=Cast(F("external_reference"), output_field=CharField()),
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
            Mode=Cast(F("onboarding_channel"), output_field=CharField()),
            Application_present_with=Cast(F("role_code"), output_field=CharField()),
            Created_timestamp=Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "Application_number",
            "Customer_name",
            "Stage",
            "Mode",
            "Created_timestamp",
            "Application_present_with",
        )
        .filter(
            Q(queue_code="QVERIFY")
            | Q(queue_code="QEXCEPTION")
            | Q(queue_code="QAPPROVE")
            | Q(queue_code="QBANKINGASSURANCE")
            | Q(queue_code="QDAYTWOFAIL")
        )
        .order_by("-Created_timestamp")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)

    now = datetime.now(get_timezone())
    result = [
        {
            "Application_number": row.get("Application_number"),
            "Customer_name": row.get("Customer_name"),
            "Stage": row.get("Stage"),
            "Ageing(in days)": str((now - row.get("Created_timestamp")).days),
            "Mode": row.get("Mode"),
            "Application_present_with": row.get("Application_present_with"),
            "Created_timestamp": row.get("Created_timestamp"),
        }
        for row in qs1
        if (now - row.get("Created_timestamp")).days > 0
    ]
    return (
        result,
        [
            "Application_number",
            "Customer_name",
            "Stage",
            "Ageing(in days)",
            "Mode",
            "Application_present_with",
            "Created_timestamp",
        ],
        "application_ageing_retail",
    )


def application_ageing_report_sp_generic(request):
    dynamic_db_connection("onboarding")
    qs = query(
        request, SingleCifSpData, OnboardingSerializer, get_db_name("onboarding")
    )
    qs1 = (
        qs.annotate(
            Application_number=Cast(F("external_reference"), output_field=CharField()),
            Business_name=Cast(F("business_name"), output_field=CharField()),
            Stage=Cast(F("queue_name"), output_field=CharField()),
            Mode=Cast(F("onboarding_channel"), output_field=CharField()),
            Application_present_with=Cast(F("role_code"), output_field=CharField()),
            Created_timestamp=Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "Application_number",
            "Business_name",
            "Stage",
            "Mode",
            "Created_timestamp",
            "Application_present_with",
            "create_timestamp",
        )
        .filter(
            Q(queue_code="QVERIFY")
            | Q(queue_code="QEXCEPTION")
            | Q(queue_code="QAPPROVE")
        )
        .order_by("-Created_timestamp")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)

    now = datetime.now(get_timezone())
    result = [
        {
            "Application_number": row.get("Application_number"),
            "Business_name": row.get("Business_name"),
            "Stage": row.get("Stage"),
            "Ageing(in days)": str((now - row.get("Created_timestamp")).days),
            "Mode": row.get("Mode"),
            "Application_present_with": row.get("Application_present_with"),
            "Created_timestamp": row.get("Created_timestamp"),
        }
        for row in qs1
        if (now - row.get("Created_timestamp")).days > 0
    ]
    return (
        result,
        [
            "Application_number",
            "Business_name",
            "Stage",
            "Ageing(in days)",
            "Mode",
            "Application_present_with",
            "Created_timestamp",
        ],
        "application_ageing_sp",
    )


def scheduled_ageing_report_agent_generic(
        request, model_name, app_type_ntb, app_type_etb, cust_type_ntb, cust_type_etb
):
    dynamic_db_connection("onboarding")
    qs = query(request, model_name, OnboardingSerializer, get_db_name("onboarding"))
    qs1 = (
        qs.filter(onboarding_channel="Agent")
        .filter(
            Q(queue_code="QVERIFY")
            | Q(queue_code="QEXCEPTION")
            | Q(queue_code="QAPPROVE")
        )
        .annotate(
            Application_number=Cast(F("external_reference"), output_field=CharField()),
            Application_type=Case(
                When(customer_type="ntb", then=Value(app_type_ntb)),
                When(customer_type="etb", then=Value(app_type_etb)),
                output_field=CharField(),
            ),
            Application_source=Case(
                When(onboarding_channel="Agent", then=Value("AGENT-ASSISTED")),
                output_field=CharField(),
            ),
            Application_status=Case(
                When(queue_code="QVERIFY", then=Value("Pending for Verification")),
                When(queue_code="QAPPROVE", then=Value("Pending for Approval")),
                When(queue_code="QEXCEPTION", then=Value("Pending for review")),
                output_field=CharField(),
            ),
            Agent_email=Cast(F("created_by"), output_field=CharField()),
            Branch_code=Cast(F("created_at_branch_code"), output_field=CharField()),
            CIF=Cast(F("cif"), output_field=CharField()),
            Account_number_1=Cast(F("account_num1"), output_field=CharField()),
            Account_number_2=F("account_num2"),
            Customer_type=Case(
                When(customer_type="ntb", then=Value(cust_type_ntb)),
                When(customer_type="etb", then=Value(cust_type_etb)),
                output_field=CharField(),
            ),
            Created_by=Cast(F("created_by"), output_field=CharField()),
            Application_create_date=TruncDate(
                "create_timestamp", tzinfo=get_timezone()
            ),
            Created_Timestamp=Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "Application_number",
            "Application_type",
            "Application_source",
            "Application_status",
            "Agent_email",
            "Application_create_date",
            "Branch_code",
            "CIF",
            "Account_number_1",
            "Account_number_2",
            "Customer_type",
            "Created_by",
            "Created_Timestamp",
        )
        .order_by("-Created_Timestamp")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)

    now = datetime.now(get_timezone())
    result = [
        {
            "Application_number": row.get("Application_number"),
            "Application_type": row.get("Application_type"),
            "Application_source": row.get("Application_source"),
            "Application_status": row.get("Application_status"),
            "Agent_email": row.get("Agent_email"),
            "Ageing(in days)": str((now - row.get("Created_Timestamp")).days),
            "Branch_code": row.get("Branch_code"),
            "CIF": row.get("CIF"),
            "Account_number_1": row.get("Account_number_1"),
            "Account_number_2": row.get("Account_number_2"),
            "Customer_type": row.get("Customer_type"),
            "Created_by": row.get("Created_by"),
            "Created_date": row.get("Application_create_date"),
        }
        for row in qs1
        if (now - row.get("Created_Timestamp")).days > 0
    ]
    return result, agent_fields


# for self and staff both retail and SP
def scheduled_ageing_report_generic(
        request,
        model_name,
        app_type_ntb,
        app_type_etb,
        cust_type_ntb,
        cust_type_etb,
        channel,
        app_source,
):
    dynamic_db_connection("onboarding")
    qs = query(request, model_name, OnboardingSerializer, get_db_name("onboarding"))
    qs1 = (
        qs.filter(onboarding_channel=channel)
        .filter(
            Q(queue_code="QVERIFY")
            | Q(queue_code="QEXCEPTION")
            | Q(queue_code="QAPPROVE")
            | Q(queue_code="QBANKINGASSURANCE")
            | Q(queue_code="QDAYTWOFAIL")
        )
        .annotate(
            Application_number=Cast(F("external_reference"), output_field=CharField()),
            Application_type=Case(
                When(customer_type="ntb", then=Value(app_type_ntb)),
                When(customer_type="etb", then=Value(app_type_etb)),
                output_field=CharField(),
            ),
            Application_source=Case(
                When(onboarding_channel=channel, then=Value(app_source)),
                output_field=CharField(),
            ),
            Application_status=Case(
                When(queue_code="QVERIFY", then=Value("Pending for Verification")),
                When(queue_code="QAPPROVE", then=Value("Pending for Approval")),
                When(queue_code="QEXCEPTION", then=Value("Pending for review")),
                When(queue_code="QBANKINGASSURANCE", then=Value("Banking Assurance")),
                When(queue_code="QDAYTWOFAIL", then=Value("Day Two Application")),
                output_field=CharField(),
            ),
            Application_create_date=TruncDate(
                "create_timestamp", tzinfo=get_timezone()
            ),
            Branch_code=Cast(F("created_at_branch_code"), output_field=CharField()),
            CIF=Cast(F("cif"), output_field=CharField()),
            Account_number_1=Cast(F("account_num1"), output_field=CharField()),
            Account_number_2=F("account_num2"),
            Customer_type=Case(
                When(customer_type="ntb", then=Value(cust_type_ntb)),
                When(customer_type="etb", then=Value(cust_type_etb)),
                output_field=CharField(),
            ),
            Created_by=Cast(F("created_by"), output_field=CharField()),
            Created_Timestamp=Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "Application_number",
            "Application_type",
            "Application_source",
            "Application_status",
            "Application_create_date",
            "Branch_code",
            "CIF",
            "Account_number_1",
            "Account_number_2",
            "Customer_type",
            "Created_by",
            "Created_Timestamp",
        )
        .order_by("-Created_Timestamp")
    )

    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    now = datetime.now(get_timezone())
    result = [
        {
            "Application_number": row.get("Application_number"),
            "Application_type": row.get("Application_type"),
            "Application_source": row.get("Application_source"),
            "Application_status": row.get("Application_status"),
            "Ageing(in days)": str((now - row.get("Created_Timestamp")).days),
            "Branch_code": row.get("Branch_code"),
            "CIF": row.get("CIF"),
            "Account_number_1": row.get("Account_number_1"),
            "Account_number_2": row.get("Account_number_2"),
            "Customer_type": row.get("Customer_type"),
            "Created_by": row.get("Created_by"),
            "Created_date": row.get("Application_create_date"),
        }
        for row in qs1
        if (now - row.get("Created_Timestamp")).days > 0
    ]
    return result, staff_self_fields
