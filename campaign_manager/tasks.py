import ast

# import json
# import time
# from datetime import timedelta

# from django.utils import timezone

from django.db.models import CharField, Value, When, Case, F, Max, TextField
from django.db.models.functions import Trunc, Cast

# from campaign_manager.models import Campaign
from profile_data.models import NotificationData

# from console.models import (
#     MessageLog,
#     CampaignRolled,
#     CampaignNotification,
#     CtaReport,
#     PikaClientDynamicQueues,
#     CampaignCtaExclude,
#     SunshineMapping,
# )
# from main.celery import background

import logging

# from main.settings import get_int_env_value
from main.tenant_middleware import get_timezone

# from main.utils.publisher import publish_eventlogger

from main.utils.dynamic_db import dynamic_db_connection, get_db_name

logger = logging.getLogger("__name__")


def extract_message_from_notification(
    channel_id, channel_name, rolled_qs, func_name=None, batch_id=None
):
    dynamic_db_connection("profile")
    message = ast.literal_eval(rolled_qs.get("message"))
    quick_replies = message.get("quick_replies")
    timestamp = rolled_qs.get("Timestamp")
    if batch_id:
        conditions = {
            "Timestamp": (
                Trunc(F("timestamp"), "second", tzinfo=get_timezone())
                if func_name == "CTA"
                else F("timestamp")
            )
        }

        qs = (
            NotificationData.objects.using(get_db_name("profile"))
            .filter(
                batch__identifier=batch_id,
                batch__channel_id=channel_id,
                batch__channel_name=channel_name,
                service_name="campaign",
                status="Success",
            )
            .annotate(message_as_text=Cast("message", output_field=TextField()))
            .values("message_as_text")
            .annotate(**conditions)
            .earliest("Timestamp")
        )
        return qs.get("message_as_text"), quick_replies, timestamp
    else:
        data = message.get("data")[0]
        title = data.get("title", " ")
        subtitle = data.get("subtitle", " ")
        if title and subtitle:
            text = title + " " + subtitle
        elif title:
            text = title
        else:
            text = subtitle
        return text, quick_replies, timestamp


# @background
# def schedule_cta():
#     tenants = PikaClientDynamicQueues.objects.using("analytics").values_list(
#         "name", flat=True
#     )
#
#     for tenant in tenants:
#         cta_task_logging(tenant)


# def cta_task_logging(tenant):
#     logger.info(f"task scheduled for tenant->{tenant}")
#     start_time = time.time()
#
#     now = timezone.now()
#     max_time_limit = now - timedelta(days=int(get_int_env_value("MAX_CTA_TIME_LIMIT")))
#
#     # latest_campaigns = CampaignRolled.objects.using("event").annotate(max_timestamp=Max("timestamp")).values_list("batch_identifier", flat=True).order_by("-max_timestamp")[:5]
#     #
#     # latest_campaign_rolled_timestamp_qs = (
#     #     CampaignRolled.objects.using("event")
#     #     .filter(tenant=tenant, timestamp__range=[max_time_limit, now], batch_identifier__in=latest_campaigns)
#     #     .values("channel_id", "channel")
#     #     .annotate(Max_timestamp=Max("timestamp"))
#     #     .values_list("channel_id", "channel", "Max_timestamp")
#     # )
#     # latest_max_campaign_rolled_timestamp_qs = {
#     #     f"{str(channel_id)}~~~{str(channel)}": timestamp
#     #     for channel_id, channel, timestamp in latest_campaign_rolled_timestamp_qs
#     # }
#     dynamic_db_connection("analytics")
#     cta_report_timestamp = (
#         CtaReport.objects.using(get_db_name("analytics"))
#         .filter(tenant=tenant)
#         .values("channel_id", "channel")
#         .annotate(
#             Max_timestamp=Max("campaign_rolled_timestamp"),
#             Max_notification_modified=Max("notification_timestamp"),
#         )
#         .values_list(
#             "channel_id", "channel", "Max_timestamp", "Max_notification_modified"
#         )
#     )
#     max_cta_report_timestamp_qs = {
#         f"{str(channel_id)}~~~{str(channel)}": {
#             "Max_timestamp": max_timestamp,
#             "Max_notification_modified": max_last_modified,
#         }
#         for channel_id, channel, max_timestamp, max_last_modified in cta_report_timestamp
#     }
#
#     # logger.info(f"latest campaigns {latest_campaigns}")
#     # cta_log(latest_max_campaign_rolled_timestamp_qs, max_cta_report_timestamp_qs, tenant, latest_campaigns)
#     # logger.info(f"execution time of task {time.time() - start_time} seconds (for latest entries)")
#
#     campaign_rolled = CampaignRolled.objects.using(get_db_name("analytics")).filter(
#         tenant=tenant, timestamp__range=[max_time_limit, now]
#     )
#
#     campaign_ids = campaign_rolled.values_list("batch_identifier", flat=True).distinct()
#
#     campaign_rolled_timestamp_qs = (
#         campaign_rolled.filter(batch_identifier__in=campaign_ids)
#         .values("channel_id", "channel")
#         .annotate(Max_timestamp=Max("timestamp"))
#         .values_list("channel_id", "channel", "Max_timestamp")
#     )
#     max_campaign_rolled_timestamp_qs = {
#         f"{str(channel_id)}~~~{str(channel)}": timestamp
#         for channel_id, channel, timestamp in campaign_rolled_timestamp_qs
#     }
#     cta_log(
#         max_campaign_rolled_timestamp_qs,
#         max_cta_report_timestamp_qs,
#         tenant,
#         campaign_ids,
#     )
#     logger.info(f"execution time of task {time.time() - start_time} seconds")


# def cta_log(
#     max_campaign_rolled_timestamp_qs, max_cta_report_timestamp_qs, tenant, campaign_ids
# ):
#     dynamic_db_connection("analytics")
#     skipped = 0
#     completed = 0
#     # completed_list = []
#     for key, value in max_campaign_rolled_timestamp_qs.items():
#         channel_id, channel = key.split("~~~")
#         cta_report_entry = max_cta_report_timestamp_qs.get(key, {})
#         if (
#             cta_report_entry.get("Max_timestamp")
#             and value
#             and value > cta_report_entry.get("Max_timestamp")
#         ):
#             camp_notif_filters = {
#                 "notification_timestamp__gt": cta_report_entry.get(
#                     "Max_notification_modified"
#                 ),
#                 "initial_channel_id": channel_id,
#                 "channel_name": channel,
#             }
#             cam_rolled_filters = {
#                 "timestamp__gt": cta_report_entry.get("Max_timestamp"),
#                 "channel_id": channel_id,
#                 "channel": channel,
#             }
#         else:
#             camp_notif_filters = {
#                 "initial_channel_id": channel_id,
#                 "channel_name": channel,
#             }
#             cam_rolled_filters = {
#                 "channel_id": channel_id,
#                 "channel": channel,
#             }
#
#         if campaign_ids:
#             camp_notif_filters["batch_identifier__in"] = campaign_ids
#
#         exclude_list = (
#             CampaignCtaExclude.objects.using(get_db_name("analytics"))
#             .filter(channel_id=channel_id, channel=channel, tenant=tenant)
#             .values_list("batch_id", flat=True)
#             or []
#         )
#         qs = (
#             CampaignNotification.objects.using(get_db_name("analytics"))
#             .filter(**camp_notif_filters)
#             .exclude(batch_identifier__in=exclude_list)
#         )
#         qs2 = (
#             qs.filter(
#                 tenant=tenant,
#                 notification_status="Success",
#             )
#             .values(
#                 "campaign_id",
#                 "campaign_name",
#                 "sub_campaign_identifier",
#                 "run_id",
#                 "profile_name",
#                 "message_id",
#                 "batch_identifier",
#                 "last_modified",
#                 "campaign_variants",
#                 "notification_timestamp",
#             )
#             .annotate(
#                 status=Case(
#                     When(status__isnull=True, then=Value("sent")),
#                     default=F("status"),
#                     output_field=CharField(),
#                 ),
#             )
#             .filter(status="sent")
#         )
#
#         conversation_id = SunshineMapping.objects.using(
#             get_db_name("analytics")
#         ).filter(mobile_number=channel_id, tenant=tenant).values_list(
#             "conversation_id", flat=True
#         ) or [
#             channel_id
#         ]
#         if (
#             MessageLog.objects.using(get_db_name("analytics"))
#             .filter(
#                 channel_id=conversation_id[0],
#                 source="user",
#                 channel=channel,
#                 tenant=tenant,
#             )
#             .exists()
#         ):
#             for item in qs2:
#                 campaign_id = item["campaign_id"]
#                 campaign_name = item["campaign_name"]
#                 subcampaign_id = item["sub_campaign_identifier"]
#                 run_id = item["run_id"]
#                 customer_name = item["profile_name"]
#                 batch_id = item["batch_identifier"]
#                 last_modified = item["last_modified"]
#                 campaign_variants = item["campaign_variants"]
#                 notification_timestamp = item["notification_timestamp"]
#                 try:
#                     rolled_qs = (
#                         CampaignRolled.objects.using(get_db_name("analytics"))
#                         .filter(
#                             tenant=tenant,
#                             batch_identifier=batch_id,
#                             **cam_rolled_filters,
#                         )
#                         .values("message", Timestamp=F("timestamp"))
#                         .earliest("Timestamp")
#                     )
#                     (
#                         message,
#                         quick_replies,
#                         timestamp,
#                     ) = extract_message_from_notification(
#                         channel_id,
#                         channel,
#                         rolled_qs,
#                         tenant=tenant,
#                         func_name="CTA",
#                         batch_id=batch_id,
#                     )
#                     latest_message = (
#                         MessageLog.objects.using(get_db_name("analytics"))
#                         .filter(
#                             tenant=tenant,
#                             channel_id=conversation_id[0],
#                             channel=channel,
#                             timestamp__gt=timestamp,
#                             source="user",
#                         )
#                         .values("message", "timestamp", "session_id")
#                         .earliest("timestamp")
#                     )
#                     quick_replies = json.dumps(quick_replies)
#                     if json.dumps(latest_message.get("message")) in quick_replies:
#                         message = latest_message.get("message")
#                         clicked_timestamp = latest_message.get("timestamp")
#                         next_campaign_timestamp_qs = (
#                             CampaignRolled.objects.using("event")
#                             .filter(
#                                 tenant=tenant,
#                                 channel_id=channel_id,
#                                 channel=channel,
#                                 timestamp__gt=rolled_qs.get("Timestamp"),
#                             )
#                             .order_by("timestamp")
#                         ).values_list("timestamp", flat=True)
#                         if next_campaign_timestamp_qs:
#                             next_campaign_timestamp = next_campaign_timestamp_qs[0]
#                         else:
#                             next_campaign_timestamp = None
#                         if not (
#                             next_campaign_timestamp is not None
#                             and next_campaign_timestamp
#                             < latest_message.get("timestamp")
#                         ):
#                             data = {
#                                 "method": "cta_report",
#                                 "campaign_id": campaign_id,
#                                 "campaign_name": campaign_name,
#                                 "sub_campaign_id": subcampaign_id,
#                                 "run_id": run_id,
#                                 "customer_name": customer_name,
#                                 "channel": channel,
#                                 "channel_id": channel_id,
#                                 "cta_clicked": message,
#                                 "campaign_rolled_timestamp": rolled_qs.get(
#                                     "Timestamp"
#                                 ).timestamp(),
#                                 "clicked_timestamp": clicked_timestamp.timestamp(),
#                                 "last_modified_timestamp": last_modified.timestamp(),
#                                 "notification_timestamp": notification_timestamp.timestamp(),
#                                 "campaign_variants": campaign_variants,
#                                 "tenant": tenant,
#                             }
#                             publish_eventlogger(data, "analytics_cta_publish")
#                             data = {
#                                 "method": "cta_report_exclude",
#                                 "channel_id": channel_id,
#                                 "channel": channel,
#                                 "batch_id": batch_id,
#                                 "tenant": tenant,
#                             }
#                             publish_eventlogger(data, "analytics_cta_publish")
#                     else:
#                         data = {
#                             "method": "cta_report_exclude",
#                             "channel_id": channel_id,
#                             "channel": channel,
#                             "batch_id": batch_id,
#                             "tenant": tenant,
#                         }
#                         publish_eventlogger(data, "analytics_cta_publish")
#                 except Exception as e:
#                     continue
#             # completed_list.append({"mobile_number": channel_id, "conversation_id": conversation_id[0]})
#             completed += 1
#         else:
#             skipped += 1
#     logger.info(f"Number of users skipped: {skipped}")
#     logger.info(f"Number of users completed: {completed}")


# logger.info(f"list of completed users: {completed_list}")
