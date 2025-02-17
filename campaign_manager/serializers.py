from rest_framework import serializers

# new models import
from campaign_manager.models import Campaign, SubCampaignDetail
from campaign_manager.models import (
    CampaignsPushbroadcastreport,
    CampaignsCampaignvariant,
    CampaignsPushbroadcasttimeline,
    CampaignsCampaignvariantdetail,
)

from console.models import CampaignNotification, CtaReport
from main.utils.common_utils import custom_filters


class CampaignsPushbroadcastSerializer(serializers.ModelSerializer):
    initialized = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignsPushbroadcastreport
        fields = ["initialized"]

    def to_internal_value(self, data):
        data = custom_filters(data, "initialized__range", None, None)
        return data


class CampaignVariantIdSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignsCampaignvariant
        fields = ["timestamp__range", "id__in", "id"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, "id__in")
        return internal_data


class CampaignsPushtimeSerializer(serializers.ModelSerializer):
    start_date__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignsPushbroadcasttimeline
        fields = ["start_date", "start_date__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "start_date__range", None, None)
        return data


class CampaignVariantDetailSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)
    campaign_variant_id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignsCampaignvariantdetail
        fields = ["timestamp__range", "campaign_variant_id__in", "campaign_variant_id"]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "timestamp__range", None, "campaign_variant_id__in"
        )
        return internal_data


# serialzer with only time range filter
class CampaignVariantSerializer(serializers.ModelSerializer):
    timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignsCampaignvariant
        fields = ["timestamp__range"]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "timestamp__range", None, None)
        return internal_data


# new serializers according to new tables
class SubCampaignSerializer(serializers.ModelSerializer):
    last_modified__range = serializers.ListField(max_length=20, required=False)
    campaign__id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = SubCampaignDetail
        fields = [
            "last_modified__range",
            "campaign__id__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "last_modified__range", None, "campaign__id__in"
        )
        return internal_data


class CampaignSerializer(serializers.ModelSerializer):
    last_modified__range = serializers.ListField(max_length=20, required=False)
    id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = Campaign
        fields = [
            "last_modified__range",
            "id__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, "last_modified__range", None, "id__in")
        return internal_data


class CampaignNotificationSerializer(serializers.ModelSerializer):
    last_modified__range = serializers.ListField(max_length=20, required=False)
    campaign_filter_id__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CampaignNotification
        fields = [
            "last_modified__range",
            "campaign_filter_id__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(
            data, "last_modified__range", None, "campaign_filter_id__in"
        )
        return internal_data


class CTAReportSerializer(serializers.ModelSerializer):
    campaign_variants__in = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = CtaReport
        fields = [
            "campaign_variants__in",
        ]

    def to_internal_value(self, data):
        internal_data = custom_filters(data, None, None, "campaign_variants__in")
        return internal_data
