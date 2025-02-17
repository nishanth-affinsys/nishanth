from rest_framework import serializers
from vision.models import StageLogOcr, StageLogFace, StageLogForgery
from main.utils.common_utils import custom_filters

class VisionOCRSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = StageLogOcr
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


class VisionFaceSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = StageLogFace
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


class VisionForgerySerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = StageLogForgery
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data
