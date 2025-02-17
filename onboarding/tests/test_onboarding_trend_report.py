# import json
#
# from django.db.models import QuerySet
# from rest_framework.test import APITestCase, APIRequestFactory
# from unittest import mock
# from onboarding.views.onboarding_trend_report_views import TrendReportViewSet
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "rw"
#
#
# path = f"{BASE_DIR}/tests/responses/onboarding_trend_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# def date_to_string(data):
#     for item in data:
#         item["Date"] = str(item["Date"])
#     return data
#
#
# class TestOnboardingTrend(APITestCase):
#     databases = {"onboarding"}
#     fixtures = [
#         "tests/fixtures/singlecifretaildata.json",
#         "tests/fixtures/singlecifspdata.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2022-07-14T00:00:00Z", "2023-08-30T00:00:00Z"]
#         }
#         self.onboard = TrendReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_channelwise_etb_onboarding_rt(self, mock_middleware):
#         result = self.onboard.channelwise_etb_onboarding_rt(self.request)
#         self.assertIsInstance(result.data, QuerySet)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_channelwise_ntb_onboarding_rt(self, mock_middleware):
#         result = self.onboard.channelwise_ntb_onboarding_rt(self.request)
#         formatted_result = date_to_string(list(result.data))
#         actual_output = self.parse_json["channel_ntb_rt"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_customer_onboarded_etb_rt(self, mock_middleware):
#         result = self.onboard.total_customer_onboarded_etb_rt(self.request)
#         actual_output = self.parse_json["cust_etb_rt"]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_customer_onboarded_ntb_rt(self, mock_middleware):
#         result = self.onboard.total_customer_onboarded_ntb_rt(self.request)
#         actual_output = [{"Month": "2023-Apr", "Count": 1}]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_productwise_account_opened_rt(self, mock_middleware):
#         result = self.onboard.productwise_account_opened_rt(self.request)
#         actual_output = self.parse_json["product_rt"]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_channelwise_etb_onboarding_sp(self, mock_middleware):
#         result = self.onboard.channelwise_etb_onboarding_sp(self.request)
#         formatted_result = date_to_string(list(result.data))
#         actual_output = self.parse_json["channel_etb_sp"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_channelwise_ntb_onboarding_sp(self, mock_middleware):
#         result = self.onboard.channelwise_ntb_onboarding_sp(self.request)
#         formatted_result = date_to_string(list(result.data))
#         actual_output = [{"Date": "2023-03-08", "Agent": 0, "Self": 0, "Staff": 0}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_customer_onboarded_etb_sp(self, mock_middleware):
#         result = self.onboard.total_customer_onboarded_etb_sp(self.request)
#         actual_output = self.parse_json["cust_etb_sp"]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_customer_onboarded_ntb_sp(self, mock_middleware):
#         result = self.onboard.total_customer_onboarded_ntb_sp(self.request)
#         self.assertIsInstance(result.data, QuerySet)
#
#     @mock.patch(
#         "onboarding.services.onboarding_trend_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_productwise_account_opened_sp(self, mock_middleware):
#         result = self.onboard.productwise_account_opened_sp(self.request)
#         actual_output = self.parse_json["product_sp"]
#         self.assertEqual(list(result.data), actual_output)
