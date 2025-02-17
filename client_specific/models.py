from django.db import models
import os

# class Apilogig9Ccrl3A0Djayyw4Muydq(models.Model):
#     api = models.CharField(max_length=500, blank=True, null=True)
#     stage = models.CharField(max_length=500, blank=True, null=True)
#     status = models.CharField(max_length=500, blank=True, null=True)
#     channel = models.CharField(max_length=20, blank=True, null=True)
#     bb_txn_reference = models.CharField(max_length=500, blank=True, null=True)
#     data = models.TextField(blank=True, null=True)
#     exception = models.CharField(max_length=500, blank=True, null=True)
#     timestamp = models.DateTimeField(blank=True, null=True)
#     customer = models.CharField(max_length=150, blank=True, null=True)
#     request_id = models.CharField(max_length=500, blank=True, null=True)
#     endpoint = models.CharField(max_length=100, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'apilogig9ccrl3a0djayyw4muydq'
#
#
# class Customerprofileig9Ccrl3A0Djayyw4Muydq(models.Model):
#     customer = models.CharField(primary_key=True, max_length=150)
#     fname = models.CharField(max_length=20, blank=True, null=True)
#     lname = models.CharField(max_length=20, blank=True, null=True)
#     age = models.IntegerField(blank=True, null=True)
#     email = models.CharField(max_length=50, blank=True, null=True)
#     gender = models.CharField(max_length=1, blank=True, null=True)
#     married = models.CharField(max_length=1, blank=True, null=True)
#     metro = models.CharField(max_length=1, blank=True, null=True)
#     employed = models.CharField(max_length=1, blank=True, null=True)
#     income = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
#     hometown = models.CharField(max_length=50, blank=True, null=True)
#     zipcode = models.CharField(max_length=6, blank=True, null=True)
#     city = models.CharField(max_length=50, blank=True, null=True)
#     state = models.CharField(max_length=50, blank=True, null=True)
#     locale = models.CharField(max_length=20, blank=True, null=True)
#     timezone = models.CharField(max_length=60, blank=True, null=True)
#     last_interacted_time = models.DateTimeField(blank=True, null=True)
#     needhelp = models.IntegerField(blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'customerprofileig9ccrl3a0djayyw4muydq'
#
#
# class Userqueriesig9Ccrl3A0Djayyw4Muydq(models.Model):
#     message = models.TextField(blank=True, null=True)
#     channel = models.CharField(max_length=20, blank=True, null=True)
#     context = models.CharField(max_length=50, blank=True, null=True)
#     handled = models.CharField(max_length=1, blank=True, null=True)
#     timestamp = models.DateTimeField(blank=True, null=True)
#     intent1 = models.CharField(max_length=50, blank=True, null=True)
#     score1 = models.DecimalField(max_digits=30, decimal_places=30, blank=True, null=True)
#     intent2 = models.CharField(max_length=50, blank=True, null=True)
#     score2 = models.DecimalField(max_digits=30, decimal_places=30, blank=True, null=True)
#     intent3 = models.CharField(max_length=50, blank=True, null=True)
#     score3 = models.DecimalField(max_digits=30, decimal_places=30, blank=True, null=True)
#     derived_intent = models.CharField(max_length=150, blank=True, null=True)
#     category_name = models.CharField(max_length=50, blank=True, null=True)
#     product_name = models.CharField(max_length=50, blank=True, null=True)
#     attribute_name = models.CharField(max_length=50, blank=True, null=True)
#     customer = models.ForeignKey(Customerprofileig9Ccrl3A0Djayyw4Muydq, models.DO_NOTHING, db_column='customer', blank=True, null=True)
#     user_session = models.ForeignKey('Usersessionsig9Ccrl3A0Djayyw4Muydq', models.DO_NOTHING, blank=True, null=True)
#     message_id = models.CharField(max_length=500, blank=True, null=True)
#     source = models.CharField(max_length=10, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'userqueriesig9ccrl3a0djayyw4muydq'
#
#
# class Usersessionsig9Ccrl3A0Djayyw4Muydq(models.Model):
#     user_session_id = models.CharField(primary_key=True, max_length=100)
#     timestamp = models.DateTimeField(blank=True, null=True)
#     channel = models.CharField(max_length=100, blank=True, null=True)
#     customer = models.ForeignKey(Customerprofileig9Ccrl3A0Djayyw4Muydq, models.DO_NOTHING, db_column='customer', blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'usersessionsig9ccrl3a0djayyw4muydq'
#
#
# class Userstageig9Ccrl3A0Djayyw4Muydq(models.Model):
#     channel = models.CharField(max_length=100, blank=True, null=True)
#     transaction_intent = models.CharField(max_length=200, blank=True, null=True)
#     transaction_id = models.CharField(max_length=150, blank=True, null=True)
#     stage = models.CharField(max_length=100, blank=True, null=True)
#     stage_result = models.CharField(max_length=100, blank=True, null=True)
#     stage_response = models.CharField(max_length=200, blank=True, null=True)
#     timestamp = models.DateTimeField(blank=True, null=True)
#     rmn = models.CharField(max_length=20, blank=True, null=True)
#     transaction_code = models.CharField(max_length=10, blank=True, null=True)
#     customer = models.ForeignKey(Customerprofileig9Ccrl3A0Djayyw4Muydq, models.DO_NOTHING, db_column='customer', blank=True, null=True)
#     user_session = models.ForeignKey(Usersessionsig9Ccrl3A0Djayyw4Muydq, models.DO_NOTHING, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'userstageig9ccrl3a0djayyw4muydq'
#
# class LiteGenericuserdata(models.Model):
#     """Generic User Data table from auth"""
#     channel_id = models.TextField(blank=True, null=True)
#     client = models.TextField(blank=True, null=True)
#     data = models.TextField(blank=True, null=True)
#     timestamp = models.DateTimeField()
#
#     class Meta:
#         "Only read access"
#         managed = False
#         db_table = "lite_genericuserdata"


from django.db import models


class AccessoryMaster(models.Model):
    tenant = models.CharField(max_length=255, null=False)
    accessory_ref_number = models.CharField(max_length=50, null=False)
    branch_code = models.CharField(max_length=25, null=True)  # LOCATION
    cif = models.CharField(max_length=50, null=True)
    account_number = models.CharField(max_length=50, null=True)
    customer_name = models.CharField(max_length=255, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    accessory = models.CharField(max_length=255, null=True)  #
    accessory_input_value = models.CharField(
        max_length=255, null=True
    )  # CARD REFERENCE NUMBER
    current_event = models.CharField(max_length=75, null=False)
    issued_token = models.CharField(max_length=255, null=True)  #
    token_status = models.CharField(max_length=25, null=True)  #
    created_by_uuid = models.CharField(max_length=255, null=True)
    created_by = models.CharField(max_length=255, null=False)
    created_by_provider = models.CharField(max_length=255, null=False)
    create_timestamp = models.DateTimeField(null=False)
    is_active = models.CharField(max_length=1, default="Y", null=False)  #

    class Meta:
        db_table = "accessory_master"


class InventoryManagement(models.Model):
    tenant = models.CharField(max_length=255, null=False)
    inventory_reference_number = models.CharField(
        max_length=50, null=False, unique=True
    )
    active = models.CharField(
        max_length=1, null=False, default="Y"
    )  # CHECK FOR Y FILTER
    uploaded_by = models.CharField(max_length=255, null=True)
    uploaded_by_provider = models.CharField(max_length=255, null=True)
    uploaded_by_uuid = models.CharField(max_length=255, null=True)
    uploaded_timestamp = models.DateTimeField(null=True)

    class Meta:
        db_table = "inventory_master"


class InventoryAuditLog(models.Model):
    tenant = models.CharField(max_length=255, null=False)
    file_path = models.CharField(max_length=255, null=False)
    file_name = models.CharField(max_length=255, null=False)
    event_name = models.CharField(max_length=255, null=False)
    action_performed_by = models.CharField(max_length=255, null=True)
    action_perform_provider = models.CharField(max_length=255, null=True)
    action_performed_by_uuid = models.CharField(max_length=255, null=True)
    action_perform_timestamp = models.DateTimeField(null=True)
    data = models.TextField(null=True)
    count = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = "inventory_audit_log"


class KycAccountOpeningDetails(models.Model):
    id = models.BigIntegerField(primary_key=True)
    kyc_reference = models.CharField(max_length=255, blank=True, null=True)
    application_reference_number = models.CharField(max_length=50, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=20, blank=True, null=True)
    primary_email_address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    kyc_state = models.CharField(max_length=100, blank=True, null=True)
    account_opening_status = models.CharField(blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'kyc_account_opening_details'


class OnboardingRetailComments(models.Model):
    id = models.BigIntegerField(primary_key=True)
    internal_reference = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    last_action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    last_action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    account_num1 = models.CharField(max_length=100, blank=True, null=True)
    account_num2 = models.CharField(max_length=100, blank=True, null=True)
    created_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    present_at_branch_code = models.CharField(max_length=25, blank=True, null=True)
    application_status = models.CharField(max_length=75, blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    queue_name = models.CharField(max_length=100, blank=True, null=True)
    action_code = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'onboarding_retail_comments'


class KycApplicationsDetails(models.Model):
    id = models.BigIntegerField(primary_key=True)
    internal_reference = models.CharField(max_length=255, blank=True, null=True)
    kyc_number = models.CharField(max_length=255, blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=255, blank=True, null=True)
    created_by= models.CharField(max_length=255,blank=True,null=True)
    create_timestamp = models.DateTimeField(blank=True, null=True)
    last_action_performed_by = models.CharField(max_length=255, blank=True, null=True)
    last_action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    customer_type = models.CharField(max_length=10, blank=True, null=True)
    channel = models.CharField(max_length=100, blank=True, null=True)
    queue_code = models.CharField(max_length=25, blank=True, null=True)
    queue_name = models.CharField(max_length=25, blank=True, null=True)
    submit_by = models.CharField(max_length=255, blank=True, null=True)
    submit_timestamp = models.DateTimeField(blank=True, null=True)
    rejected_by = models.CharField(max_length=255, blank=True, null=True)
    rejected_timestamp = models.DateTimeField(blank=True, null=True)
    last_modified_by = models.CharField(max_length=255, blank=True, null=True)
    last_modified_timestamp = models.DateTimeField(blank=True, null=True)
    action_code = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'kyc_applications_details'


class OnboardingAuditDetails(models.Model):
    id = models.BigIntegerField(primary_key=True)
    single_cifrt_internal_reference = models.CharField(max_length=50, blank=True, null=True)
    event = models.CharField(max_length=255, blank=True, null=True)
    action_by = models.CharField(max_length=255, blank=True, null=True)
    action_perform_timestamp = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(max_length=250, blank=True, null=True)
    kyc_reference = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'onboarding_audit_details'
