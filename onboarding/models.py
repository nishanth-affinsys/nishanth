from django.db import models


class ActionConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    action_code = models.CharField(max_length=100)
    action_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "action_config"
        unique_together = (
            ("tenant", "action_code", "action_name"),
            ("tenant", "action_code"),
        )


class AgentBranchConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=50)
    branch_type = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    agent_uuid = models.CharField(max_length=255, blank=True, null=True)
    agent_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "agent_branch_config"
        unique_together = (
            (
                "tenant",
                "agent_uuid",
                "agent_name",
                "provider",
                "branch_code",
                "branch_type",
                "branch_name",
            ),
        )


class AgentRoleConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    agent_uuid = models.CharField(max_length=255, blank=True, null=True)
    agent_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    role = models.CharField(max_length=200)
    role_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "agent_role_config"
        unique_together = (
            ("tenant", "agent_uuid", "agent_name", "provider", "role", "role_name"),
        )


class BranchConfiguration(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=50)
    branch_type = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    branch_details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "branch_configuration"
        unique_together = (
            ("tenant", "branch_code", "branch_type"),
            ("tenant", "branch_code"),
            ("tenant", "branch_code", "branch_type", "branch_name"),
        )


class EmailReceivers(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    sm_sp = models.CharField(max_length=50)
    agent = models.CharField(max_length=50, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "email_receivers"


class EtbProcessTarget(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    actor = models.CharField(max_length=50)
    process_mode = models.CharField(max_length=50)
    process = models.ForeignKey("ProcessMapping", models.DO_NOTHING)
    product_category = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "etb_process_target"


class FileReferenceManagementRt(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    external_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField()
    screen_name = models.CharField(max_length=150, blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)
    bucket_name = models.CharField(max_length=200, blank=True, null=True)
    obj_path = models.CharField(max_length=254, blank=True, null=True)
    internal_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    external_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    file_extension = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    upload_timestamp = models.DateTimeField(blank=True, null=True)
    uploaded_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "file_reference_management_rt"


class FileReferenceManagementSp(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    external_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField()
    screen_name = models.CharField(max_length=150, blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)
    bucket_name = models.CharField(max_length=200, blank=True, null=True)
    obj_path = models.CharField(max_length=254, blank=True, null=True)
    internal_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    external_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    file_extension = models.CharField(max_length=50, blank=True, null=True)
    file_size = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    upload_timestamp = models.DateTimeField(blank=True, null=True)
    uploaded_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "file_reference_management_sp"


class OtpCounter(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=254)
    request_by_uuid = models.CharField(max_length=254)
    request_by_username = models.CharField(max_length=254)
    request_timestamp = models.CharField(max_length=254)
    phone = models.CharField(max_length=20)
    otp_request_id = models.CharField(max_length=254)
    otp_expiry = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "otp_counter"
        unique_together = (
            (
                "tenant",
                "request_by_uuid",
                "request_by_username",
                "request_timestamp",
                "phone",
                "otp_request_id",
                "otp_expiry",
            ),
        )


class ProcessMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    process_name = models.CharField(max_length=255)
    process_list = models.TextField()

    class Meta:
        managed = False
        db_table = "process_mapping"


class ProcessTarget(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    product_key = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    process_mode = models.CharField(max_length=50)
    process = models.ForeignKey(ProcessMapping, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "process_target"


class QueueActionMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    queue_code = models.CharField(max_length=200)
    queue_name = models.CharField(max_length=200)
    action_code = models.CharField(max_length=200)
    action_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "queue_action_mapping"


class QueueConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    queue_code = models.CharField(max_length=100)
    queue_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "queue_config"
        unique_together = (
            ("tenant", "queue_code", "queue_name"),
            ("tenant", "queue_code"),
        )


class RetailProductMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    product_key = models.CharField(unique=True, max_length=50)
    product_name = models.CharField(max_length=50)
    product_icon_path = models.TextField(blank=True, null=True)
    product_channel = models.CharField(max_length=254, blank=True, null=True)
    scheme_description = models.TextField(blank=True, null=True)
    documents_required = models.TextField(blank=True, null=True)
    key_fact_path = models.TextField(blank=True, null=True)
    applicable_gender = models.CharField(max_length=50, blank=True, null=True)
    scheme_code = models.CharField(max_length=50)
    scheme_type = models.CharField(max_length=50)
    gl_subhead_code = models.CharField(max_length=75)
    customer_nationality = models.CharField(max_length=75, blank=True, null=True)
    account_currency = models.CharField(max_length=50, blank=True, null=True)
    annual_income = models.CharField(max_length=75, blank=True, null=True)
    account_type = models.CharField(max_length=50, blank=True, null=True)
    retail_account_category = models.CharField(max_length=254, blank=True, null=True)
    retail_account_type = models.CharField(max_length=75, blank=True, null=True)
    process_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "retail_product_mapping"
        unique_together = (
            (
                "tenant",
                "product_key",
                "product_name",
                "product_channel",
                "account_type",
                "applicable_gender",
                "scheme_code",
                "scheme_type",
                "gl_subhead_code",
                "account_currency",
                "annual_income",
                "retail_account_category",
                "retail_account_type",
            ),
        )


class RoutingLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    route_name = models.CharField(max_length=255, blank=True, null=True)
    from_branch_code = models.CharField(max_length=50, blank=True, null=True)
    from_role_code = models.CharField(max_length=100, blank=True, null=True)
    from_queue_code = models.CharField(max_length=100, blank=True, null=True)
    ac_code = models.CharField(max_length=255, blank=True, null=True)
    to_branch_code = models.CharField(max_length=50, blank=True, null=True)
    to_role_code = models.CharField(max_length=100, blank=True, null=True)
    to_queue_code = models.CharField(max_length=100, blank=True, null=True)
    increase_version = models.CharField(max_length=1, blank=True, null=True)
    customer_type = models.CharField(max_length=25, blank=True, null=True)
    condition_priority = models.CharField(max_length=25, blank=True, null=True)
    route_condition = models.ForeignKey("RoutingRules", models.DO_NOTHING)
    product = models.CharField(max_length=255, blank=True, null=True)
    call_cbs = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "routing_log"
        unique_together = (
            (
                "tenant",
                "from_branch_code",
                "from_role_code",
                "from_queue_code",
                "product",
                "ac_code",
                "to_branch_code",
                "to_role_code",
                "to_queue_code",
                "route_condition",
                "condition_priority",
                "increase_version",
                "customer_type",
            ),
        )


class RoutingRules(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    route_condition_name = models.CharField(max_length=200, blank=True, null=True)
    route_condition = models.TextField()

    class Meta:
        managed = False
        db_table = "routing_rules"


class RtApiStage(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    completion_status = models.CharField(max_length=1)
    pending_functions = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rt_api_stage"


class RtApplicationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    action_perform_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rt_application_log"


class RtAuditComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    action_code = models.CharField(max_length=100, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rt_audit_comments"


class RtRoutingLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    route_dump = models.TextField(blank=True, null=True)
    condition_dump = models.TextField(blank=True, null=True)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    perform_timestamp = models.DateTimeField(blank=True, null=True)
    performed_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rt_routing_log"


class SingleCifRetailData(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_action = models.CharField(max_length=255, blank=True, null=True)
    last_action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    last_action_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_action_performed_by_uuid = models.CharField(
        max_length=255, blank=True, null=True
    )
    last_action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_by_provider = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    rejected_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    rejected_by = models.CharField(max_length=255, blank=True, null=True)
    rejected_by_provider = models.CharField(max_length=255, blank=True, null=True)
    rejected_timestamp = models.DateTimeField(blank=True, null=True)
    discarded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    discarded_by = models.CharField(max_length=255, blank=True, null=True)
    discarded_by_provider = models.CharField(max_length=255, blank=True, null=True)
    discarded_timestamp = models.DateTimeField(blank=True, null=True)
    submit_status = models.CharField(max_length=1, blank=True, null=True)
    application_status = models.CharField(max_length=75, blank=True, null=True)
    display_in_queue = models.CharField(max_length=1, blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    common_data = models.TextField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    primary_contact_number = models.CharField(max_length=50, blank=True, null=True)
    primary_email_address = models.CharField(max_length=254, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    preferred_id_type = models.CharField(max_length=100, blank=True, null=True)
    preferred_id_number = models.CharField(max_length=100, blank=True, null=True)
    cif = models.CharField(max_length=20, blank=True, null=True)
    account_num1 = models.CharField(max_length=100, blank=True, null=True)
    account_num2 = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    onboarding_channel = models.CharField(max_length=100)
    created_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    created_at_branch_type = models.CharField(max_length=25, blank=True, null=True)
    application_branch_code = models.CharField(max_length=25, blank=True, null=True)
    application_branch_type = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_type = models.CharField(max_length=25, blank=True, null=True)
    role_code = models.CharField(max_length=25, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    kyc_reference = models.CharField(max_length=100, blank=True, null=True)
    file_upload_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "single_cif_retail_data"
        unique_together = (
            ("tenant", "external_reference"),
            ("tenant", "internal_reference", "version_no"),
            ("tenant", "internal_reference"),
        )


class SingleCifRetailDataHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    internal_reference = models.CharField(
        unique=True, max_length=50, blank=True, null=True
    )
    version_no = models.IntegerField(blank=True, null=True)
    external_reference = models.CharField(
        unique=True, max_length=100, blank=True, null=True
    )
    archive_data = models.TextField(blank=True, null=True)
    archived_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    archived_by = models.CharField(max_length=255, blank=True, null=True)
    archived_timestamp = models.DateTimeField(blank=True, null=True)
    archived_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "single_cif_retail_data_history"
        unique_together = (("internal_reference", "version_no"),)


class SingleCifSpData(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_action = models.CharField(max_length=255, blank=True, null=True)
    last_action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    last_action_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_action_performed_by_uuid = models.CharField(
        max_length=255, blank=True, null=True
    )
    last_action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_by_provider = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    rejected_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    rejected_by = models.CharField(max_length=255, blank=True, null=True)
    rejected_by_provider = models.CharField(max_length=255, blank=True, null=True)
    rejected_timestamp = models.DateTimeField(blank=True, null=True)
    discarded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    discarded_by = models.CharField(max_length=255, blank=True, null=True)
    discarded_by_provider = models.CharField(max_length=255, blank=True, null=True)
    discarded_timestamp = models.DateTimeField(blank=True, null=True)
    submit_status = models.CharField(max_length=1, blank=True, null=True)
    record_status = models.CharField(max_length=75, blank=True, null=True)
    display_in_queue = models.CharField(max_length=1, blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    common_data = models.TextField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    primary_contact_number = models.CharField(max_length=50, blank=True, null=True)
    primary_email_address = models.CharField(max_length=254, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_representative_name = models.CharField(
        max_length=100, blank=True, null=True
    )
    cif = models.CharField(max_length=20, blank=True, null=True)
    account_num1 = models.CharField(max_length=100, blank=True, null=True)
    account_num2 = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    onboarding_channel = models.CharField(max_length=100)
    created_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    created_at_branch_type = models.CharField(max_length=25, blank=True, null=True)
    application_branch_code = models.CharField(max_length=25, blank=True, null=True)
    application_branch_type = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_type = models.CharField(max_length=25, blank=True, null=True)
    role_code = models.CharField(max_length=25, blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    kyc_reference = models.CharField(max_length=100, blank=True, null=True)
    file_upload_status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "single_cif_sp_data"
        unique_together = (
            ("tenant", "external_reference"),
            ("tenant", "internal_reference", "version_no"),
            ("tenant", "internal_reference"),
        )


class SingleCifSpDataHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    internal_reference = models.CharField(
        unique=True, max_length=100, blank=True, null=True
    )
    version_no = models.IntegerField(blank=True, null=True)
    external_reference = models.CharField(
        unique=True, max_length=100, blank=True, null=True
    )
    archive_data = models.TextField(blank=True, null=True)
    archived_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    archived_by = models.CharField(max_length=255, blank=True, null=True)
    archived_timestamp = models.DateTimeField(blank=True, null=True)
    archived_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "single_cif_sp_data_history"
        unique_together = (("internal_reference", "version_no"),)


class SpApiStage(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    completion_status = models.CharField(max_length=1)
    pending_functions = models.TextField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sp_api_stage"


class SpApplicationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    action_perform_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sp_application_log"


class SpAuditComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    action_code = models.CharField(max_length=100, blank=True, null=True)
    branch_code = models.CharField(max_length=100, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sp_audit_comments"


class SpProductMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    product_key = models.CharField(unique=True, max_length=50)
    product_name = models.CharField(max_length=50)
    product_icon_path = models.TextField(blank=True, null=True)
    product_channel = models.CharField(max_length=254, blank=True, null=True)
    scheme_description = models.TextField(blank=True, null=True)
    documents_required = models.TextField(blank=True, null=True)
    key_fact_path = models.TextField(blank=True, null=True)
    account_type = models.CharField(max_length=50)
    applicable_gender = models.CharField(max_length=50, blank=True, null=True)
    scheme_code = models.CharField(max_length=50)
    scheme_type = models.CharField(max_length=50)
    gl_subhead_code = models.CharField(max_length=75)
    customer_nationality = models.CharField(max_length=75, blank=True, null=True)
    account_currency = models.CharField(max_length=50)
    account_turnover = models.CharField(max_length=254, blank=True, null=True)
    process_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sp_product_mapping"
        unique_together = (
            (
                "tenant",
                "product_key",
                "product_name",
                "product_channel",
                "account_type",
                "applicable_gender",
                "scheme_code",
                "scheme_type",
                "gl_subhead_code",
                "customer_nationality",
                "account_currency",
                "account_turnover",
            ),
        )


class SpRoutingLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    route_dump = models.TextField(blank=True, null=True)
    condition_dump = models.TextField(blank=True, null=True)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    perform_timestamp = models.DateTimeField(blank=True, null=True)
    performed_by_provider = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sp_routing_log"


class UserBranchConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    branch_code = models.CharField(max_length=50)
    branch_type = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    user_uuid = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    deleted_at = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_deleted = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = "user_branch_config"
        unique_together = (
            (
                "tenant",
                "user_uuid",
                "username",
                "provider",
                "email",
                "branch_code",
                "branch_type",
                "branch_name",
                "is_deleted",
            ),
        )


class UserRoleConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    user_uuid = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    role = models.CharField(max_length=200)
    role_name = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = "user_role_config"
        unique_together = (
            ("tenant", "user_uuid", "username", "provider", "role", "role_name"),
        )


# onboarding views


class DetailedReportTableRt(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    account_num1 = models.CharField(max_length=100, blank=True, null=True)
    account_num2 = models.CharField(max_length=100, blank=True, null=True)
    created_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    onboarding_channel = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by = models.CharField(max_length=50, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "detailed_report_table_rt"


class DetailedReportTableSp(models.Model):
    id = models.BigAutoField(primary_key=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    account_num1 = models.CharField(max_length=100, blank=True, null=True)
    account_num2 = models.CharField(max_length=100, blank=True, null=True)
    created_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=50, blank=True, null=True)
    onboarding_channel = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by = models.CharField(max_length=50, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "detailed_report_table_sp"


# kyc  models


class FileReferenceManagementKyc(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField()
    screen_name = models.CharField(max_length=150, blank=True, null=True)
    key_name = models.CharField(max_length=100, blank=True, null=True)
    bucket_name = models.CharField(max_length=200, blank=True, null=True)
    obj_path = models.CharField(max_length=254, blank=True, null=True)
    internal_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    external_file_name_reference = models.CharField(
        max_length=100, blank=True, null=True
    )
    file_extension = models.CharField(max_length=50, blank=True, null=True)
    content_type = models.CharField(max_length=50, blank=True, null=True)
    uploaded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    uploaded_by = models.CharField(max_length=255, blank=True, null=True)
    uploaded_by_provider = models.CharField(max_length=255, blank=True, null=True)
    upload_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "file_reference_management_kyc"


class KycApplicationLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    action_perform_provider = models.CharField(max_length=255, blank=True, null=True)
    action_performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "kyc_application_log"


class KycAuditComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    action_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "kyc_audit_comments"


class KycDocuments(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=100)
    kyc_reference = models.CharField(max_length=255)
    kyc_number = models.CharField(max_length=255)
    version_no = models.CharField(max_length=50)
    doc_type = models.CharField(max_length=255)
    doc_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    class Meta:
        managed = False
        db_table = "kyc_documents"
        unique_together = (
            (
                "tenant",
                "kyc_reference",
                "kyc_number",
                "version_no",
                "doc_type",
                "doc_number",
            ),
        )


class KycHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    kyc_reference = models.CharField(max_length=100)
    version_no = models.CharField(max_length=50)
    archive_data = models.CharField(max_length=100)
    archived_by_uuid = models.CharField(max_length=100)
    archived_by = models.CharField(max_length=100)
    archived_by_provider = models.CharField(max_length=100)
    archived_timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "kyc_history"
        unique_together = (
            (
                "kyc_reference",
                "version_no",
                "archive_data",
                "archived_by_uuid",
                "archived_by",
                "archived_by_provider",
            ),
        )


class KycMaster(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=100)
    internal_reference = models.CharField(max_length=255)
    kyc_number = models.CharField(max_length=255)
    version_no = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=100)
    primary_email_address = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    additional_data = models.TextField(blank=True, null=True)
    kyc_status = models.CharField(max_length=50, blank=True, null=True)
    kyc_level = models.CharField(max_length=100, blank=True, null=True)
    kyc_level_updated_at = models.DateTimeField(blank=True, null=True)
    common_data = models.TextField(blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_by_provider = models.CharField(max_length=255, blank=True, null=True)
    created_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    discarded_by = models.CharField(max_length=255, blank=True, null=True)
    discarded_by_provider = models.CharField(max_length=255, blank=True, null=True)
    discarded_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    discarded_timestamp = models.DateTimeField(blank=True, null=True)
    display_in_queue = models.CharField(max_length=1, blank=True, null=True)
    last_action = models.CharField(max_length=255, blank=True, null=True)
    last_action_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    last_action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    last_action_performed_by_uuid = models.CharField(
        max_length=255, blank=True, null=True
    )
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by_provider = models.CharField(max_length=255, blank=True, null=True)
    last_modified_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    rejected_by = models.CharField(max_length=255, blank=True, null=True)
    rejected_by_provider = models.CharField(max_length=255, blank=True, null=True)
    rejected_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    rejected_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_by_provider = models.CharField(max_length=255, blank=True, null=True)
    submit_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    channel = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    kyc_expires_at = models.DateTimeField(blank=True, null=True)
    product_id = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "kyc_master"
        unique_together = (
            (
                "tenant",
                "internal_reference",
                "version_no",
                "kyc_number",
                "first_name",
                "middle_name",
                "last_name",
                "primary_contact_number",
                "primary_email_address",
                "kyc_status",
                "kyc_level",
            ),
        )


class KycRoutingLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    tenant = models.CharField(max_length=50)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    version_no = models.IntegerField(blank=True, null=True)
    route_dump = models.TextField(blank=True, null=True)
    condition_dump = models.TextField(blank=True, null=True)
    performed_by = models.CharField(max_length=255, blank=True, null=True)
    performed_by_provider = models.CharField(max_length=255, blank=True, null=True)
    performed_by_uuid = models.CharField(max_length=255, blank=True, null=True)
    perform_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "kyc_routing_log"
