from django.db import models


class Schedule(models.Model):
    id = models.BigAutoField(primary_key=True)
    schedule_name = models.CharField(max_length=100)
    dashboard_name = models.TextField()
    chart_name = models.TextField()
    recipient_name = models.TextField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    schedule_type = models.CharField(max_length=20)
    schedule_time = models.CharField(max_length=20)
    day = models.TextField(blank=True, null=True)
    end_time = models.CharField(max_length=10, blank=True, null=True)
    starts_on = models.DateTimeField(blank=True, null=True)
    ends_on = models.DateTimeField(blank=True, null=True)
    from_timerange = models.DateTimeField(blank=True, null=True)
    to_timerange = models.DateTimeField(blank=True, null=True)
    occurrences = models.IntegerField(blank=True, null=True)
    tenant = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField()
    last_modified_timestamp = models.DateTimeField()
    abort_reason = models.CharField(max_length=100, blank=True, null=True)
    time_zone = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "schedule"
