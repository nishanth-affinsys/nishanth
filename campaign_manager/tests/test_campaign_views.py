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
# class TestCampaignViews(APITestCase):
#     databases = {"profile", "campaign"}
#     fixtures = [
#         "campaign_manager/tests/fixtures/profiledataprofiledataslotuuid.json",
#         "campaign_manager/tests/fixtures/subcampaignuser.json",
#         "campaign_manager/tests/fixtures/subcampaignrun.json",
#         "campaign_manager/tests/fixtures/subcampaigntargetsegment.json",
#         "campaign_manager/tests/fixtures/campaign.json",
#         "campaign_manager/tests/fixtures/subcampaigndetail.json",
#         "campaign_manager/tests/fixtures/profiledataprofiledata.json",
#         "campaign_manager/tests/fixtures/profiledataprofiledataoptedoutmarketing.json",
#         "campaign_manager/tests/fixtures/profiledatachanneldata.json",
#         "campaign_manager/tests/fixtures/profiledataprofiledataoptedoututility.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2023-02-01T00:00:00Z", "2023-11-18T00:00:00Z"],
#             "campaign_variants": [85, 77, 86, 79, 94, 87, 91, 90, 94],
#         }
#         self.campaign_users = CampaignViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_target_users_by_run_id(self, mock_middleware):
#         result = self.campaign_users.target_users_by_run_id(self.request)
#         actual_output = self.parse_json["targeted_by_run"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_target_users_by_run_id_export_csv(self, mock_middleware):
#         result = self.campaign_users.target_users_by_run_id_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=targeted_users_by_run.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_target_users_by_run_id_export_pdf(self, mock_middleware):
#         result = self.campaign_users.target_users_by_run_id_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=targeted_users_by_run.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_marketing_users_by_channel(self, mock_middleware):
#         result = self.campaign_users.total_marketing_users_by_channel(self.request)
#         actual_output = self.parse_json["marketing_users"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_marketing_users_by_channel_export_csv(self, mock_middleware):
#         result = self.campaign_users.total_marketing_users_by_channel_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=aggregate_users.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_marketing_users_by_channel_export_pdf(self, mock_middleware):
#         result = self.campaign_users.total_marketing_users_by_channel_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=aggregate_users.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_utility_users_by_channel(self, mock_middleware):
#         result = self.campaign_users.total_utility_users_by_channel(self.request)
#         actual_output = self.parse_json["marketing_users"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_utility_users_by_channel_export_csv(self, mock_middleware):
#         result = self.campaign_users.total_utility_users_by_channel_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=aggregate_users.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_utility_users_by_channel_export_pdf(self, mock_middleware):
#         result = self.campaign_users.total_utility_users_by_channel_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=aggregate_users.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_marketing(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_marketing(self.request)
#         actual_output = self.parse_json["marketing_users"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_marketing_export_csv(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_marketing_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=user_status.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_marketing_export_pdf(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_marketing_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=user_status.pdf",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_utility(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_utility(self.request)
#         actual_output = self.parse_json["marketing_users"]
#         self.assertEqual(result.data, OrderedDict(actual_output))
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_utility_export_csv(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_utility_export_csv(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=user_status.csv",
#         )
#
#     @mock.patch(
#         "campaign_manager.services.campaign_views_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_opted_in_out_details_utility_export_pdf(self, mock_middleware):
#         result = self.campaign_users.opted_in_out_details_utility_export_pdf(
#             self.request
#         )
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=user_status.pdf",
#         )
