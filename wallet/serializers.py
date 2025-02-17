from sys import intern

from rest_framework import serializers

from wallet.models import (
    TransactionsTransaction,
    AccountingMerchant,
    QrWallet,
    WalletAccountingentry,
)

from main.utils.common_utils import custom_filters


# Wallet serializer for demo
class TransactionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = TransactionsTransaction
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


class AccMerchantSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = AccountingMerchant
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


class QrWalletSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = QrWallet
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


class WalletAccountingentrySerializer(serializers.ModelSerializer):
    transaction_timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = WalletAccountingentry
        fields = ["transaction_timestamp", "transaction_timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "transaction_timestamp__range", None, None)
        return internal_data
