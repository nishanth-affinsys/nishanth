from datetime import timedelta

from django.utils import timezone

from django.db.models import F, Q
from django.db.models.functions import Trunc

from client_specific.models import OnboardingAuditDetails
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from onboarding.serializers import OnboardingSerializer, OnboardingAuditSerializer
from main.tenant_middleware import get_timezone
from console.models import OnboardingCampaignDetails


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


# def comments_approver_generic(request):
#     dynamic_db_connection("onboarding")
#     filtered_data = request.data
#     if filtered_data.get("timestamp__range"):
#         internal_reference_list = (
#             SingleCifRetailData.objects.using(get_db_name("onboarding"))
#             .filter(
#                 queue_code="QSUCCESS",
#                 last_modified_timestamp__range=filtered_data.get("timestamp__range"),
#             )
#             .values_list("internal_reference", flat=True)
#         )
#     else:
#         internal_reference_list = (
#             SingleCifRetailData.objects.using(get_db_name("onboarding"))
#             .filter(
#                 queue_code="QSUCCESS",
#             )
#             .values_list("internal_reference", flat=True)
#         )
#     query = (
#         RtAuditComments.objects.using(get_db_name("onboarding"))
#         .filter(
#             internal_reference__in=list(internal_reference_list),
#             action_code__in=["CBSSUBMIT", "REJECT"],
#         )
#         .values("internal_reference", "action_code", "comments")
#     )
#     return (
#         query,
#         ["internal_reference", "action_code", "comments"],
#         "comments_approver",
#     )


def audit_trail_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": OnboardingAuditDetails,
        "serializers": OnboardingAuditSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "Onboarding_reference_number": F("single_cifrt_internal_reference"),
            "Kyc_reference": F("kyc_reference"),
            "Event": F("event"),
            "Comment": F("comments"),
            "Action_performed_by": F("action_by"),
            "Action_perform_timestamp": Trunc(
                F("action_perform_timestamp"), "second", tzinfo=get_timezone()
            )
        },
        "order_by": ["-Action_perform_timestamp"],
    }
    return add_args(params, key, value)


# def onboarding_potential_customers_generic(request):
#     filter_data = request.data
#     queryset = KycMaster.objects.filter(
#         queue_code='QSUCCESS',
#         last_modified_timestamp__range=filter_data.get('timestamp__range')
#     ).exclude(
#         Q(internal_reference__in=SingleCifRetailData.objects.values('kyc_reference'))
#     )
#     return queryset, _, _


def onboarding_campaign_details_util(request):
    dynamic_db_connection("analytics")
    filter_data = request.data
    start_time, end_time = timezone.now() - timedelta(days=int(filter_data["days"])), timezone.now()

    queryset = (
        OnboardingCampaignDetails.objects.using(get_db_name("analytics")).
        filter(
            last_modified__range=[start_time, end_time],
        ).exclude(
            application_status__in=['QSUCCESS', 'QBANKINGASSURANCE', 'QDAYTWOREMEDIATED', 'QDAYTWOFAIL', 'QDAYTWOPASS'],
        ).values("email", "mobile_number").distinct()
    )
    filtered_data = [entry for entry in queryset if not (entry["email"] == "" and entry["mobile_number"] == "")]
    return filtered_data
