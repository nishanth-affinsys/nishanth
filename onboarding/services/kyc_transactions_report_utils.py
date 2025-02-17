import pytz
from django.db.models import Case, When, Value, F, DateTimeField, CharField
from django.db.models.functions import Cast, Concat, Trunc
from rest_framework.decorators import action

from main import settings
from main.settings import db_engine_oracle
from main.tenant_middleware import get_current_tenant_name, get_timezone
from onboarding.models import KycMaster
from onboarding.serializers import OnboardingSerializer, KycApplicationSerializer
from onboarding.services.onboarding_detailed_report_utils import add_args
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from client_specific.models import KycApplicationsDetails


def kyc_onboarding_success_bigno_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QSUCCESS",
        },
        "values": ["kyc_number"],
        "count": True,
        "distinct": True
    }
    return params


def kyc_failed_bigno_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QREJECT",
        },
        "values": ["kyc_number"],
        "count": True,
        "distinct": True,
    }
    return params


def kyc_exceptions_big_no_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QEXCEPTION",
        },
        "values": ["kyc_number"],
        "count": True,
        "distinct": True,
    }
    return params


def kyc_transaction_details_report_generic(request, queue_code, key=None, value=None):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": queue_code,
        },
        "values_kwargs": {
            "Internal_reference": F("internal_reference"),
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
        },
    }

    if queue_code == "QSUCCESS":
        params["values_kwargs"]["Approved_by"] = F("submit_by")
        params["values_kwargs"]["Approved_timestamp"] = Trunc(
            F("submit_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Approved_timestamp"]

    elif queue_code == "QREJECT":
        params["values_kwargs"]["Rejected_by"] = F("rejected_by")
        params["values_kwargs"]["Rejected_timestamp"] = Trunc(
            F("rejected_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Rejected_timestamp"]

    elif queue_code == "QEXCEPTION":
        params["values_kwargs"]["Last_modified_by"] = F("last_modified_by")
        params["values_kwargs"]["Last_modified_timestamp"] = Trunc(
            F("last_modified_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Last_modified_timestamp"]

    return add_args(params, key, value)


def kyc_onboarding_details_comments_generic(request, queue_code, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": KycApplicationsDetails,
        "serializers": KycApplicationSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "queue_code": queue_code
        },
        "values_kwargs": {
            "Kyc_reference": F("internal_reference"),
            "Customer_name": F("customer_name"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Channel": F("channel"),
            "Action_code": F("action_code"),
            "Application_status": F("queue_name"),
            "Comments": F("comments"),
            "Last_modified_timestamp": Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            )
        },
    }
    if queue_code == "QSUCCESS":
        params["values_kwargs"]["Approved_by"] = F("submit_by")
        params["values_kwargs"]["Approved_timestamp"] = Trunc(
            F("submit_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Approved_timestamp"]
    elif queue_code == "QREJECT":
        params["values_kwargs"]["Rejected_by"] = F("rejected_by")
        params["values_kwargs"]["Rejected_timestamp"] = Trunc(
            F("rejected_timestamp"), "second", tzinfo=get_timezone()
        )
        params["order_by"] = ["-Rejected_timestamp"]

    return add_args(params, key, value)


def kyc_success_bigno_generic(request):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "queue_code": "QSUCCESS",
        },
        "values": ["kyc_number"],
        "count": True,
        "distinct": True,
    }
    return params
