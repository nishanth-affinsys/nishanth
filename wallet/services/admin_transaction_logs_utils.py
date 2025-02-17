from wallet.models import WalletAccountingentry, TransactionsTransaction
from wallet.serializers import WalletAccountingentrySerializer, TransactionSerializer
import json
from main.utils.boiler_plate import query
from main.tenant_middleware import get_current_tenant_name, get_timezone
from django.db.models import F, JSONField
from django.db.models.functions import Cast, Trunc
from django.db.models.fields.json import KT


def wallet_admin_transaction_logs_generic(request):
    qs = query(request, TransactionsTransaction, TransactionSerializer, "transaction")
    qs = (
        qs.
        filter(
            tenant=get_current_tenant_name(),
        )
        .annotate(
            charges_data=Cast("charge", JSONField()),
            acquirer_details_data=Cast("acquirer_details", JSONField()),
            transaction_method_data=Cast("transaction_method", JSONField()),
        )
        .values(
            Transaction_ID=F("uuid"),
            Amount=F("amount"),
            Currency=F("currency"),
            Status=F("status"),
            Total_Charge=KT("charges_data__total_charge"),
            Total_discount=KT("charges_data__total_discount"),
            Final_amount=KT("charges_data__final_amount"),
            Receiver_type=KT("acquirer_details_data__receiver_provider"),
            Source_account_type=KT("transaction_method_data__source_type"),
            Account_number=KT("transaction_method_data__account_number"),
            Wallet_id=KT("transaction_method_data__wallet_id"),
            Status_description=F("status_description"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            Attempt_no=F("attempt_no"),
            Transaction_type=F("transaction_definition_id__name"),
            Template_code=F("transaction_template_id__template_code"),
            Node_id=F("node_id"),
            Additional_info=F("additional_info"),
            Initiator_username=F("initiator_id__username"),
            Receiver_username=F("receiver_id__username"),
        )
    )

    return (
        qs,
        [
        "Transaction_ID",
        "Amount",
        "Currency",
        "Status",
        "Total_Charge",
        "Total_discount",
        "Final_amount",
        "Receiver_type",
        "Source_account_type",
        "Account_number",
        "Wallet_id",
        "Status_description",
        "Timestamp",
        "Attempt_no",
        "Transaction_type",
        "Template_code",
        "Node_id",
        "Additional_info",
        "Initiator_username",
        "Receiver_username",
        ],
        "Transaction_Logs_Report",
    )


def wallet_admin_reconciliation_report(request):
    qs = query(
        request, WalletAccountingentry, WalletAccountingentrySerializer, "accounting"
    )
    qs = (
        qs
        .filter(tenant=get_current_tenant_name())
        .values(
            Transaction_Category=F("transaction_category"),
            Transaction_Code=F("transaction_code"),
            Transaction_UUID=F("transaction_uuid"),
            Event=F("event"),
            Accounting_Entry_UUID=F("accounting_entry_uuid"),
            Account=F("account"),
            Account_Type=F("account_type"),
            Account_Currency=F("account_currency"),
            Debit_Credit_Index=F("debit_credit_index"),
            Transaction_Currency=F("transaction_currency"),
            Transaction_Amount=F("transaction_amount"),
            Local_Currency_Amount=F("local_currency_amount"),
            Beneficiary=F("beneficiary"),
            Transaction_Timestamp=Trunc(F("transaction_timestamp"), "second", tzinfo=get_timezone()),
            GL_Category=F("gl_category"),
        )
    )

    return (
        qs,
        [
            "Transaction_Category",
            "Transaction_Code",
            "Transaction_UUID",
            "Accounting_Entry_UUID",
            "Event",
            "Account",
            "Account_Type",
            "Account_Currency",
            "Debit_Credit_Index",
            "Transaction_Amount",
            "Local_Currency_Amount",
            "Transaction_Currency",
            "Beneficiary",
            "Transaction_Timestamp",
            "GL_Category",
        ],
        "Reconciliation_Report",
    )
