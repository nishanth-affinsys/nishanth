from django.db import models


class CampaignsApprovalcomment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.TextField()
    approval_obj = models.OneToOneField(
        "CampaignsCampaignvariantapproval", models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "campaigns_approvalcomment"


class CampaignsBroadcastreport(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer = models.CharField(max_length=255)
    creative_content = models.ForeignKey(
        "CampaignsCreativecontent", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaigns_broadcastreport"


class CampaignsCampaign(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "campaigns_campaign"


class CampaignsCampaignvariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_variant = models.BooleanField()
    status = models.CharField(max_length=50)
    campaign = models.ForeignKey(CampaignsCampaign, models.DO_NOTHING)
    type = models.CharField(max_length=50)
    archived = models.BooleanField()
    timestamp = models.DateTimeField()
    tenant = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campaigns_campaignvariant"


class CampaignsCampaignvariantapproval(models.Model):
    id = models.BigAutoField(primary_key=True)
    approval_status = models.CharField(max_length=100)
    campaign_variant = models.ForeignKey(CampaignsCampaignvariant, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "campaigns_campaignvariantapproval"


class CampaignsCampaignvariantdetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_recommended_cohorts = models.JSONField()
    product_product_filters = models.JSONField()
    product_cohorts_filter = models.JSONField()
    campaign_variant = models.OneToOneField(CampaignsCampaignvariant, models.DO_NOTHING)
    product_product_list = models.JSONField()
    product_selected_products = models.JSONField()
    user_product_filters = models.JSONField()
    user_recommended_products = models.JSONField()
    user_selected_cohorts = models.JSONField()
    user_user_cohorts = models.JSONField()
    user_user_filters = models.JSONField()
    selected_users = models.JSONField()
    timestamp = models.DateTimeField()
    user_selected_products = models.JSONField()

    class Meta:
        managed = False
        db_table = "campaigns_campaignvariantdetail"


class CampaignsCampaignvariantusers(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_variant = models.ForeignKey(CampaignsCampaignvariant, models.DO_NOTHING)
    user_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaigns_campaignvariantusers"


class CampaignsChannelcontent(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.JSONField()

    class Meta:
        managed = False
        db_table = "campaigns_channelcontent"


class CampaignsCreativecontent(models.Model):
    id = models.BigAutoField(primary_key=True)
    content_type = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    campaign_variant = models.ForeignKey(CampaignsCampaignvariant, models.DO_NOTHING)
    channel_content = models.OneToOneField(CampaignsChannelcontent, models.DO_NOTHING)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaigns_creativecontent"


class CampaignsCreativecontentlocation(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=255)
    creative_content = models.ForeignKey(
        CampaignsCreativecontent, models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaigns_creativecontentlocation"


class CampaignsPullbroadcastreport(models.Model):
    broadcastreport_ptr = models.OneToOneField(
        CampaignsBroadcastreport, models.DO_NOTHING, primary_key=True
    )
    pull_broadcast_timeline = models.ForeignKey(
        "CampaignsPullbroadcasttimeline", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "campaigns_pullbroadcastreport"


class CampaignsPullbroadcasttimeline(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField()
    campaign_variant = models.ForeignKey(CampaignsCampaignvariant, models.DO_NOTHING)
    is_active = models.BooleanField()
    end_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "campaigns_pullbroadcasttimeline"


class CampaignsPushbroadcastreport(models.Model):
    broadcastreport_ptr = models.OneToOneField(
        CampaignsBroadcastreport, models.DO_NOTHING, primary_key=True
    )
    channel = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    initialized = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    read = models.DateTimeField(blank=True, null=True)
    delivered = models.DateTimeField(blank=True, null=True)
    clicked = models.DateTimeField(blank=True, null=True)
    push_broadcast_timeline = models.ForeignKey(
        "CampaignsPushbroadcasttimeline", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "campaigns_pushbroadcastreport"


class CampaignsPushbroadcasttimeline(models.Model):
    id = models.BigAutoField(primary_key=True)
    frequency = models.IntegerField()
    recurrence_interval = models.IntegerField()
    start_date = models.DateTimeField()
    completed_count = models.IntegerField()
    last_timestamp = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField()
    campaign_variant = models.ForeignKey(
        CampaignsCampaignvariant, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "campaigns_pushbroadcasttimeline"


class CampaignsBroadcastusermessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    message_id = models.CharField(max_length=100, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    campaign_variant = models.ForeignKey(
        "CampaignsCampaignvariant", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "campaigns_broadcastusermessage"


# NEW campaign models
class Campaign(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_modified = models.DateTimeField()
    campaign_tags = models.TextField(blank=True, null=True)
    archived = models.BooleanField()
    created_timestamp = models.DateTimeField()
    campaign_category = models.CharField(max_length=1000, blank=True, null=True)
    campaign_description = models.CharField(max_length=1000, blank=True, null=True)
    campaign_id = models.CharField(max_length=1000, blank=True, null=True)
    campaign_name = models.CharField(max_length=1000, blank=True, null=True)
    campaign_type = models.CharField(max_length=1000, blank=True, null=True)
    parent = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=1000, blank=True, null=True)
    tenant = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campaign"


class CampaignUserLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, models.DO_NOTHING)
    subcampaign = models.ForeignKey("SubCampaignDetail", models.DO_NOTHING)
    group_id = models.CharField(max_length=32)
    user_slots = models.TextField(blank=True, null=True)
    profile_id = models.CharField(max_length=1000, blank=True, null=True)
    segment_name = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "campaign_user_log"


class SubCampaignContentSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_time = models.DateTimeField(blank=True, null=True)
    sub_campaign = models.ForeignKey("SubCampaignDetail", models.DO_NOTHING)
    event_end_value_occurence = models.IntegerField(blank=True, null=True)
    event_end_value_time = models.DateTimeField(blank=True, null=True)
    repeat_interval = models.IntegerField(blank=True, null=True)
    repeats_on = models.TextField(blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    relativeto = models.ForeignKey(
        "SubCampaignDetail",
        models.DO_NOTHING,
        related_name="subcampaigncontentschedule_relativeto_set",
        blank=True,
        null=True,
    )
    event_end_type = models.CharField(max_length=1000, blank=True, null=True)
    event_schedule = models.CharField(max_length=1000, blank=True, null=True)
    event_type = models.CharField(max_length=1000, blank=True, null=True)
    schedule_type = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_content_schedule"


class SubCampaignContentSegment(models.Model):
    id = models.BigAutoField(primary_key=True)
    cj_id = models.IntegerField(blank=True, null=True)
    channels = models.TextField(blank=True, null=True)
    channel_instance = models.CharField(max_length=1000, blank=True, null=True)
    cj_name = models.CharField(max_length=1000, blank=True, null=True)
    language = models.CharField(max_length=1000, blank=True, null=True)
    segment_name = models.CharField(max_length=1000, blank=True, null=True)
    task_id = models.CharField(max_length=1000, blank=True, null=True)
    utter_name = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_content_segment"


class SubCampaignDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_primary = models.BooleanField()
    campaign = models.ForeignKey(Campaign, models.DO_NOTHING)
    created_timestamp = models.DateTimeField()
    last_modified = models.DateTimeField()
    description = models.CharField(max_length=1000, blank=True, null=True)
    identifier = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    status = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_detail"


class SubCampaignRun(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    sub_campaign = models.ForeignKey(SubCampaignDetail, models.DO_NOTHING)
    campaign = models.ForeignKey(Campaign, models.DO_NOTHING)
    run_id = models.IntegerField()
    notification_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_run"


class SubCampaignSegmentSchedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    sub_campaign = models.ForeignKey(SubCampaignDetail, models.DO_NOTHING)
    interval = models.IntegerField()
    type = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_segment_schedule"


class SubCampaignTarget(models.Model):
    id = models.BigAutoField(primary_key=True)
    content_segment = models.ForeignKey(SubCampaignContentSegment, models.DO_NOTHING)
    sub_campaign = models.ForeignKey(SubCampaignDetail, models.DO_NOTHING)
    target_segment = models.ForeignKey("SubCampaignTargetSegment", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "sub_campaign_target"


class SubCampaignTargetSegment(models.Model):
    id = models.BigAutoField(primary_key=True)
    csv_upload = models.BooleanField()
    cj_id = models.CharField(max_length=1000, blank=True, null=True)
    cj_name = models.CharField(max_length=1000, blank=True, null=True)
    filename = models.CharField(max_length=1000, blank=True, null=True)
    filetype = models.CharField(max_length=1000, blank=True, null=True)
    segment_name = models.CharField(max_length=1000, blank=True, null=True)
    task_id = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_target_segment"


class SubCampaignUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    campaign_run = models.ForeignKey(SubCampaignRun, models.DO_NOTHING)
    target_segment = models.ForeignKey(SubCampaignTargetSegment, models.DO_NOTHING)
    user_slots = models.TextField(blank=True, null=True)
    channel = models.CharField(max_length=1000, blank=True, null=True)
    profile_id = models.CharField(max_length=1000, blank=True, null=True)
    segment_name = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sub_campaign_user"


# notification models


class NotificationBatch(models.Model):
    id = models.BigAutoField(primary_key=True)
    identifier = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notification_batch"


class NotificationRolled(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    channel_id = models.CharField(max_length=250, blank=True, null=True)
    channel_name = models.CharField(max_length=50, blank=True, null=True)
    service_name = models.CharField(max_length=50, blank=True, null=True)
    utter_name = models.CharField(max_length=50, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True, null=True)
    batch = models.ForeignKey(NotificationBatch, models.DO_NOTHING)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    media = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "notification_rolled"


class NotificationStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    message_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    notification = models.ForeignKey(NotificationRolled, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "notification_status"
