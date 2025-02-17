# import json
#
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from campaign_manager.views.campaign_active_inactive_views import (
#     CampaignActiveInActiveViewSet,
# )
# from unittest import mock
#
# from console.tests.test_report_at_glance import datetime_to_string
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebacampaign"
#
#
# path = f"{BASE_DIR}/campaign_manager/tests/responses/campaign_active_inactive_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestActiveInactiveCampaigns(APITestCase):
#     databases = {"campaign", "profile"}
#     fixtures = [
#         "campaign_manager/tests/fixtures/campaign.json",
#         "campaign_manager/tests/fixtures/campaignuserlog.json",
#         "campaign_manager/tests/fixtures/subcampaigndetail.json",
#         "campaign_manager/tests/fixtures/profiledataprofiledataslotuuid.json",
#         "campaign_manager/tests/fixtures/profiledataprofiledata.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2023-01-11T00:00:00Z", "2023-10-28T00:00:00Z"],
#             "campaign_variants": [85, 77, 86, 79, 94, 87],
#         }
#         self.campaign_status = CampaignActiveInActiveViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_created_campaigns_bigNum(self, mock_middleware):
#         result = self.campaign_status.created_campaigns_bigNum(self.request)
#         actual_output = self.parse_json["created_campaign"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_completed_campaigns_bigNum(self, mock_middleware):
#         result = self.campaign_status.completed_campaigns_bigNum(self.request)
#         actual_output = self.parse_json["completed_campaign"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_campaigns_bigNum(self, mock_middleware):
#         result = self.campaign_status.active_campaigns_bigNum(self.request)
#         actual_output = self.parse_json["active_campaign"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_inactive_campaigns_bigNum(self, mock_middleware):
#         result = self.campaign_status.inactive_campaigns_bigNum(self.request)
#         actual_output = self.parse_json["inactive_campaign"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_deleted_campaigns_bigNum(self, mock_middleware):
#         result = self.campaign_status.deleted_campaigns_bigNum(self.request)
#         actual_output = self.parse_json["deleted_campaign"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_inactive_linechart(self, mock_middleware):
#         result = self.campaign_status.active_inactive_linechart(self.request)
#         formatted_actual_data = datetime_to_string(result.data)
#         actual_output = self.parse_json["active_inactive_linechart"]
#         self.assertEqual(formatted_actual_data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_aggregate_details(self, mock_middleware):
#         result = self.campaign_status.campaign_aggregate_details(self.request)
#         actual_output = self.parse_json["aggregate_details"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_aggregate_details_export_csv(self, mock_middleware):
#         result = self.campaign_status.campaign_aggregate_details_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Campaigns_aggregate_details.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_aggregate_details_export_pdf(self, mock_middleware):
#         result = self.campaign_status.campaign_aggregate_details_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=Campaigns_aggregate_details.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_types_details(self, mock_middleware):
#         result = self.campaign_status.campaign_types_details(self.request)
#         actual_output = self.parse_json["campaign_type_details"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_types_details_export_csv(self, mock_middleware):
#         result = self.campaign_status.campaign_types_details_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=campaign_types_details.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_campaign_types_details_export_pdf(self, mock_middleware):
#         result = self.campaign_status.campaign_types_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=campaign_types_details.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sub_campaign_targeted_user(self, mock_middleware):
#         result = self.campaign_status.sub_campaign_targeted_user(self.request)
#         actual_output = self.parse_json["sub_targeted_users"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sub_campaign_targeted_user_export_csv(self, mock_middleware):
#         result = self.campaign_status.sub_campaign_targeted_user_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=subcampaign_targeted_users.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_active_inactive_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sub_campaign_targeted_user_export_pdf(self, mock_middleware):
#         result = self.campaign_status.sub_campaign_targeted_user_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=subcampaign_targeted_users.pdf",
#         )
