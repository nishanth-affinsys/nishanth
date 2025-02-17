from django.db import models

# Create your models here.


class ApiRequestLoggingApilogentry(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    remote_address = models.CharField(max_length=20, blank=True, null=True)
    query_params = models.TextField(blank=True, null=True)
    request_body = models.TextField(blank=True, null=True)
    host = models.CharField(max_length=100, blank=True, null=True)
    requested_at = models.DateTimeField()
    status_code = models.SmallIntegerField()
    response_ms = models.IntegerField(blank=True, null=True)
    response_body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "api_request_logging_apilogentry"


class Authentication(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    provider = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "authentication"


class BatchIdentifier(models.Model):
    id = models.BigAutoField(primary_key=True)
    identifier = models.CharField(max_length=80)
    channel_id = models.CharField(max_length=250)
    channel_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "batch_identifier"
        unique_together = (("channel_id", "channel_name", "identifier"),)


class BotInteraction(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    transaction_type = models.CharField(max_length=255, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    remarks = models.CharField(max_length=255, blank=True, null=True)
    interaction = models.ForeignKey("Interaction", models.DO_NOTHING)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "bot_interaction"


class CampaignData(models.Model):
    timestamp = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    profile_id = models.CharField(max_length=250)
    campaign_id = models.IntegerField()
    campaign_name = models.CharField(max_length=250)
    subcampaign_id = models.IntegerField()
    run_id = models.IntegerField()
    batch = models.ForeignKey(BatchIdentifier, models.DO_NOTHING)
    subcampaign_name = models.CharField(max_length=250)
    tenant = models.CharField(max_length=50)
    campaign_identifier = models.CharField(max_length=250, blank=True, null=True)
    created_timestamp = models.DateTimeField()
    subcampaign_identifier = models.CharField(max_length=250, blank=True, null=True)
    interaction = models.ForeignKey(
        "Interaction", models.DO_NOTHING, blank=True, null=True
    )
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campaign_data"


class CampaignDynamicCta(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_id = models.CharField(max_length=250, blank=True, null=True)
    click = models.CharField(max_length=250, blank=True, null=True)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaign_dynamic_cta"


class CategoryAudit(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    category = models.CharField(max_length=20)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)
    channel_information = models.ForeignKey("ChannelInformation", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "category_audit"


class CategoryOptout(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=20)
    channel_information = models.ForeignKey("ChannelInformation", models.DO_NOTHING)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "category_optout"
        unique_together = (("profile", "channel_information", "category"),)


class ChannelInformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)
    is_opted = models.BooleanField()

    class Meta:
        managed = False
        db_table = "channel_information"


class ComplaintInteraction(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.CharField(max_length=255, blank=True, null=True)
    srn = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    interaction = models.ForeignKey("Interaction", models.DO_NOTHING)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_interaction"


class HandoffInteraction(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    agent_session_id = models.CharField(max_length=255, blank=True, null=True)
    agent_id = models.CharField(max_length=255, blank=True, null=True)
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    remarks = models.CharField(max_length=255, blank=True, null=True)
    interaction = models.ForeignKey("Interaction", models.DO_NOTHING)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "handoff_interaction"


class Interaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    cust_id = models.CharField(max_length=255, blank=True, null=True)
    service_type = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    data = models.TextField(blank=True, null=True)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "interaction"


class Linking(models.Model):
    id = models.BigAutoField(primary_key=True)
    link_id = models.CharField(max_length=255)
    profile = models.ForeignKey("Profile", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "linking"


class MessageStatus(models.Model):
    channel_id = models.CharField(max_length=150)
    message_id = models.CharField(primary_key=True, max_length=255)
    channel = models.CharField(max_length=100, blank=True, null=True)
    delivered = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField()
    tenant = models.CharField(max_length=50, blank=True, null=True)
    read = models.CharField(max_length=100, blank=True, null=True)
    sent = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "message_status"


class NotificationData(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    profile_id = models.CharField(max_length=250)
    service_name = models.CharField(max_length=50)
    tenant = models.CharField(max_length=50)
    utter_name = models.CharField(max_length=50)
    message = models.TextField()
    media = models.TextField()
    message_id = models.ForeignKey(
        MessageStatus, models.DO_NOTHING, blank=True, null=True
    )
    status = models.CharField(max_length=50)
    exceptions = models.TextField()
    batch = models.ForeignKey(BatchIdentifier, models.DO_NOTHING)
    delivered = models.CharField(max_length=100, blank=True, null=True)
    read = models.CharField(max_length=100, blank=True, null=True)
    sent = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notification_data"


class PikaClientDynamicExchanges(models.Model):
    id = models.BigAutoField(primary_key=True)
    consumer_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    durable = models.BooleanField()

    class Meta:
        managed = False
        db_table = "pika_client_dynamic_exchanges"
        unique_together = (("consumer_name", "name"),)


class PikaClientDynamicQueues(models.Model):
    id = models.BigAutoField(primary_key=True)
    consumer_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    details = models.TextField()

    class Meta:
        managed = False
        db_table = "pika_client_dynamic_queues"
        unique_together = (("consumer_name", "name"),)


class Profile(models.Model):
    profile_id = models.CharField(primary_key=True, max_length=255)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    is_authenticated = models.BooleanField()
    tenant = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "profile"


class WalletInteraction(models.Model):
    id = models.BigAutoField(primary_key=True)
    channel_name = models.CharField(max_length=255, blank=True, null=True)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=255, blank=True, null=True)
    wallet_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    interaction = models.ForeignKey(Interaction, models.DO_NOTHING)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "wallet_interaction"
