from django.db import models
import os


class MessageLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_id = models.CharField(max_length=50)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    context = models.CharField(max_length=50, blank=True, null=True)
    handled = models.CharField(max_length=1, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    intent = models.CharField(max_length=50, blank=True, null=True)
    score = models.DecimalField(max_digits=30, decimal_places=30, blank=True, null=True)
    event = models.CharField(max_length=50, blank=True, null=True)
    event_type = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "message_log"


class StageLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_id = models.CharField(max_length=150)
    channel = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_intent = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=150, blank=True, null=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    stage_result = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    rmn = models.CharField(max_length=20, blank=True, null=True)
    transaction_code = models.CharField(max_length=10, blank=True, null=True)
    node_id = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    from_account = models.CharField(max_length=100, blank=True, null=True)
    applicable_charges = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stage_log"


class ApiLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    endpoint = models.CharField(max_length=200, blank=True, null=True)
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    request_id = models.CharField(max_length=150, blank=True, null=True)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    api = models.CharField(max_length=500, blank=True, null=True)
    stage = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    internal_reference = models.CharField(max_length=500, blank=True, null=True)
    external_reference = models.CharField(max_length=500, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    exception = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "api_log"


class UserFlow(models.Model):
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    target = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    rank = models.BigIntegerField(blank=True, null=True)
    customer_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "user_flow"


class StageLogAuth(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=35, blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, null=True)
    result_detail = models.CharField(max_length=500, blank=True, null=True)
    ip_info = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    payload = models.TextField(blank=True, null=True)
    provider = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stage_log_auth"


class NetRegistrationActivity(models.Model):
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "net_registration_activity"


class LatestRegistrationActivity(models.Model):
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    registered = models.CharField(max_length=50, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "latest_registration_activity"


class Activity(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    operation = models.CharField(max_length=100, blank=True, null=True)
    endpoint = models.CharField(max_length=200, blank=True, null=True)
    result = models.CharField(max_length=100, blank=True, null=True)
    status_code = models.CharField(max_length=10, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    status_code_description = models.CharField(max_length=100, blank=True, null=True)
    request_timestamp = models.DateTimeField(blank=True, null=True)
    request_method = models.CharField(max_length=100, blank=True, null=True)
    execution_time = models.CharField(max_length=50)
    service_name = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "activity"


class ActivityLog(models.Model):
    activity = models.OneToOneField(Activity, models.DO_NOTHING, primary_key=True)
    request_body = models.TextField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "activity_log"


class ComplaintTicketLogs(models.Model):
    id = models.BigAutoField(primary_key=True)
    srn = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    last_updated_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    hold_time = models.BigIntegerField(blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    breached_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_ticket_logs"


class ComplaintsActivity(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaints_activity"


class RecentTicketActivity(models.Model):
    id = models.BigIntegerField(blank=True, primary_key=True)
    srn = models.CharField(max_length=50, blank=True, null=True)
    last_updated_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=10, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    hold_time = models.BigIntegerField(blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    breached_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "recent_ticket_activity"


class ComplaintEmailAudit(models.Model):
    id = models.BigAutoField(primary_key=True)
    srn = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    email_from = models.CharField(max_length=250, blank=True, null=True)
    email_to = models.CharField(max_length=250, blank=True, null=True)
    source = models.CharField(max_length=250, blank=True, null=True)
    cc_user = models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=250, blank=True, null=True)
    message_id = models.CharField(max_length=250, blank=True, null=True)
    agent_name = models.CharField(max_length=250, blank=True, null=True)
    number_of_attachments = models.CharField(max_length=250, blank=True, null=True)
    tenant = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_email_audit"


class MessageStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_id = models.CharField(max_length=150)
    message_id = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "message_status"


class ChannelsReactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    page_id = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    post_id = models.CharField(max_length=100, blank=True, null=True)
    action_type = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "channels_reactions"


class CampaignNotification(models.Model):
    id = models.BigIntegerField(primary_key=True)
    campaign_filter_id = models.BigIntegerField(blank=True, null=True)
    campaign_id = models.CharField(max_length=1000, blank=True, null=True)
    campaign_name = models.CharField(max_length=1000, blank=True, null=True)
    sub_campaign_identifier = models.CharField(max_length=1000, blank=True, null=True)
    sub_campaign_name = models.CharField(max_length=1000, blank=True, null=True)
    run_id = models.IntegerField(blank=True, null=True)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)
    batch_id = models.BigIntegerField(blank=True, null=True)
    batch_identifier = models.CharField(max_length=50, blank=True, null=True)
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    initial_channel_id = models.CharField(max_length=250, blank=True, null=True)
    channel_name = models.CharField(max_length=50, blank=True, null=True)
    message_id = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    notification_status = models.CharField(max_length=50, blank=True, null=True)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    message_timestamp = models.DateTimeField(blank=True, null=True)
    notification_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "campaign_notification"


# llm models
class LlmUpload(models.Model):
    id = models.BigAutoField(primary_key=True)
    services = models.JSONField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.CharField(max_length=100)
    last_updated_at = models.DateTimeField()
    indexing_status = models.CharField(max_length=10)
    vector_ids = models.JSONField(blank=True, null=True)
    user_name = models.CharField(max_length=100)
    languages = models.JSONField(blank=True, null=True)
    tenant = models.CharField(max_length=100)
    file_name = models.CharField(max_length=250, blank=True, null=True)
    object_path = models.CharField(max_length=100, blank=True, null=True)
    object_type = models.CharField(max_length=100)
    website_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "llm_upload"


class CampaignRolled(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    batch_identifier = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "campaign_rolled"


class ServiceStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    service = models.CharField(max_length=100)
    healthz_endpoint = models.CharField(max_length=200)
    healthz_status = models.CharField(max_length=50)
    livez_endpoint = models.CharField(max_length=200)
    livez_status = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "service_status"


class SunshineMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    conversation_id = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sunshine_mapping"


class CtaReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.CharField(max_length=100, blank=True, null=True)
    campaign_name = models.CharField(max_length=100, blank=True, null=True)
    sub_campaign_id = models.CharField(max_length=100, blank=True, null=True)
    run_id = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    channel_id = models.CharField(max_length=100, blank=True, null=True)
    cta_clicked = models.CharField(max_length=100, blank=True, null=True)
    clicked_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    campaign_variants = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    campaign_rolled_timestamp = models.DateTimeField(blank=True, null=True)
    notification_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "cta_report"
        unique_together = (
            (
                "campaign_id",
                "campaign_name",
                "sub_campaign_id",
                "run_id",
                "customer_name",
                "channel",
                "channel_id",
                "cta_clicked",
                "campaign_rolled_timestamp",
                "clicked_timestamp",
                "last_modified_timestamp",
                "campaign_variants",
                "tenant",
            ),
        )


class PikaClientDynamicQueues(models.Model):
    id = models.BigAutoField(primary_key=True)
    consumer_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        managed = False
        db_table = "pika_client_dynamic_queues"
        unique_together = (("consumer_name", "name"),)


class CampaignCtaExclude(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_id = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    batch_id = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campaign_cta_exclude"
        unique_together = (("channel_id", "channel", "batch_id"),)


class BotbuilderProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField()
    lang = models.JSONField()
    channel = models.JSONField()
    env = models.JSONField()
    plugins = models.JSONField()
    release = models.CharField(max_length=20)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = "botbuilder_project"
        unique_together = (("name", "repo_url"),)


class EtbUserDetails(models.Model):
    id = models.FloatField(primary_key=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField()
    is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "etb_user_details"


class EtbUserDetailsOracle(models.Model):
    id = models.FloatField(primary_key=True)
    account_number = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField()
    is_active = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "etb_user_details"


class MessageLogDetails(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    channel_id = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    context = models.CharField(max_length=50, blank=True, null=True)
    event = models.CharField(max_length=50, blank=True, null=True)
    event_type = models.CharField(max_length=50, blank=True, null=True)
    handled = models.CharField(max_length=1, blank=True, null=True)
    intent = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    score = models.DecimalField(max_digits=30, decimal_places=30, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    message_id = models.CharField(max_length=200, blank=True, null=True)
    customer_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'message_log_details'


class StageLogDetails(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_intent = models.CharField(max_length=200, blank=True, null=True)
    transaction_id = models.CharField(max_length=150, blank=True, null=True)
    stage = models.CharField(max_length=100, blank=True, null=True)
    stage_result = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    rmn = models.CharField(max_length=20, blank=True, null=True)
    transaction_code = models.CharField(max_length=10, blank=True, null=True)
    node_id = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    applicable_charges = models.CharField(max_length=100, blank=True, null=True)
    from_account = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'stage_log_details'


class ApiLogDetails(models.Model):
    id = models.BigIntegerField(primary_key=True, blank=False, null=False)
    endpoint = models.CharField(max_length=250, blank=True, null=True)
    channel_id = models.CharField(max_length=150, blank=True, null=True)
    request_id = models.CharField(max_length=150, blank=True, null=True)
    session_id = models.CharField(max_length=50, blank=True, null=True)
    api = models.CharField(max_length=500, blank=True, null=True)
    stage = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    channel = models.CharField(max_length=20, blank=True, null=True)
    internal_reference = models.CharField(max_length=500, blank=True, null=True)
    external_reference = models.CharField(max_length=500, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    exception = models.CharField(max_length=500, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    customer_type = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'api_log_details'


class OnboardingCampaignDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    internal_reference = models.CharField(max_length=100)
    email = models.CharField(max_length=250)
    mobile_number = models.CharField(max_length=250)
    last_modified = models.DateTimeField()
    application_status = models.CharField(max_length=250)
    tenant = models.CharField(max_length=250)
    stage = models.CharField(max_length=250, blank=True, null=True)
    last_action = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'onboarding_campaign_details'
