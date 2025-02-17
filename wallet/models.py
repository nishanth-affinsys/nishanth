from django.db import models


# Wallet transaction schema models
class TransactionsAccountingentrydefinition(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.CharField(max_length=50)
    debit_credit_index = models.CharField(max_length=1)
    charge_code = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=10)
    netting_index = models.BooleanField()
    account = models.ForeignKey(
        "TransactionsTransactiongeneralledger", models.DO_NOTHING
    )
    transaction_template = models.ForeignKey(
        "TransactionsTransactiontemplate", models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "transactions_accountingentrydefinition"


class TransactionsTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=50)
    amount = models.CharField(max_length=255)
    charge = models.TextField(blank=True, null=True)
    currency = models.CharField(max_length=3)
    acquirer_details = models.TextField()
    transaction_method = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)
    status_description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField()
    attempt_no = models.IntegerField()
    transaction_definition = models.ForeignKey(
        "TransactionsTransactiondefinition", models.DO_NOTHING
    )
    transaction_template = models.ForeignKey(
        "TransactionsTransactiontemplate", models.DO_NOTHING, blank=True, null=True
    )
    node_id = models.CharField(max_length=40, blank=True, null=True)
    service_name = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    initiator = models.ForeignKey("TransactionsTransactionuser", models.DO_NOTHING)
    receiver = models.ForeignKey(
        "TransactionsTransactionuser",
        models.DO_NOTHING,
        related_name="transactionstransaction_receiver_set",
    )
    tenant = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "transactions_transaction"


class TransactionsTransactioncategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    tenant = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "transactions_transactioncategory"


class TransactionsTransactionchargelog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_subtype = models.CharField(max_length=50, blank=True, null=True)
    kyc = models.CharField(max_length=5, blank=True, null=True)
    charge_code = models.CharField(max_length=20)
    charge_amount = models.CharField(max_length=255)
    transaction_link = models.ForeignKey(TransactionsTransaction, models.DO_NOTHING)
    tenant = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "transactions_transactionchargelog"


class TransactionsTransactiondefinition(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    od_tracking = models.CharField(max_length=50)
    credit_tracking = models.CharField(max_length=50)
    consider_for_activity = models.BooleanField()
    is_active = models.BooleanField()
    external_transaction_code = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey(TransactionsTransactioncategory, models.DO_NOTHING)
    tenant = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "transactions_transactiondefinition"


class TransactionsTransactiongeneralledger(models.Model):
    id = models.BigAutoField(primary_key=True)
    gl_code = models.CharField(unique=True, max_length=30)
    type = models.CharField(max_length=100)
    is_leaf_node = models.BooleanField()
    is_blocked = models.BooleanField()
    is_open = models.BooleanField()

    class Meta:
        managed = False
        db_table = "transactions_transactiongeneralledger"


class TransactionsTransactionlimit(models.Model):
    id = models.BigAutoField(primary_key=True)
    detail = models.TextField()
    last_modified = models.DateTimeField()
    is_active = models.BooleanField()
    transaction_code = models.OneToOneField(
        "TransactionsTransactiontemplate", models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "transactions_transactionlimit"


class TransactionsTransactionlimitlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_subtype = models.CharField(max_length=50)
    kyc = models.CharField(max_length=5)
    account_type = models.CharField(max_length=30)
    limit = models.ForeignKey(TransactionsTransactionlimit, models.DO_NOTHING)
    transaction = models.ForeignKey(TransactionsTransaction, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "transactions_transactionlimitlog"


class TransactionsTransactiontemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    template_code = models.CharField(max_length=15)
    description = models.TextField()
    from_account_type = models.CharField(max_length=1)
    to_account_type = models.CharField(max_length=1)
    beneficiary = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField()
    customer_alert = models.BooleanField()
    transaction_definition = models.ForeignKey(
        TransactionsTransactiondefinition, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "transactions_transactiontemplate"
        unique_together = ("template_code", "transaction_definition")


# merchant accounting table from eventlogger
class AccountingMerchant(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    sender_name = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    node_id = models.CharField(max_length=100, blank=True, null=True)
    node_name = models.CharField(max_length=100, blank=True, null=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    qr_id = models.CharField(max_length=100, blank=True, null=True)
    qr_status = models.CharField(max_length=100, blank=True, null=True)
    qr_type = models.CharField(max_length=100, blank=True, null=True)
    receiver_acc_number = models.CharField(max_length=100, blank=True, null=True)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    sender_acc_number = models.CharField(max_length=100, blank=True, null=True)
    sender_acc_type = models.CharField(max_length=100, blank=True, null=True)
    sender_age = models.CharField(max_length=100, blank=True, null=True)
    sender_location = models.CharField(max_length=100, blank=True, null=True)
    transaction_amount = models.CharField(max_length=100, blank=True, null=True)
    transaction_remarks = models.CharField(max_length=100, blank=True, null=True)
    transaction_status = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=100, blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    sender_id = models.IntegerField(blank=True, null=True)
    transaction_type = models.CharField(max_length=100, blank=True, null=True)
    receiver_provider = models.CharField(max_length=100, blank=True, null=True)
    sender_phone_number = models.CharField(max_length=250, blank=True, null=True)
    receiver_phone_number = models.CharField(max_length=250, blank=True, null=True)
    qr_description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "accounting_merchant"


class MerchantHierarchy(models.Model):
    node_id = models.IntegerField(primary_key=True)
    node_name = models.CharField(max_length=100, blank=True, null=True)
    level_id = models.IntegerField(blank=True, null=True)
    node_id_of_children = models.TextField(
        blank=True, null=True
    )  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "merchant_hierarchy"


class QrWallet(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    qr_uuid = models.CharField(max_length=100, blank=True, null=True)
    qr_type = models.CharField(max_length=100, blank=True, null=True)
    node_id = models.CharField(max_length=100, blank=True, null=True)
    node_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    tenant = models.CharField(max_length=100, blank=True, null=True)
    receiver_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)
    behaviour = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "qr_wallet"


class TransactionsTransactionuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    provider = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    unique_identifier = models.CharField(max_length=255)
    payment_identifier = models.CharField(max_length=255, blank=True, null=True)
    payment_method_provider = models.CharField(max_length=255, blank=True, null=True)
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    tenant = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "transactions_transactionuser"
        unique_together = (
            (
                "unique_identifier",
                "payment_type",
                "payment_identifier",
                "payment_method_provider",
            ),
        )


class WalletAccountingentry(models.Model):
    id = models.BigAutoField(primary_key=True)
    transaction_category = models.CharField(max_length=100)
    transaction_code = models.CharField(max_length=100)
    transaction_template = models.CharField(max_length=100)
    transaction_uuid = models.CharField(max_length=100)
    event = models.CharField(max_length=100)
    accounting_entry_uuid = models.CharField(unique=True, max_length=50)
    account = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100)
    account_currency = models.CharField(max_length=100)
    debit_credit_index = models.CharField(max_length=1)
    amount_tag = models.CharField(max_length=100)
    transaction_currency = models.CharField(max_length=50)
    transaction_amount = models.CharField(max_length=50, blank=True, null=True)
    exchange_rate = models.CharField(max_length=50, blank=True, null=True)
    local_currency_amount = models.CharField(max_length=50, blank=True, null=True)
    offset_account = models.CharField(max_length=100)
    beneficiary = models.CharField(max_length=100, blank=True, null=True)
    transaction_timestamp = models.DateTimeField()
    value_timestamp = models.DateTimeField(blank=True, null=True)
    gl_category = models.CharField(max_length=100)
    customer_gl_index = models.CharField(max_length=1)
    is_gl_balance_updated = models.BooleanField()
    tenant = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "wallet_accountingentry"
