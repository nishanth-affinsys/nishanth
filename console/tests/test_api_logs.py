# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from console.views.api_logs_views import ApiLogsChartsViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebacpsix"
#
#
# path = f"{BASE_DIR}/tests/responses/api_reports_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestApiLogs(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["tests/fixtures/apilog.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.api = ApiLogsChartsViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_calls(self, mock_middleware):
#         result = self.api.api_calls(self.request)
#         actual_output = self.parse_json["api_calls"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_calls_export(self, mock_middleware):
#         result = self.api.api_calls_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_api_calls.csv",
#         )
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_calls_export_pdf(self, mock_middleware):
#         result = self.api.api_calls_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=total_api_calls.pdf"
#         )
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_details(self, mock_middleware):
#         result = self.api.api_details(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["api_details"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_details_export(self, mock_middleware):
#         result = self.api.api_details_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=api_details.csv",
#         )
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_details_export_pdf(self, mock_middleware):
#         result = self.api.api_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=api_details.pdf",
#         )
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_exceptions(self, mock_middleware):
#         result = self.api.api_exceptions(self.request)
#         actual_output = self.parse_json["api_exceptions"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_exceptions_export(self, mock_middleware):
#         result = self.api.api_exceptions_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=api_exceptions.csv",
#         )
#
#     @mock.patch(
#         "console.services.api_logs_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_api_exceptions_export_pdf(self, mock_middleware):
#         result = self.api.api_exceptions_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=api_exceptions.pdf",
#         )
