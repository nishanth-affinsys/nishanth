# import json
# from collections import OrderedDict
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from campaign_manager.views.campaign_views import CampaignViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebacampaign"
#
#
# path = f"{BASE_DIR}/campaign_manager/tests/responses/campaign_views_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestNotificationCampaigns(APITestCase):
#     databases = {"analytics"}
#     fixtures = [
#         "campaign_manager/tests/fixtures/campaignnotification.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2023-05-11T00:00:00Z", "2023-10-28T00:00:00Z"],
#             "campaign_variants": [85, 77, 86, 79, 94, 87],
#         }
#         self.campaign_notification = CampaignViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#
#     # @mock.patch(
#     #     "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#     #     side_effect=get_current_tenant_name,
#     # )
#     # def test_campaign_notification_details(self, mock_middleware):
#     #     result = self.campaign_notification.campaign_notification_details(self.request)
#     #     actual_output = self.parse_json["notification_details"]
#     #     self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_notification_details_export(self, mock_middleware):
#         result = self.campaign_notification.campaign_notification_details_export(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Campaign_details.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_notification_details_export_pdf(self, mock_middleware):
#         result = self.campaign_notification.campaign_notification_details_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=Campaign_details.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sent_messages_per_channel(self, mock_middleware):
#         result = self.campaign_notification.total_sent_messages_per_channel(
#             self.request
#         )
#         actual_output = self.parse_json["sent_notification"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_delivered_messages_per_channel(self, mock_middleware):
#         result = self.campaign_notification.total_delivered_messages_per_channel(
#             self.request
#         )
#         actual_output = self.parse_json["delivered_notification"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_read_messages_per_channel(self, mock_middleware):
#         result = self.campaign_notification.total_read_messages_per_channel(
#             self.request
#         )
#         actual_output = self.parse_json["read_notifications"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
