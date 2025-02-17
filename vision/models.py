from django.db import models


class StageLogFace(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    internal_reference = models.CharField(max_length=500, blank=True, null=True)
    external_reference = models.CharField(max_length=500, blank=True, null=True)
    channel_code = models.CharField(max_length=20, blank=True, null=True)
    object_path = models.CharField(max_length=1000, blank=True, null=True)
    threshold = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )
    user_id = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.CharField(max_length=50, blank=True, null=True)
    matching_status = models.BooleanField(blank=True, null=True)
    age_lower_limit = models.IntegerField(blank=True, null=True)
    age_upper_limit = models.IntegerField(blank=True, null=True)
    blur_present = models.BooleanField(blank=True, null=True)
    blur_threshold = models.IntegerField(blank=True, null=True)
    face_detection_score = models.FloatField(blank=True, null=True)
    face_detection_threshold = models.FloatField(blank=True, null=True)
    face_verification_score = models.FloatField(blank=True, null=True)
    face_verification_threshold = models.FloatField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    gradient_score = models.FloatField(blank=True, null=True)
    image_quality_final = models.CharField(max_length=100)
    is_face_detected = models.BooleanField(blank=True, null=True)
    is_face_verified = models.BooleanField(blank=True, null=True)
    laplacian_score = models.FloatField(blank=True, null=True)
    noise_present = models.BooleanField(blank=True, null=True)
    noise_threshold = models.IntegerField(blank=True, null=True)
    total_faces_detected = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stage_log_face"


class StageLogForgery(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    internal_reference = models.CharField(max_length=500, blank=True, null=True)
    external_reference = models.CharField(max_length=500, blank=True, null=True)
    channel_code = models.CharField(max_length=20, blank=True, null=True)
    object_path = models.CharField(max_length=1000, blank=True, null=True)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    document_class = models.CharField(max_length=50, blank=True, null=True)
    prediction_score = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stage_log_forgery"


class StageLogOcr(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    internal_reference = models.CharField(max_length=500, blank=True, null=True)
    external_reference = models.CharField(max_length=500, blank=True, null=True)
    channel_code = models.CharField(max_length=20, blank=True, null=True)
    object_path = models.CharField(max_length=1000, blank=True, null=True)
    parser_code = models.CharField(max_length=50)
    user_id = models.CharField(max_length=100, blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=50, blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)
    blur_present = models.BooleanField(blank=True, null=True)
    blur_threshold = models.IntegerField(blank=True, null=True)
    gradient_score = models.FloatField(blank=True, null=True)
    image_quality_final = models.CharField(max_length=100)
    image_type_final = models.CharField(max_length=100)
    image_type_score = models.IntegerField(blank=True, null=True)
    image_type_threshold = models.IntegerField(blank=True, null=True)
    is_above_threshold = models.BooleanField(blank=True, null=True)
    laplacian_score = models.FloatField(blank=True, null=True)
    noise_present = models.BooleanField(blank=True, null=True)
    noise_threshold = models.IntegerField(blank=True, null=True)
    parsing_score = models.FloatField(blank=True, null=True)
    parsing_threshold = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "stage_log_ocr"
