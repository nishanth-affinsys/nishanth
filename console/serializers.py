from attr.validators import max_len
from rest_framework import serializers

from console.models import (
    MessageLog,
    ApiLog,
    StageLog,
    Activity,
    MessageStatus,
    LlmUpload,
    ServiceStatus,
    StageLogAuth,
    ChannelsReactions,
    MessageLogDetails,
    StageLogDetails, ApiLogDetails
)
from main.utils.common_utils import custom_filters


class BotReportSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = MessageLog
        fields = ["channel", "channel__in", "timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", "channel__in", None)
        return internal_data


class DailyTrafficSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = MessageLog
        fields = ["channel", "channel__in", "timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", "channel__in", None)
        return internal_data


class ApiLogsSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = ApiLog
        fields = ["channel", "channel__in", "timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", "channel__in", None)
        return internal_data


class TransactionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = StageLog
        fields = ["channel", "channel__in", "timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", "channel__in", None)
        return internal_data


class ActivitySerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = Activity
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class AuditLogSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = StageLogAuth
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class MessageStatusSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = MessageStatus
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class LlmUploadSerializer(serializers.ModelSerializer):
    last_updated_at__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = LlmUpload
        fields = ["last_updated_at", "last_updated_at__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "last_updated_at__range", None, None)
        return data


class LlmMessagelogSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = MessageLog
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class ServiceStatusSerializer(serializers.ModelSerializer):
    last_modified_timestamp__range = serializers.ListField(
        max_length=20, required=False
    )

    class Meta:
        model = ServiceStatus
        fields = ["last_modified_timestamp", "last_modified_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "last_modified_timestamp__range", None, None)
        return data


class ChannelReactionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ChannelsReactions
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class CommitSerializer(serializers.Serializer):
    added = serializers.ListField(child=serializers.CharField())
    modified = serializers.ListField(child=serializers.CharField())


# Serializer for the main request data
class RequestDataSerializer(serializers.Serializer):
    commits = CommitSerializer(many=True, required=True)


class MessageLogSessionsSerializer(serializers.Serializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)
    customer_type__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = MessageLogDetails
        fields = ["channel", "channel__in", "timestamp", "timestamp__range", "customer_type", "customer_type__in"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", "channel__in", None, "customer_type__in")
        return data


class StageLogDetailsSerializer(serializers.Serializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)
    customer_type__in = serializers.ListField(max_length=150, required=False)
    transaction_intent__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = StageLogDetails
        fields = ["channel", "channel__in", "timestamp", "timestamp__range", "customer_type", "customer_type__in",
                  "transaction_intent__in", "transaction_intent"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", "channel__in", None, "customer_type__in",
                              "transaction_intent__in")
        return data


class ApiLogDetailSerializer(serializers.Serializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)
    customer_type__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = ApiLogDetails
        fields = ["channel", "channel__in", "timestamp", "timestamp__range", "customer_type", "customer_type__in"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", "channel__in", None, "customer_type__in")
        return data
