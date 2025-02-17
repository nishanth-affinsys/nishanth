from collections import OrderedDict

from django.db.models import (
    Case,
    When,
    Value,
    F,
    CharField,
)
from django.db.models.functions import Concat, Trunc

from main.settings import ENABLE_BRANCH_FILTER
from main.tenant_middleware import get_current_tenant_name, get_timezone
from onboarding.models import (
    DetailedReportTableRt,
    DetailedReportTableSp,
    UserBranchConfig,
)
from client_specific.models import OnboardingRetailComments
from onboarding.serializers import OnboardingSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def add_customer_or_business_name(params, rt_table, sp_table, model_name, insert_index):
    custom_column = ()
    if model_name == rt_table:
        # Adding Customer_name at the specified position in the OrderedDict
        custom_column = (
            "Customer_name",
            Concat(
                F("first_name"),
                Value(" "),
                F("middle_name"),
                Value(" "),
                F("last_name"),
            ),
        )
    elif model_name == sp_table:
        # Adding Business_name at the specified position in the OrderedDict
        custom_column = ("Business_name", F("business_name"))

    params["values_kwargs"] = OrderedDict(
        list(params["values_kwargs"].items())[:insert_index]
        + [custom_column]
        + list(params["values_kwargs"].items())[insert_index:]
    )

    return params


def get_branch_wise_users_data(request):
    branch_list = []
    dynamic_db_connection("onboarding")
    logged_user = request.user.user_id
    branch_codes = (
        UserBranchConfig.objects.using(get_db_name("onboarding"))
        .filter(tenant=get_current_tenant_name(), is_deleted="N", user_uuid=logged_user)
        .values_list("branch_code", flat=True)
    )
    branch_list = list(branch_codes)
    return branch_list

    # branch_list = []
    # logged_user = request.user.user_id
    # print("i am here")
    # branch = list(
    #     UserBranchConfig.objects.using("onboarding")
    #     .filter(tenant=get_current_tenant_name(), is_deleted="N", user_uuid=logged_user)
    #     .values("branch_code")
    # )
    # for i in branch:
    #     if i["branch_code"]:
    #         branch_list.append(i["branch_code"])
    # print("branch list===>", branch_list)
    # return branch_list


def onb_detailed_applications_report_generic(
        request, model_name, onboarding_channel, insert_index, key=None, value=None
):
    dynamic_db_connection("onboarding")
    params = {
        "request": request,
        "models": model_name,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("onboarding"),
        "filter_kwargs": {
            "onboarding_channel": onboarding_channel,
        },
        "values_kwargs": {
            "Application_number": F("external_reference"),
            "Product_name": F("product_name"),
            "Phone_Number": F("primary_contact_number"),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_modified_by": F("last_modified_by"),
            "Last_modified_timestamp": Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Verified_by": F("action_performed_by"),
            "Verified_timestamp": Trunc(
                F("action_perform_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Account_number_1": F("account_num1"),
            "Account_number_2": F("account_num2"),
            "Created_at_branch_code": F("created_at_branch_code"),
            "Present_at_branch_code": F("present_at_branch_code"),
            "Application_stage": F("queue_name"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
        },
        "order_by": ["-Created_timestamp"],
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    params = add_customer_or_business_name(
        params,
        DetailedReportTableRt,
        DetailedReportTableSp,
        model_name,
        insert_index,
    )
    return add_args(params, key, value)


def detailed_report_comments_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": OnboardingRetailComments,
        "serializers": OnboardingSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "Application_number": F("internal_reference"),
            "Product_name": F("product_name"),
            "Phone_Number": F("primary_contact_number"),
            "Created_by": F("created_by"),
            "Created_timestamp": Trunc(
                F("create_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_modified_by": F("last_modified_by"),
            "Last_modified_timestamp": Trunc(
                F("last_modified_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_action_performed_by": F("last_action_performed_by"),
            "Last_action_perform_timestamp": Trunc(
                F("last_action_perform_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Approved_by": F("submit_by"),
            "Approved_timestamp": Trunc(
                F("submit_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Account_number_1": F("account_num1"),
            "Account_number_2": F("account_num2"),
            "Created_at_branch_code": F("created_at_branch_code"),
            "Present_at_branch_code": F("present_at_branch_code"),
            "Application_stage": F("queue_name"),
            "Customer_type": Case(
                When(customer_type="ntb", then=Value("NTB")),
                When(customer_type="etb", then=Value("ETB")),
                output_field=CharField(),
            ),
            "Action": F("action_code"),
            "Comments": F("comments")
        }
    }
    if ENABLE_BRANCH_FILTER:
        branch_list = get_branch_wise_users_data(request)
        params["filter_kwargs"]["created_at_branch_code__in"] = branch_list
    return add_args(params, key, value)

