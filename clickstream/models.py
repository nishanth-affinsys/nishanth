from django.db import models


class ClickstreamAction(models.Model):
    id = models.BigAutoField(primary_key=True)
    action_type = models.CharField(max_length=1500)
    location = models.CharField(max_length=1500, blank=True, null=True)
    redirect_to = models.CharField(max_length=1500, blank=True, null=True)
    click_element_type = models.CharField(max_length=1500, blank=True, null=True)
    click_element_href = models.CharField(max_length=1500, blank=True, null=True)
    click_element_key = models.CharField(max_length=1500, blank=True, null=True)
    click_element_value = models.CharField(max_length=1500, blank=True, null=True)
    total_clicks_on_page = models.CharField(max_length=1500, blank=True, null=True)
    total_clicks = models.CharField(max_length=1500, blank=True, null=True)
    time_spent_on_page = models.IntegerField(blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()
    redirect_from = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "clickstream_action"


class ClickstreamBrowser(models.Model):
    id = models.BigAutoField(primary_key=True)
    browser_family = models.CharField(max_length=1500, blank=True, null=True)
    browser_type = models.CharField(max_length=1500, blank=True, null=True)
    browser_name = models.CharField(max_length=1500, blank=True, null=True)
    browser_version = models.CharField(max_length=1500, blank=True, null=True)
    language = models.CharField(max_length=1500, blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "clickstream_browser"


class ClickstreamDevice(models.Model):
    id = models.BigAutoField(primary_key=True)
    device_type = models.CharField(max_length=1500, blank=True, null=True)
    device_brand = models.CharField(max_length=1500, blank=True, null=True)
    device_model = models.CharField(max_length=1500, blank=True, null=True)
    device_screen_resolution = models.CharField(max_length=1500, blank=True, null=True)
    device_os_name = models.CharField(max_length=1500, blank=True, null=True)
    device_os_version = models.CharField(max_length=1500, blank=True, null=True)
    device_price_range = models.CharField(max_length=1500, blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "clickstream_device"


class ClickstreamGeneralrecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    visitor_type = models.CharField(max_length=1500, blank=True, null=True)
    referrer_type = models.CharField(max_length=1500, blank=True, null=True)
    referrer_name = models.CharField(max_length=1500, blank=True, null=True)
    referrer_url = models.CharField(max_length=1500, blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "clickstream_generalrecord"


class ClickstreamIpinformation(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip_address = models.CharField(max_length=1500, blank=True, null=True)
    network_domain = models.CharField(max_length=1500, blank=True, null=True)
    internet_service_provider = models.CharField(max_length=1500, blank=True, null=True)
    continent = models.CharField(max_length=1500, blank=True, null=True)
    country = models.CharField(max_length=1500, blank=True, null=True)
    city = models.CharField(max_length=1500, blank=True, null=True)
    region = models.CharField(max_length=1500, blank=True, null=True)
    location = models.CharField(max_length=1500, blank=True, null=True)
    latitude = models.CharField(max_length=1500, blank=True, null=True)
    longitude = models.CharField(max_length=1500, blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "clickstream_ipinformation"


class ClickstreamPageinfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    page_url = models.CharField(max_length=1500, blank=True, null=True)
    page_title = models.CharField(max_length=1500, blank=True, null=True)
    record = models.ForeignKey(
        "ClickstreamRecord", models.DO_NOTHING, blank=True, null=True
    )
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "clickstream_pageinfo"


class ClickstreamRecord(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    session_id = models.CharField(max_length=1500, blank=True, null=True)
    user_identifier = models.ForeignKey(
        "ClickstreamUseridentifier", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "clickstream_record"


class ClickstreamUseridentifier(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=1500, blank=True, null=True)
    browser_id = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "clickstream_useridentifier"
