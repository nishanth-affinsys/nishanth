from django.db.models import Count, DateField, F, Q, TextField
from django.db.models.functions import Cast, TruncDate

from campaign_manager.models import Campaign, SubCampaignDetail, CampaignUserLog
from campaign_manager.serializers import CampaignSerializer, SubCampaignSerializer
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import query
from main.utils.dynamic_db import get_db_name, dynamic_db_connection
from main.utils.common_utils import custom_filters


def created_campaigns_bignum_generic(request):
    dynamic_db_connection("campaign")
    params = {
        "request": request,
        "models": Campaign,
        "serializers": CampaignSerializer,
        "db_schema": get_db_name("campaign"),
        "count": True,
    }
    return params


def campaigns_status_bignum_generic(request, status):
    dynamic_db_connection("campaign")
    params = {
        "request": request,
        "models": Campaign,
        "serializers": CampaignSerializer,
        "db_schema": get_db_name("campaign"),
        "filter_kwargs": {
            "status": status,
            "archived": False,
        },
        "count": True,
    }
    return params


def deleted_campaigns_bignum_generic(request):
    dynamic_db_connection("campaign")
    params = {
        "request": request,
        "models": Campaign,
        "serializers": CampaignSerializer,
        "db_schema": get_db_name("campaign"),
        "filter_kwargs": {"archived": True},
        "count": True,
    }
    return params


def active_inactive_linechart_generic(request):  # gives the status of campaigns
    dynamic_db_connection("campaign")
    qs = query(
        request,
        Campaign,
        CampaignSerializer,
        db_schema=get_db_name("campaign"),
    )
    qs1 = (
        qs.values(Date=TruncDate("last_modified", tzinfo=get_timezone()))
        .annotate(
            Active_Campaigns=Count(
                "id",
                distinct=True,
                filter=Q(status="ACTIVE") & Q(archived=False),
            ),
            Inactive_Campaigns=Count(
                "id",
                distinct=True,
                filter=Q(status="INACTIVE") & Q(archived=False),
            ),
            Completed_Campaigns=Count(
                "id",
                distinct=True,
                filter=Q(status="COMPLETED") & Q(archived=False),
            ),
            Deleted_Campaigns=Count("id", distinct=True, filter=Q(archived=True)),
        )
        .order_by("Date")
    )
    return qs1


def campaign_aggregate_details_generic(request):
    dynamic_db_connection("campaign")
    qs = query(
        request,
        SubCampaignDetail,
        SubCampaignSerializer,
        db_schema=get_db_name("campaign"),
    )
    qs1 = qs.values(Campaign_id=F("campaign__campaign_id")).annotate(
        Total_Sub_Campaigns=Count("identifier"),
        Total_Active_Sub_Campaigns=Count(
            "identifier",
            filter=Q(status="ACTIVE"),
            distinct=True,
        ),
        Total_Inactive_Sub_Campaigns=Count(
            "identifier",
            filter=Q(status="INACTIVE"),
            distinct=True,
        ),
        Total_Completed_Sub_Campaigns=Count(
            "identifier",
            filter=Q(status="COMPLETED"),
            distinct=True,
        ),
    )
    return (
        qs1,
        [
            "Campaign_id",
            "Total_Sub_Campaigns",
            "Total_Active_Sub_Campaigns",
            "Total_Inactive_Sub_Campaigns",
            "Total_Completed_Sub_Campaigns",
        ],
        "Campaigns_aggregate_details",
    )


def campaign_types_details_generic(request):
    dynamic_db_connection("campaign")
    qs = query(
        request,
        SubCampaignDetail,
        SubCampaignSerializer,
        db_schema=get_db_name("campaign"),
    )
    qs1 = qs.values(
        Campaign_Id=F("campaign__campaign_id"),
        Campaign_Name=F("campaign__campaign_name"),
        Campaign_Category=F("campaign__campaign_category"),
        Sub_Campaign_Id=F("identifier"),
        Sub_Campaign_Name=F("name"),
        Sub_Campaign_Status=F("status"),
        Sub_Campaign_Type=F("type"),
    ).order_by("Campaign_Id")
    return (
        qs1,
        [
            "Campaign_Id",
            "Campaign_Name",
            "Campaign_Category",
            "Sub_Campaign_Id",
            "Sub_Campaign_Name",
            "Sub_Campaign_Status",
            "Sub_Campaign_Type",
        ],
        "campaign_types_details",
    )


def sub_campaign_targeted_user_generic(request):
    dynamic_db_connection("campaign")
    filter_data = request.data
    filters = custom_filters(
        filter_data, "campaign__last_modified__range", None, "campaign__id__in"
    )
    qs1 = (
        CampaignUserLog.objects.using(get_db_name("campaign"))
        .filter(**filters)
        .annotate(count_users=Cast("user_slots", output_field=TextField()))
        .values(
            Campaign_Id=F("campaign__campaign_id"),
            Campaign_Name=F("campaign__campaign_name"),
            Sub_Campaign_Id=F("subcampaign__identifier"),
            Sub_Campaign_Name=F("subcampaign__name"),
        )
        .annotate(Total_Targeted_User=Count("count_users", distinct=True))
        .order_by("Campaign_Id")
    )
    return (
        qs1,
        [
            "Campaign_Id",
            "Campaign_Name",
            "Sub_Campaign_Id",
            "Sub_Campaign_Name",
            "Total_Targeted_User",
        ],
        "subcampaign_targeted_users",
    )
