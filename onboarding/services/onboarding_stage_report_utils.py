from django.db.models import (
    Count,
    Value,
    Case,
    When,
    F,
    CharField,
)
from django.db.models.functions import Trunc

from main.settings import ENABLE_BRANCH_FILTER
from main.tenant_middleware import get_timezone
from onboarding.serializers import OnboardingSerializer
from client_specific.models import KycAccountOpeningDetails
from onboarding.models import SingleCifRetailData, SingleCifSpData
from main.utils.boiler_plate import query
from onboarding.services.onboarding_detailed_report_utils import (
    add_args,
    add_customer_or_business_name,
    get_branch_wise_users_data,
)
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

# constants
in_progress = "In Progress"
pending_verification = "Pending Verification"
pending_approval = "Pending Approval"


def started_flow_generic(request, model_name, onboarding_channel):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QAMEND",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
                "QDISCARD",
                "QEXCEPTION",
            ],
            "onboarding_channel": onboarding_channel,
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def started_flow_self_rt_generic(request):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": SingleCifRetailData,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QTEMP",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
                "QDISCARD",
                "QEXCEPTION",
                "QAMEND",
                "QBANKINGASSURANCE",
                "QDAYTWOFAIL",
                "QDAYTWOPASS",
                "QDAYTWOREJECT",
                "QDAYTWOREMEDIATED"
            ],
            "onboarding_channel": "Self",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def staff_started_flow_rt_generic(request):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": SingleCifRetailData,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QAMEND",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
                "QEXCEPTION",
            ],
            "onboarding_channel": "Staff",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def started_flow_self_sp_generic(request):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": SingleCifSpData,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QTEMP",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
                "QDISCARD",
            ],
            "onboarding_channel": "Self",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def staff_started_flow_sp_generic(request):
    params = {
        "request": request,
        "models": SingleCifSpData,
        "serializers": OnboardingSerializer,
        "db_schema": "onboarding",
        "filter_kwargs": {
            "queue_code__in": [
                "QAMEND",
                "QVERIFY",
                "QAPPROVE",
                "QSUCCESS",
                "QREJECT",
            ],
            "onboarding_channel": "Staff",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def cif_created_generic(request, model_name, onboarding_channel):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QSUCCESS",
            "onboarding_channel": onboarding_channel,
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def cif_failed_generic(request, model_name, onboarding_channel):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QREJECT",
            "onboarding_channel": onboarding_channel,
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def successful_cif_details_generic(
        request, model_name, onboarding_channel, key=None, value=None
):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QSUCCESS",
            "onboarding_channel": onboarding_channel,
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Account_number_1": F("account_num1"),
            "Account_number_2": F("account_num2"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Created_timestamp"],
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params, SingleCifRetailData, SingleCifSpData, model_name, 1
    )
    return add_args(params, key, value)


def failed_cif_details_generic(
        request, model_name, onboarding_channel, key=None, value=None
):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QREJECT",
            "onboarding_channel": onboarding_channel,
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Rejected_by": F("rejected_by"),
            "Rejected_timestamp": Trunc(
                F("rejected_timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Created_timestamp"],
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params, SingleCifRetailData, SingleCifSpData, model_name, 1
    )
    return add_args(params, key, value)


def self_discarded_generic(request, model_name, onboarding_channel):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QDISCARD",
            "onboarding_channel": onboarding_channel,
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def self_discarded_details_generic(request, model_name, key=None, value=None):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QDISCARD",
            "onboarding_channel": "Self",
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
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
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params, SingleCifRetailData, SingleCifSpData, model_name, 1
    )
    return add_args(params, key, value)


def applications_with_maker_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": ["QAMEND", "QTEMP"],
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def applications_with_verifier_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QVERIFY",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def applications_with_approvers_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QAPPROVE",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def applications_processed_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QSUCCESS",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def applications_rejected_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QREJECT",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def applications_exceptions_bigno_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QEXCEPTION",
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def overall_application_stages_sp_stacked_generic(request):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifSpData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items1 = (
        qs1.filter(onboarding_channel="Agent")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Agent=Count(F("labels")))
        .values("labels", "Agent")
        .exclude(labels__isnull=True)
    )

    items2 = (
        qs1.filter(onboarding_channel="Staff")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Staff=Count(F("labels")))
        .values("labels", "Staff")
        .exclude(labels__isnull=True)
    )

    items3 = (
        qs1.filter(onboarding_channel="Self")
        .annotate(
            labels=Case(
                When(queue_code="QTEMP", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Self=Count(F("labels")))
        .values("labels", "Self")
        .exclude(labels__isnull=True)
    )

    labels = [
        in_progress,
        pending_verification,
        pending_approval,
        "Successful",
        "Rejected",
    ]
    response = []

    for label in labels:
        items1_data = items1.filter(labels=label)
        items2_data = items2.filter(labels=label)
        items3_data = items3.filter(labels=label)
        data = {
            "labels": label,
            "Agent": items1_data[0].get("Agent") if len(items1_data) > 0 else 0,
            "Staff": items2_data[0].get("Staff") if len(items2_data) > 0 else 0,
            "Self": items3_data[0].get("Self") if len(items3_data) > 0 else 0,
        }
        response.append(data)

    return response


def overall_application_stages_rt_stacked_generic(request):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifRetailData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items1 = (
        qs1.filter(onboarding_channel="Agent")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Agent=Count(F("labels")))
        .values("labels", "Agent")
        .exclude(labels__isnull=True)
    )

    items2 = (
        qs1.filter(onboarding_channel="Staff")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Staff=Count(F("labels")))
        .values("labels", "Staff")
        .exclude(labels__isnull=True)
    )

    items3 = (
        qs1.filter(onboarding_channel="Self")
        .annotate(
            labels=Case(
                When(queue_code="QTEMP", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
            )
        )
        .values("queue_code", "labels")
        .annotate(Self=Count(F("labels")))
        .values("labels", "Self")
        .exclude(labels__isnull=True)
    )

    labels = [
        in_progress,
        pending_verification,
        pending_approval,
        "Successful",
        "Rejected",
        "Exceptions",
    ]
    response = []

    for label in labels:
        items1_data = items1.filter(labels=label)
        items2_data = items2.filter(labels=label)
        items3_data = items3.filter(labels=label)
        data = {
            "labels": label,
            "Agent": items1_data[0].get("Agent") if len(items1_data) > 0 else 0,
            "Staff": items2_data[0].get("Staff") if len(items2_data) > 0 else 0,
            "Self": items3_data[0].get("Self") if len(items3_data) > 0 else 0,
        }
        response.append(data)

    return response


def queuecodes_pie_rt_generic(request, onboarding_channel):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifRetailData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items = (
        qs1.filter(onboarding_channel=onboarding_channel)
        .filter(
            queue_code__in=[
                "QAMEND",
                "QVERIFY",
                "QSUCCESS",
                "QAPPROVE",
                "QREJECT",
                "QEXCEPTION",
            ]
        )
        .values("queue_code")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("queue_code", "label")
        .annotate(count=Count("labels"))
        .values("label", "count")
        .order_by("-count")
    )
    return items


def self_queuecodes_pie_rt_generic(request):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifRetailData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items = (
        qs1.filter(onboarding_channel="Self")
        .filter(
            queue_code__in=[
                "QTEMP",
                "QVERIFY",
                "QSUCCESS",
                "QAPPROVE",
                "QREJECT",
                "QEXCEPTION",
                "QDISCARD",
                "QAMEND",
                "QBANKINGASSURANCE",
                "QDAYTWOFAIL",
                "QDAYTWOPASS",
                "QDAYTWOREMEDIATED",
                "QDAYTWOREJECT"
            ]
        )
        .values("queue_code")
        .annotate(
            labels=Case(
                When(queue_code__in=["QTEMP", "QAMEND"], then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QDISCARD", then=Value("Abandoned")),
                When(queue_code="QEXCEPTION", then=Value("Exceptions")),
                When(queue_code="QBANKINGASSURANCE", then=Value("Banking Assurance")),
                When(queue_code="QDAYTWOFAIL", then=Value("Day Two Fail")),
                When(queue_code="QDAYTWOPASS", then=Value("Day Two Pass")),
                When(queue_code="QDAYTWOREMEDIATED", then=Value("Day Two Remediated")),
                When(queue_code="QDAYTWOREJECT", then=Value("Day Two Reject")),
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("label")
        .annotate(count=Count("label"))
        .order_by("-count")
    )
    return items


def queuecodes_pie_sp_generic(request, onboarding_channel):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifSpData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items = (
        qs1.filter(onboarding_channel=onboarding_channel)
        .filter(queue_code__in=["QAMEND", "QVERIFY", "QSUCCESS", "QAPPROVE", "QREJECT"])
        .values("queue_code")
        .annotate(
            labels=Case(
                When(queue_code="QAMEND", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("queue_code", "label")
        .annotate(count=Count("labels"))
        .values("label", "count")
        .order_by("-count")
    )
    return items


def self_queuecodes_pie_sp_generic(request):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, SingleCifSpData, OnboardingSerializer, get_db_name("onboarding")
    )
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        qs1 = qs1.filter(created_at_branch_code__in=branch_list)
    items = (
        qs1.filter(onboarding_channel="Self")
        .filter(
            queue_code__in=[
                "QTEMP",
                "QVERIFY",
                "QSUCCESS",
                "QAPPROVE",
                "QREJECT",
                "QDISCARD",
            ]
        )
        .values("queue_code")
        .annotate(
            labels=Case(
                When(queue_code="QTEMP", then=Value(in_progress)),
                When(queue_code="QVERIFY", then=Value(pending_verification)),
                When(queue_code="QAPPROVE", then=Value(pending_approval)),
                When(queue_code="QSUCCESS", then=Value("Successful")),
                When(queue_code="QREJECT", then=Value("Rejected")),
                When(queue_code="QDISCARD", then=Value("Abandoned")),
            )
        )
        .annotate(label=F("labels"))
        .exclude(labels__isnull=True)
        .values("queue_code", "label")
        .annotate(count=Count("labels"))
        .values("label", "count")
        .order_by("-count")
    )
    return items


def kyc_account_opening_details_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": KycAccountOpeningDetails,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "Kyc_reference": F("kyc_reference"),
            "Application_Reference_Number": F("application_reference_number"),
            "Mobile_Number": F("primary_contact_number"),
            "Email": F("primary_email_address"),
            "First_Name": F("first_name"),
            "Last_Name": F("last_name"),
            "Kyc_state": F("kyc_state"),
            "Account_opening_status": F("account_opening_status"),
            "Create_timestamp": Trunc(F("create_timestamp"), "second", tzinfo=get_timezone()),
            "Last_modified_timestamp": Trunc(F("last_modified_timestamp"), "second", tzinfo=get_timezone()),
        }
    }
    return add_args(params, key, value)
