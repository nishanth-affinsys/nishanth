from django.db.models import Case, When, Value, F, DateTimeField, CharField
from django.db.models.functions import Cast, Concat, Trunc

from main.settings import ENABLE_BRANCH_FILTER
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main import settings

import pytz

from onboarding.models import SingleCifRetailData, SingleCifSpData
from onboarding.serializers import OnboardingSerializer
from onboarding.services.onboarding_detailed_report_utils import (
    add_args,
    add_customer_or_business_name,
    get_branch_wise_users_data,
)
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def successful_transaction_generic(request, model_name):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QSUCCESS",
                "QBANKINGASSURANCE",
                "QDAYTWOFAIL",
                "QDAYTWOPASS",
                "QDAYTWOREJECT",
                "QDAYTWOREMEDIATED"
            ],
        },
        "values": ["external_reference"],
        "count": True,
        "distinct": True,
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return params


def failed_transaction_generic(request, model_name):
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


def exception_transaction_generic(request, model_name):
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


# common function for successful details
def successful_transaction_report_generic(request, model_name, key=None, value=None):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                "QSUCCESS",
                "QBANKINGASSURANCE",
                "QDAYTWOFAIL",
                "QDAYTWOPASS",
                "QDAYTWOREJECT",
                "QDAYTWOREMEDIATED"
            ]
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Account_number_1": F("account_num1"),
            "Account_number_2": F("account_num2"),
            "Branch_code": F("created_at_branch_code"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Mode": F("onboarding_channel"),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Approved_timestamp"],
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params, SingleCifRetailData, SingleCifSpData, model_name, 1
    )
    return add_args(params, key, value)


# common function for rejected transactions
def rejected_transactions_report_generic(request, model_name, key=None, value=None):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": "QREJECT",
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Branch_code": F("created_at_branch_code"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Mode": F("onboarding_channel"),
            "Rejected_by": F("rejected_by"),
            "Rejected_timestamp": Trunc(
                F("rejected_timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Rejected_timestamp"],
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params, SingleCifRetailData, SingleCifSpData, model_name, 1
    )
    return add_args(params, key, value)


def discarded_or_exceptions_transaction_rt_generic(
        request, queue_code, key=None, value=None
):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": SingleCifRetailData,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code": queue_code,
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Customer_name": Concat(
                F("first_name"),
                Value(" "),
                F("middle_name"),
                Value(" "),
                F("last_name"),
            ),
            "Branch_code": F("created_at_branch_code"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Mode": F("onboarding_channel"),
        },
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list

    if queue_code == "QDISCARD":
        params["values_kwargs"]["Abandoned_by"] = F("discarded_by")
        params["values_kwargs"]["Abandoned_timestamp"] = Trunc(
            F("discarded_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Abandoned_timestamp"]
    elif queue_code == "QEXCEPTION":
        params["values_kwargs"]["Last_modified_by"] = F("last_modified_by")
        params["values_kwargs"]["Last_modified_timestamp"] = Trunc(
            F("last_modified_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Last_modified_timestamp"]

    return add_args(params, key, value)


def onboarding_remediated_pass_generic(request, key=None, value=None):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": SingleCifRetailData,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "queue_code__in": [
                'QDAYTWOREMEDIATED',
                'QDAYTWOPASS',
                'QDAYTWOFAIL',
                'QBANKINGASSURANCE',
                'QDAYTWOREJECT'
            ]
        },
        "values_kwargs": {
            "Application_Reference_Number": F("internal_reference"),
            "Application_Status": F("queue_name"),
            "Primary_Contact_Number": F("primary_contact_number"),
            "Primary_Email_Address": F("primary_email_address"),
            "Account_Number_1": F("account_num1"),
            "Account_Number_2": F("account_num2"),
            "Last_action_perform_timestamp": Trunc(F("last_action_perform_timestamp"), "second", tzinfo=get_timezone()),
        },
    }
    return add_args(params, key, value)
