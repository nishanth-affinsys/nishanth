from rest_framework import serializers
from main.utils.common_utils import custom_filters
from client_specific.models import AccessoryMaster, InventoryManagement


class AccessoryMasterSerializer(serializers.ModelSerializer):
    create_timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = AccessoryMaster
        fields = ["create_timestamp", "create_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "create_timestamp__range", None, None)
        return data


class InventoryManagementSerializer(serializers.ModelSerializer):
    uploaded_timestamp__range = serializers.ListField(max_length=20, required=False)

    class Meta:
        model = InventoryManagement
        fields = ["uploaded_timestamp", "uploaded_timestamp__range"]

    def to_internal_value(self, data):
        data = custom_filters(data, "uploaded_timestamp__range", None, None)
        return data


# class ProfileDataSerializer(serializers.ModelSerializer):
#     created_timestamp__range = serializers.ListField(max_length=20, required=False)
#     profiledataprofilechannel__channel_identifier__channel_name__in = (
#         serializers.ListField(max_length=150, required=False)
#     )
#
#     class Meta:
#         model = ProfileDataProfiledata
#         fields = [
#             "created_timestamp",
#             "created_timestamp__range",
#             "profiledataprofilechannel__channel_identifier__channel_name__in",
#         ]
#
#
#     def to_internal_value(self, data):
#         data = {
#             "created_timestamp__range": data.get("timestamp__range"),
#             "profiledataprofilechannel__channel_identifier__channel_name__in": data.get(
#                 "channel"
#             ),
#         }
#         return data
#

# from psycopg2 import Timestamp
from rest_framework import serializers

#
#
# from client_specific.models import (
#   Userstageig9Ccrl3A0Djayyw4Muydq,
#   LiteGenericuserdata
# )

# class UserStageSerializer(serializers.ModelSerializer):
#     timestamp__range = serializers.ListField(max_length=20, required=False)
#
#     class Meta:
#         model = Userstageig9Ccrl3A0Djayyw4Muydq
#         fields = ["timestamp", "timestamp__range"]

# class LiteGenericSerializer(serializers.ModelSerializer):
#     timestamp__range = serializers.ListField(max_length=20, required=False)
#     timestamp = serializers.DateTimeField(required=False)
#
#     class Meta:
#         model = LiteGenericuserdata
#         fields = ["timestamp", "timestamp__range"]
