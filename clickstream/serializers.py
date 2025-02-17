from psycopg2 import Timestamp
from rest_framework import serializers

from clickstream.models import (
    ClickstreamIpinformation,
    ClickstreamRecord,
    ClickstreamDevice,
    ClickstreamBrowser,
    ClickstreamAction,
)


class ClickStreamIpInformationSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ClickstreamIpinformation
        fields = ["timestamp__range"]


class ClickStreamRecordSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ClickstreamRecord
        fields = ["timestamp__range"]


class ClickStreamDeviceSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ClickstreamDevice
        fields = ["timestamp__range"]


class ClickStreamBrowserSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ClickstreamBrowser
        fields = ["timestamp__range"]


class ClickStreamActionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ClickstreamAction
        fields = ["timestamp__range"]
