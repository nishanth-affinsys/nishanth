from rest_framework import serializers

from profile_data.models import (
    Profile,
    CategoryOptout,
    Interaction,
    BotInteraction,
    HandoffInteraction,
    ComplaintInteraction,
    CampaignData,
)
from main.utils.common_utils import custom_filters


class ProfileSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = Profile
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class CategoryOptoutSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CategoryOptout
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class InteractionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = Interaction
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class BotInteractionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = BotInteraction
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class HandoffInteractionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = HandoffInteraction
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class ComplaintInteractionSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = ComplaintInteraction
        fields = ["timestamp", "timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "timestamp__range", None, None)
        return data


class CampaignDataSerializers(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    campaign_id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignData
        fields = [
            "timestamp__range",
            "campaign_id__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "timestamp__range", None, "campaign_id__in"
        )
        return internal_data


class CampaignDynamicCtaSerializers(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    campaign_id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignData
        fields = [
            "timestamp__range",
            "campaign_id__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "timestamp__range", None, "campaign_id__in"
        )
        return internal_data
