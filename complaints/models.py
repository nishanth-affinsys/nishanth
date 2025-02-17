from django.db import models


class ComplaintCategory(models.Model):
    category_id = models.CharField(unique=True, max_length=50)
    category_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_category"


class ComplaintLabel(models.Model):
    label_id = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    severity = models.IntegerField(blank=True, null=True)
    tat = models.IntegerField(blank=True, null=True)
    internal_tat = models.IntegerField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_label"
        unique_together = (("name", "value"),)


class ComplaintTicket(models.Model):
    srn = models.CharField(unique=True, max_length=50)
    summary = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    creation_time = models.DateTimeField()
    last_updated_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=10)
    severity_score = models.IntegerField(blank=True, null=True)
    norm_severity_score = models.IntegerField(blank=True, null=True)
    tat_target = models.IntegerField(blank=True, null=True)
    hold_time = models.PositiveBigIntegerField()
    internal_tat_target = models.IntegerField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(ComplaintCategory, models.DO_NOTHING)
    reporter = models.ForeignKey(
        "ComplaintUser",
        models.DO_NOTHING,
        related_name="reporter",
    )
    submitter = models.ForeignKey(
        "ComplaintUser",
        models.DO_NOTHING,
        related_name="submitter",
    )
    assignee = models.ForeignKey(
        "ComplaintUser",
        models.DO_NOTHING,
        related_name="assignee",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "complaint_ticket"


class ComplaintTicketattachment(models.Model):
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    bucket_name = models.CharField(max_length=200, blank=True, null=True)
    obj_path = models.CharField(max_length=254, blank=True, null=True)
    file_extension = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    log_timestamp = models.DateTimeField()
    ticket = models.ForeignKey(ComplaintTicket, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "complaint_ticketattachment"


class ComplaintTicketcomment(models.Model):
    comment = models.TextField()
    timestamp = models.DateTimeField()
    is_system_generated = models.BooleanField()
    is_public = models.BooleanField()
    attachment = models.ForeignKey(
        ComplaintTicketattachment, models.DO_NOTHING, blank=True, null=True
    )
    ticket = models.ForeignKey(ComplaintTicket, models.DO_NOTHING)
    user = models.ForeignKey("ComplaintUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "complaint_ticketcomment"


class ComplaintTicketlabelselector(models.Model):
    label = models.ForeignKey(ComplaintLabel, models.DO_NOTHING)
    ticket = models.ForeignKey(ComplaintTicket, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "complaint_ticketlabelselector"
        unique_together = (("ticket", "label"),)


class ComplaintTicketusermap(models.Model):
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    ticket = models.ForeignKey(ComplaintTicket, models.DO_NOTHING)
    user = models.ForeignKey("ComplaintUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "complaint_ticketusermap"
        unique_together = (("ticket", "user"),)


class ComplaintUser(models.Model):
    user_id = models.CharField(unique=True, max_length=50)
    user_name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50, blank=True, null=True)
    is_supervisor = models.BooleanField()

    class Meta:
        managed = False
        db_table = "complaint_user"


class ComplaintUsercategorymap(models.Model):
    category = models.ForeignKey(ComplaintCategory, models.DO_NOTHING)
    user = models.ForeignKey(ComplaintUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "complaint_usercategorymap"
        unique_together = (("user", "category"),)


class ComplaintUserlabelselector(models.Model):
    label = models.ForeignKey(ComplaintLabel, models.DO_NOTHING)
    user = models.ForeignKey(ComplaintUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "complaint_userlabelselector"
        unique_together = (("user", "label"),)
