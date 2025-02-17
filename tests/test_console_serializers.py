# from django.test import TestCase
#
# from console.serializers import (
#     BotReportSerializer,
#     DailyTrafficSerializer,
#     ApiLogsSerializer,
#     TransactionSerializer,
#     ActivitySerializer,
#     MessageStatusSerializer,
# )
#
#
# class BotReportSerializerTestCase(TestCase):
#     def test_bot_report_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#             "channel": ["webchat"],
#         }
#         serializer = BotReportSerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(serializer.validated_data["channel__in"], ["webchat"])
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
#
#     def test_daily_traffic_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#             "channel": ["webchat"],
#         }
#         serializer = DailyTrafficSerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(serializer.validated_data["channel__in"], ["webchat"])
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
#
#     def test_api_logs_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#             "channel": ["webchat"],
#         }
#         serializer = ApiLogsSerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(serializer.validated_data["channel__in"], ["webchat"])
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
#
#     def test_transactions_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#             "channel": ["webchat"],
#         }
#         serializer = TransactionSerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(serializer.validated_data["channel__in"], ["webchat"])
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
#
#     def test_activity_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"]
#         }
#         serializer = ActivitySerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
#
#     def test_message_status_serializer(self):
#         serializer_data = {
#             "timestamp__range": ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#             "channel": ["webchat"],
#         }
#         serializer = MessageStatusSerializer(data=serializer_data)
#         result = serializer.is_valid()
#         self.assertTrue(result)
#         serialized_data = serializer.data
#         self.assertEqual(
#             serialized_data["timestamp__range"],
#             ["2023-01-01T00:00:00", "2023-06-01T00:00:00"],
#         )
