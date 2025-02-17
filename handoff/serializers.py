from psycopg2 import Timestamp
from rest_framework import serializers

from handoff.models import AnalyticsSocialevent
from main.utils.common_utils import custom_filters


class AgentReportSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    channel__in = serializers.ListField(max_length=150, required=False)

    class Meta:
        model = AnalyticsSocialevent
        fields = ["channel", "channel__in", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", "channel__in", None)
        return internal_data
