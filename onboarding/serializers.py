from rest_framework import serializers
from onboarding.models import SingleCifRetailData
from main.utils.common_utils import custom_filters
from client_specific.models import KycApplicationsDetails, OnboardingAuditDetails


class OnboardingSerializer(serializers.ModelSerializer):
    last_modified_timestamp__range = serializers.ListField(
        max_length=20, required=False
    )

    class Meta:
        model = SingleCifRetailData
        fields = ["last_modified_timestamp", "last_modified_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "last_modified_timestamp__range", None, None)
        return data


class KycApplicationSerializer(serializers.ModelSerializer):
    last_modified_timestamp__range = serializers.ListField(
        max_length=20, required=False
    )

    class Meta:
        model = KycApplicationsDetails
        fields = ["last_modified_timestamp", "last_modified_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "last_modified_timestamp__range", None, None)
        return data


class OnboardingAuditSerializer(serializers.ModelSerializer):
    action_perform_timestamp__range = serializers.ListField(
        max_length=20, required=False
    )

    class Meta:
        model = OnboardingAuditDetails
        fields = ["action_perform_timestamp", "action_perform_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "action_perform_timestamp__range", None, None)
        return data
