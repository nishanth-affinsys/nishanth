from django.db.models import Count, DateField, F, Q, TextField
from rest_framework.response import Response
from main.tenant_middleware import get_timezone
from django.db.models.functions import Trunc
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from profile_data.models import CampaignData, CampaignDynamicCta, Profile
from profile_data.serializers import (
    CampaignDataSerializers,
    CampaignDynamicCtaSerializers,
)
from main.utils.common_utils import custom_filters


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def rolled_campaigns_bignum_generic(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": CampaignData,
        "serializers": CampaignDataSerializers,
        "db_schema": get_db_name("profile"),
        "filter_kwargs": {
            "type": "DYNAMIC",
        },
        "values": ["campaign_id"],
        "count": True,
        "distinct": True,
    }
    return params


def rolled_campaigns_details(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": CampaignData,
        "serializers": CampaignDataSerializers,
        "db_schema": get_db_name("profile"),
        "filter_kwargs": {"type": "DYNAMIC"},
        "distinct_args": ["campaign_id"],
        "values": [
            "campaign_id",
            "campaign_name",
            "subcampaign_id",
            "subcampaign_name",
            "run_id",
        ],
        "annotate": {"Timestamp": Trunc("timestamp", "second", tzinfo=get_timezone())},
    }
    return add_args(params, key, value)


def campaign_cta_clicked_count(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": CampaignDynamicCta,
        "serializers": CampaignDynamicCtaSerializers,
        "db_schema": get_db_name("profile"),
        "distinct_args": ["campaign_id", "profile_id"],
        "count": True,
    }
    return params


def campaign_cta_clicked_details(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    filters = custom_filters(
        filter_data,
        "timestamp__range",
        None,
        "campaign_id__in",
    )
    qs = (
        CampaignDynamicCta.objects.using(get_db_name("profile"))
        .filter(**filters)
        .distinct("campaign_id", "profile_id")
        .values("id", "campaign_id", "click", "profile_id")
        .annotate(Clicked_Timestamp=Trunc("timestamp", "second", tzinfo=get_timezone()))
    )

    profile_id_list = qs.values_list("profile_id", flat=True)

    profile_details = Profile.objects.using(get_db_name("profile")).filter(
        profile_id__in=profile_id_list
    )

    results = []
    profile_details_dict = {profile.profile_id: profile for profile in profile_details}

    for item in qs:
        profile_id = item["profile_id"]
        profile = profile_details_dict.get(profile_id)
        if profile:
            merged_item = {
                "campaign_id": item["campaign_id"],
                "click": item["click"],
                "profile_id": item["profile_id"],
                "name": profile.user_name,
                "email": profile.email,
                "mobile_number": profile.mobile_number,
                "Clicked_Timestamp": item["Clicked_Timestamp"],
            }
            results.append(merged_item)

    return (
        results,
        [
            "campaign_id",
            "click",
            "profile_id",
            "name",
            "email",
            "mobile_number",
            "Clicked_Timestamp",
        ],
        "CTA Clicked Details",
    )


def campaign_targeted_users_count(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": CampaignData,
        "serializers": CampaignDataSerializers,
        "db_schema": get_db_name("profile"),
        "filter_kwargs": {
            "type": "DYNAMIC",
        },
        "distinct_args": ["campaign_id", "profile_id"],
        "count": True,
    }
    return params


def campaign_targeted_users_generic(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", None, "campaign_id__in")
    qs = (
        CampaignData.objects.using(get_db_name("profile"))
        .filter(type="DYNAMIC", **filters)
        .distinct("campaign_id", "profile_id")
        .annotate(Timestamp=Trunc("timestamp", "second", tzinfo=get_timezone()))
        .values()
    )

    profile_id_list = qs.values_list("profile_id", flat=True)

    profile_details = Profile.objects.using(get_db_name("profile")).filter(
        profile_id__in=profile_id_list
    )

    results = []
    profile_details_dict = {profile.profile_id: profile for profile in profile_details}

    for item in qs:
        profile_id = item["profile_id"]
        profile = profile_details_dict.get(profile_id)
        if profile:
            merged_item = {
                "campaign_id": item["campaign_id"],
                "campaign_name": item["campaign_name"],
                "subcampaign_id": item["subcampaign_id"],
                "subcampaign_name": item["subcampaign_name"],
                "clicked_timestamp": item["Timestamp"],
                "profile_id": profile_id,
                "name": profile.user_name,
                "email": profile.email,
                "mobile_number": profile.mobile_number,
            }
            results.append(merged_item)

    return (
        results,
        [
            "campaign_id",
            "campaign_name",
            "subcampaign_id",
            "subcampaign_name",
            "clicked_timestamp",
            "profile_id",
            "name",
            "email",
            "mobile_number",
        ],
        "Total Targeted Users - Details",
    )


def campaign_dynamic_campaign_aggregate_generic(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", None, "campaign_id__in")
    qs = (
        CampaignData.objects.using(get_db_name("profile"))
        .annotate(Timestamp=Trunc("timestamp", "second"))
        .filter(type="DYNAMIC", **filters)
        .values(
            "campaign_id",
            "subcampaign_id",
            "subcampaign_name",
            "campaign_name",
            "Timestamp",
        )
        .annotate(Total_Targeted_Users=Count("profile_id"))
    )

    cta_details = (
        CampaignDynamicCta.objects.using(get_db_name("profile"))
        .filter(**filters)
        .values("campaign_id")
        .annotate(Total_Clicked_CTA=Count("profile_id", distinct=True))
    )

    results = []
    cta_details_dict = {cta["campaign_id"]: cta for cta in cta_details}
    for item in qs:
        campaign_id = str(item["campaign_id"])
        cta_detail = cta_details_dict.get(campaign_id)
        if cta_detail:
            merged_item = {
                "campaign_id": campaign_id,
                "subcampaign_id": item["subcampaign_id"],
                "subcampaign_name": item["subcampaign_name"],
                "campaign_name": item["campaign_name"],
                "Timestamp": item["Timestamp"],
                "Total_Targeted_Users": item["Total_Targeted_Users"],
                "Total_Clicked_CTA": cta_detail["Total_Clicked_CTA"],
            }
            results.append(merged_item)

    return (
        results,
        [
            "campaign_id",
            "campaign_name",
            "subcampaign_id",
            "subcampaign_name",
            "Total_Targeted_Users",
            "Total_Clicked_CTA",
            "Timestamp",
        ],
        "Aggregate Dynamic Campaign Details",
    )
