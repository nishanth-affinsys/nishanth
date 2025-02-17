import json
import logging
from collections import defaultdict
from datetime import timedelta, datetime

from django.db.models import Count, Q, F, Case, When, Value, CharField, TextField
from django.db.models.functions import Trunc, Cast

from campaign_manager.models import (
    SubCampaignUser,
    CampaignUserLog,
    SubCampaignContentSegment,
)
from profile_data.models import ChannelInformation, CategoryOptout
from campaign_manager.serializers import (
    CampaignNotificationSerializer,
    CTAReportSerializer,
)
from campaign_manager.tasks import extract_message_from_notification
from console.models import (
    CampaignNotification,
    CampaignRolled,
    MessageLog,
    CtaReport,
)
from main.utils.common_utils import custom_filters
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import query

from main.utils.dynamic_db import dynamic_db_connection, get_db_name

string_time = "%d-%m-%Y %H:%M:%S"

# constants
opt_out = "Opt_Out"
opt_in = "Opt_In"

logger = logging.getLogger(__name__)

from django.db import connections, transaction


def campaign_notification_details_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        CampaignNotification,
        CampaignNotificationSerializer,
        get_db_name("analytics"),
    )
    qs2 = (
        qs.filter(notification_status="Success")
        .values(
            "campaign_id",
            "campaign_name",
            "sub_campaign_identifier",
            "run_id",
            "profile_name",
            "channel_id",
            "channel_name",
            "message_id",
        )
        .annotate(
            Message_timestamp=Trunc(
                "message_timestamp", "second", tzinfo=get_timezone()
            ),
            status=Case(
                When(status__isnull=True, then=Value("sent")),
                default=F("status"),
                output_field=CharField(),
            ),
        )
    )
    message_status_dict = defaultdict(lambda: {"sent": "", "delivered": "", "read": ""})
    for item in qs2:
        message_id = item["message_id"]
        status = item["status"]
        timestamp = item["Message_timestamp"]
        if status in ("sent", "delivered", "read"):
            message_status_dict[message_id][status] = (
                timestamp.strftime(string_time) if timestamp else ""
            )
    response = []
    for item in qs2:
        message_id = item["message_id"]
        campaign_id = item["campaign_id"]
        campaign_name = item["campaign_name"]
        subcampaign_id = item["sub_campaign_identifier"]
        run_id = item["run_id"]
        customer_name = item["profile_name"]
        channel = item["channel_name"]
        channel_id = item["channel_id"]
        sent_time = message_status_dict[message_id]["sent"]
        delivered_timestamp = message_status_dict[message_id]["delivered"]
        if sent_time and delivered_timestamp:
            sent_datetime = datetime.strptime(sent_time, string_time)
            delivered_datetime = datetime.strptime(delivered_timestamp, string_time)

            if sent_datetime > delivered_datetime:
                # Adjust sent timestamp by subtracting 10 seconds
                new_sent_datetime = sent_datetime - timedelta(seconds=10)
                sent_time = new_sent_datetime.strftime(string_time)

        if (
            sent_time
            or message_status_dict[message_id].get("delivered")
            or message_status_dict[message_id].get("read")
        ):
            value = {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "sub_campaign_id": subcampaign_id,
                "run_id": run_id,
                "customer_name": customer_name,
                "channel": channel,
                "channel_id": channel_id,
                "sent": message_status_dict[message_id]["sent"],
                "delivered": message_status_dict[message_id]["delivered"],
                "read": message_status_dict[message_id]["read"],
            }
            response.append(json.dumps(value))
    response = list(set(response))
    response = [json.loads(value) for value in response]
    response.sort(key=lambda x: x["campaign_id"])
    return (
        response,
        [
            "campaign_id",
            "campaign_name",
            "sub_campaign_id",
            "run_id",
            "customer_name",
            "channel",
            "channel_id",
            "sent",
            "delivered",
            "read",
        ],
        "notification_details",
    )


def target_users_by_run_id_generic(request):
    dynamic_db_connection("campaign")
    filter_data = request.data
    filters = custom_filters(
        filter_data,
        "campaign_run__campaign__last_modified__range",
        None,
        "campaign_run__campaign__id__in",
    )
    campaign_qs = (
        SubCampaignUser.objects.using(get_db_name("campaign"))
        .filter(**filters)
        .annotate(count_users=Cast("user_slots", output_field=TextField()))
        .values(
            campaign_id=F("campaign_run__campaign__campaign_id"),
            campaign_name=F("campaign_run__campaign__campaign_name"),
            sub_campaign_id=F("campaign_run__sub_campaign__identifier"),
            sub_campaign_name=F("campaign_run__sub_campaign__name"),
            run_id=F("campaign_run__run_id"),
        )
        .annotate(targeted_users=Count("count_users", distinct=True))
        .order_by("campaign_id")
    )
    return (
        campaign_qs,
        [
            "campaign_id",
            "campaign_name",
            "sub_campaign_id",
            "sub_campaign_name",
            "run_id",
            "targeted_users",
        ],
        "targeted_users_by_run",
    )


def total_messages_per_channel_generic(request, status):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        CampaignNotification,
        CampaignNotificationSerializer,
        get_db_name("analytics"),
    )
    if status == "sent":
        status_filter = Q(status="sent") | Q(status__isnull=True)
    else:
        status_filter = Q(status=status)

    result_qs = (
        qs.filter(
            status_filter,
            notification_status="Success",
        )
        .annotate(count=Count("message_id", filter=Q(status=status)))
        .values("channel_name")
        .annotate(count=Count("message_id"))
    )
    return result_qs


def opted_in_out_details_generic(
    request, campaign_category, profile_category, optin_category
):
    dynamic_db_connection("campaign")
    filter_data = request.data
    filters = custom_filters(
        filter_data, "campaign__last_modified__range", None, "campaign__id__in"
    )
    campaign_profile_ids = (
        CampaignUserLog.objects.using(get_db_name("campaign"))
        .filter(campaign__campaign_category=campaign_category, **filters)
        .values_list("profile_id", flat=True)
    )

    if filter_data.get("campaign_variants"):
        channel_qs = (
            SubCampaignContentSegment.objects.using(get_db_name("campaign"))
            .filter(
                subcampaigntarget__sub_campaign__campaign__in=filter_data.get(
                    "campaign_variants"
                )
            )
            .values_list("channels")
        )
    else:
        channel_qs = SubCampaignContentSegment.objects.using(
            get_db_name("campaign")
        ).values_list("channels")
    channels_list = [
        channel
        for channels_tuple in channel_qs
        for channel in channels_tuple[0].split(",")
    ]
    unique_channels_list = list(set(channels_list))
    status_dict = {}
    dynamic_db_connection("profile")
    profiles_qs = (
        CategoryOptout.objects.using(get_db_name("profile"))
        .annotate(
            status=Case(
                When(
                    Q(category=profile_category) | Q(category="ALL"),
                    then=Value(opt_out),
                ),
                When(
                    Q(category="OPTIN") | Q(category=optin_category), then=Value(opt_in)
                ),
                output_field=CharField(),
            )
        )
        .values("status", "profile_id")
    )
    for row in profiles_qs:
        profile_id = row["profile_id"]
        status_dict[profile_id] = row["status"]

    result = []
    qs = (
        ChannelInformation.objects.using(get_db_name("profile"))
        .filter(
            profile_id__in=list(campaign_profile_ids),
            channel_name__in=unique_channels_list,
        )
        .values(
            Profile_id=F("profile_id"),
            User_name=F("profile__user_name"),
            Channel_Id=F("channel_id"),
            Channel_Name=F("channel_name"),
        )
        .order_by("Profile_id")
    )
    for row in qs:
        result.append(
            {
                "Customer_name": row["User_name"],
                "Profile_Id": row["Profile_id"],
                "Channel_Id": row["Channel_Id"],
                "Channel": row["Channel_Name"],
                "Status": status_dict.get(row["Profile_id"], opt_in),
            }
        )
    return (
        result,
        ["Customer_name", "Profile_Id", "Channel_Id", "Channel", "Status"],
        "user_status",
    )


def total_users_by_channel_generic(
    request, campaign_category, profile_category, optin_category
):
    dynamic_db_connection("campaign")
    filter_data = request.data
    filters = custom_filters(
        filter_data, "campaign__last_modified__range", None, "campaign__id__in"
    )
    campaign_profile_ids = (
        CampaignUserLog.objects.using(get_db_name("campaign"))
        .filter(campaign__campaign_category=campaign_category, **filters)
        .values_list("profile_id", flat=True)
    )
    if filter_data.get("campaign_variants"):
        channel_qs = (
            SubCampaignContentSegment.objects.using(get_db_name("campaign"))
            .filter(
                subcampaigntarget__sub_campaign__campaign__in=filter_data.get(
                    "campaign_variants"
                )
            )
            .values_list("channels")
        )
    else:
        channel_qs = SubCampaignContentSegment.objects.using(
            get_db_name("campaign")
        ).values_list("channels")
    channels_list = [
        channel
        for channels_tuple in channel_qs
        for channel in channels_tuple[0].split(",")
    ]
    unique_channels_list = list(set(channels_list))
    status_dict = {}
    dynamic_db_connection("profile")
    profiles_qs = (
        CategoryOptout.objects.using(get_db_name("profile"))
        .annotate(
            status=Case(
                When(
                    Q(category=profile_category) | Q(category="ALL"),
                    then=Value(opt_out),
                ),
                When(
                    Q(category="OPTIN") | Q(category=optin_category), then=Value(opt_in)
                ),
                output_field=CharField(),
            )
        )
        .values("status", "profile_id")
    )
    for row in profiles_qs:
        profile_id = row["profile_id"]
        status_dict[profile_id] = row["status"]

    result = []

    channel_counts = defaultdict(lambda: {opt_in: 0, opt_out: 0, "Total": 0})
    qs = (
        ChannelInformation.objects.using(get_db_name("profile"))
        .filter(
            profile_id__in=list(campaign_profile_ids),
            channel_name__in=unique_channels_list,
        )
        .values(
            Profile_id=F("profile_id"),
            Channel_Id=F("channel_id"),
            Channel=F("channel_name"),
        )
    )
    for row in qs:
        profile_id = row["Profile_id"]
        channel_name = row["Channel"]
        status = status_dict.get(profile_id, opt_in)

        if status == "Opt_Out":
            channel_counts[channel_name][opt_out] += 1
        else:
            channel_counts[channel_name][opt_in] += 1

        channel_counts[channel_name]["Total"] += 1

    result = [
        {"Channel": channel, **counts} for channel, counts in channel_counts.items()
    ]
    logger.debug(result)
    return (
        result,
        ["Channel", "Opt_In", "Opt_Out", "Total"],
        "aggregate_users",
    )


def total_converted_users_per_run_generic(request):
    dynamic_db_connection("analytics")
    campaign_id = request.GET.get("campaign_id")
    sub_campaign_identifier = request.GET.get("sub_campaign_id")
    run_id = request.GET.get("run_id")
    channel_name = request.GET.get("channel")
    conversation_id = request.GET.get("channel_id")
    notification_queryset = CampaignNotification.objects.using(
        get_db_name("analytics")
    ).filter(
        campaign_id=campaign_id,
        sub_campaign_identifier=sub_campaign_identifier,
        run_id=run_id,
        channel_id=conversation_id,
        channel_name=channel_name,
    )
    if notification_queryset.exists() == False:
        return []
    mobile_number = notification_queryset.values_list(
        "initial_channel_id", flat=True
    ).first()
    batch_id = notification_queryset.latest("batch_identifier").batch_identifier
    rolled_qs = (
        CampaignRolled.objects.using(get_db_name("analytics"))
        .filter(
            channel_id=mobile_number, channel=channel_name, batch_identifier=batch_id
        )
        .annotate(Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()))
        .values("message", "timestamp", "Timestamp")
    )
    if rolled_qs.exists() == False:
        return []
    rolled_qs = rolled_qs.earliest("timestamp")
    message, quick_replies, timestamp = extract_message_from_notification(
        mobile_number,
        channel_name,
        rolled_qs,
        func_name=None,
        batch_id=batch_id,
    )
    response = [{"Message": message, "Timestamp": timestamp, "Source": "campaign"}]
    try:
        latest_message = (
            MessageLog.objects.using(get_db_name("analytics"))
            .filter(
                channel_id=conversation_id,
                channel=channel_name,
                timestamp__gt=rolled_qs.get("timestamp"),
                source="user",
            )
            .values("message", "timestamp", "session_id")
            .earliest("timestamp")
        )
        quick_replies = json.dumps(quick_replies)
        if json.dumps(latest_message.get("message")).lower() in quick_replies.lower():
            session_id = latest_message.get("session_id")
            next_campaign_timestamp_qs = (
                CampaignRolled.objects.using(get_db_name("analytics"))
                .filter(
                    channel_id=mobile_number,
                    channel=channel_name,
                    timestamp__gt=rolled_qs.get("timestamp"),
                )
                .order_by("timestamp")
            ).values_list("timestamp", flat=True)
            if next_campaign_timestamp_qs:
                next_campaign_timestamp = next_campaign_timestamp_qs[0]
            else:
                next_campaign_timestamp = None

            if next_campaign_timestamp is None or (
                next_campaign_timestamp > latest_message.get("timestamp")
            ):
                all_messages = (
                    MessageLog.objects.using(get_db_name("analytics"))
                    .annotate(
                        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone())
                    )
                    .filter(
                        session_id=session_id,
                        timestamp__gt=rolled_qs.get("timestamp"),
                    )
                    .values("message", "timestamp", "Timestamp", "source")
                )
                all_messages = sorted(all_messages, key=lambda x: x["timestamp"])
                for message_data in all_messages:
                    message = message_data.get("message")
                    timestamp = message_data.get("Timestamp")
                    source = message_data.get("source")
                    if source == "bot":
                        message, _, timestamp = extract_message_from_notification(
                            mobile_number,
                            channel_name,
                            message_data,
                        )
                    data = {
                        "Message": message,
                        "Timestamp": timestamp,
                        "Source": source,
                    }
                    response.append(data)

    except Exception as e:
        return response
    return response


def campaign_user_reply_button_details_generic(request):
    dynamic_db_connection("analytics")
    qs3 = query(request, CtaReport, CTAReportSerializer, get_db_name("analytics"))
    response = qs3.values(
        "campaign_id",
        "campaign_name",
        "sub_campaign_id",
        "run_id",
        "customer_name",
        "channel",
        "channel_id",
    ).annotate(
        CTA_Clicked=F("cta_clicked"),
        Clicked_Timestamp=Trunc(
            F("clicked_timestamp"), "second", tzinfo=get_timezone()
        ),
    )
    return (
        response,
        [
            "campaign_id",
            "campaign_name",
            "sub_campaign_id",
            "run_id",
            "customer_name",
            "channel",
            "channel_id",
            "CTA_Clicked",
            "Clicked_Timestamp",
        ],
        "cta_clicked",
    )


# old campaign manager
# def channelwise_count_campaign_user_generic(request):
#     filter_data = request.data
#     qs1 = (
#         CampaignsCampaignvariantdetail.objects.using("campaign")
#         .filter(
#             campaign_variant__tenant=get_current_tenant_name(),
#             timestamp__range=filter_data.get("timestamp__range"),
#             campaign_variant_id__in=filter_data.get("campaign_variants"),
#         )
#         .values("campaign_variant_id", "campaign_variant__name", "selected_users")
#     )
#
#     res = []
#     for i in qs1:
#         whatsapp = 0
#         email = 0
#         facebook = 0
#         users = i["selected_users"]
#         for j in users:
#             if j.get("email"):
#                 email += 1
#             if j.get("fb_id"):
#                 facebook += 1
#             if j.get("whatsapp_number"):
#                 whatsapp += 1
#         data = {
#             "campaign_variant_id": i["campaign_variant_id"],
#             "campaign_name": i["campaign_variant__name"],
#             "whatsapp": whatsapp,
#             "facebook": facebook,
#             "email": email,
#         }
#         res.append(data)
#     response = sorted(res, key=lambda x: x["campaign_variant_id"])
#     return (
#         response,
#         ["campaign_variant_id", "campaign_name", "whatsapp", "facebook", "email"],
#         "user_count",
#     )
