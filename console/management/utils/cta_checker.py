from django.utils import timezone
import time
from datetime import timedelta

from console.models import CampaignRolled, SunshineMapping, CampaignNotification
from main.settings import get_int_env_value
import logging

from django.conf import settings
from main.utils.dynamic_db import get_db_consumer_name, dynamic_db_consumer_connection
from main.utils.publisher import publish_common

logger = logging.getLogger(__name__)


def check_if_cta_exists(data: dict):
    start_time = time.time()
    source = data.get("source")
    logger.debug(f"source of message is {source}")
    if source == "user":
        tenant = data.get("tenant")
        message = data.get("message")
        message_log_channel_id = data.get("channel_id")
        channel = data.get("channel")

        dynamic_db_consumer_connection("analytics", tenant)

        now = timezone.now() + timedelta(hours=1)
        max_time_limit = now - timedelta(
            days=int(get_int_env_value("MAX_CTA_TIME_LIMIT"))
        )

        channel_id = (
                SunshineMapping.objects.using(get_db_consumer_name("analytics", tenant))
                .filter(conversation_id=message_log_channel_id, tenant=tenant)
                .values_list("mobile_number", flat=True)
                or [message_log_channel_id]
        )[0]

        logger.info(f"Checking if CTA exists in {tenant} with message {message}")

        logger.debug(f"channel_id is {channel_id} with channel_id is {channel}")

        all_batch_ids = (
            CampaignRolled.objects.using(get_db_consumer_name("analytics", tenant))
            .filter(
                tenant=tenant,
                channel_id=channel_id,
                channel=channel,
                timestamp__range=[max_time_limit, now],
            )
            .values_list("batch_identifier", flat=True)
            .distinct()
        )

        if all_batch_ids:
            matched_batch_id = False

            for batch_id in all_batch_ids:
                matched_batch_id = batch_id if batch_id in message else matched_batch_id

            if matched_batch_id:
                logger.info(f"CTA exists in {tenant} with message {message}")
                logger.info("logging into cta table")
                rolled_qs = (
                    CampaignRolled.objects.using(
                        get_db_consumer_name("analytics", tenant)
                    )
                    .filter(
                        batch_identifier=matched_batch_id,
                        tenant=tenant,
                        channel_id=channel_id,
                        channel=channel,
                        timestamp__range=[max_time_limit, now],
                    )
                    .values("timestamp")
                    .latest("timestamp")
                )
                campaign_notification = (
                    CampaignNotification.objects.using(
                        get_db_consumer_name("analytics", tenant)
                    )
                    .filter(
                        batch_identifier=matched_batch_id,
                        tenant=tenant,
                        initial_channel_id=channel_id,
                        channel_name=channel,
                    )
                    .values(
                        "campaign_id",
                        "campaign_name",
                        "sub_campaign_identifier",
                        "run_id",
                        "profile_name",
                        "message_id",
                        "batch_identifier",
                        "last_modified",
                        "campaign_filter_id",
                        "notification_timestamp",
                        "subcampaign_name"
                    )
                    .latest("notification_timestamp")
                )

                cta_publish = {
                    "method": "cta_report",
                    "campaign_id": campaign_notification.get("campaign_id"),
                    "campaign_name": campaign_notification.get("campaign_name"),
                    "sub_campaign_id": campaign_notification.get(
                        "sub_campaign_identifier"
                    ),
                    "run_id": campaign_notification.get("run_id"),
                    "customer_name": campaign_notification.get("profile_name"),
                    "channel": channel,
                    "channel_id": channel_id,
                    "cta_clicked": message,
                    "campaign_rolled_timestamp": rolled_qs.get("timestamp").timestamp(),
                    "clicked_timestamp": data.get("timestamp"),
                    "last_modified_timestamp": campaign_notification.get(
                        "last_modified"
                    ).timestamp(),
                    "notification_timestamp": campaign_notification.get(
                        "notification_timestamp"
                    ).timestamp(),
                    "campaign_variants": campaign_notification.get(
                        "campaign_filter_id"
                    ),
                    "tenant": tenant,
                }
                publish_common(
                    data=cta_publish,
                    exchange="analytics_publish",
                    routing_key="analytics_cta_publish",
                )

                """Publish event for profile for cta recording"""
                profile_cta_publish = {
                    "channel_id": channel_id,
                    "channel_name": channel,
                    "campaign_id": campaign_notification.get("campaign_filter_id"),
                    "campaign_name": campaign_notification.get("campaign_name"),
                    "sub_campaign_id": campaign_notification.get(
                        "sub_campaign_identifier"
                    ),
                    "subcampaign_name": campaign_notification.get("sub_campaign_name"),
                    "batch": matched_batch_id,
                    "run_id": campaign_notification.get("run_id"),
                    "campaign_identifier": campaign_notification.get("campaign_id"),
                    "cta_clicked": "Yes",
                    "clicked_timestamp": data.get("timestamp"),
                    "cta_message": message
                }
                publish_common(
                    data=profile_cta_publish,
                    exchange='campaign_data',
                    routing_key='campaign.cta',
                )

                cta_exclude = {
                    "method": "cta_report_exclude",
                    "channel_id": channel_id,
                    "channel": channel,
                    "batch_id": matched_batch_id,
                    "tenant": tenant,
                }
                publish_common(
                    data=cta_exclude,
                    exchange="analytics_publish",
                    routing_key="analytics_cta_publish",
                )
            else:
                logger.info(f"No CTA exists in {tenant} with message {message}")
        else:
            logger.debug(f"No batch ids found in time frame {max_time_limit} and {now}")
    logger.info(
        f"time taken to check for CTA: {round(time.time() - start_time, 2)} seconds"
    )
