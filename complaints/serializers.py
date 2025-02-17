from rest_framework import serializers
from console.models import ComplaintTicketLogs, ComplaintEmailAudit
from main.utils.common_utils import custom_filters


class ComplaintTicketSerializer(serializers.ModelSerializer):
    created_timestamp__range = serializers.ListField(max_length=20, required=True)
    source__in = serializers.ListField(max_length=150, required=True)

    class Meta:
        model = ComplaintTicketLogs
        fields = [
            "source",
            "source__in",
            "created_timestamp__range",
            "created_timestamp",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "created_timestamp__range", "source__in", None
        )
        return internal_data


class ComplaintEmailSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=True)

    class Meta:
        model = ComplaintEmailAudit
        fields = [
            "timestamp__range",
            "timestamp",
        ]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data
