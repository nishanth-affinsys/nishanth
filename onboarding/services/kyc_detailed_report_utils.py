import pytz
from django.db.models import (
    Case,
    When,
    Value,
    F,
    CharField,
    DateTimeField,
)
from django.db.models.functions import Cast, Concat, Trunc

from main import settings
from main.tenant_middleware import get_current_tenant_name, get_timezone
from onboarding.models import (
    KycMaster,
)
from client_specific.models import KycApplicationsDetails
from onboarding.serializers import OnboardingSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def kyc_detailed_report_generic(request, key=None, value=None):
    dynamic_db_connection("kyc")
    params = {
        "request": request,
        "models": KycMaster,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("kyc"),
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
        },
        "values_kwargs": {
            "Kyc_reference": F("internal_reference"),
            "Product_name": F("product_name"),
            "Customer_name": Concat(
                F("first_name"),
                Value(" "),
                F("middle_name"),
                Value(" "),
                F("last_name"),
            ),
            "Phone_Number": F("primary_contact_number"),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_action_performed_by": F("last_action_performed_by"),
            "Last_action_perform_timestamp": Trunc(
                F("last_action_perform_timestamp"), "second", tzinfo=get_timezone()),
            "Last_modified_by": F("last_modified_by"),
            "Last_modified_timestamp": Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Application_stage": F("queue_name"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
        },
        "order_by": ["-Created_timestamp"],
    }
    return add_args(params, key, value)


def kyc_onboarding_detailed_report_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": KycApplicationsDetails,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
        },
        "values_kwargs": {
            "Kyc_reference": F("internal_reference"),
            "Product_name": F("product_name"),
            "Customer_name": F("customer_name"),
            "Phone_Number": F("primary_contact_number"),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_action_performed_by": F("last_action_performed_by"),
            "Last_action_perform_timestamp": Trunc(
                F("last_action_perform_timestamp"), "second", tzinfo=get_timezone()),
            "Last_modified_by": F("last_modified_by"),
            "Last_modified_timestamp": Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Application_stage": F("queue_name"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Comments": F("comments")
        },
        "order_by": ["-Created_timestamp"],
    }
    return add_args(params, key, value)
