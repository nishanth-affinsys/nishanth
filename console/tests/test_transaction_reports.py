# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from console.views.transactions_reports_views import TransactionChartsViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebacpsix"
#
#
# path = f"{BASE_DIR}/tests/responses/transaction_reports_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# def datetime_to_string(data):
#     return [
#         {
#             "Date": item["Date"].strftime("%Y-%m-%d"),
#             "Successfull_transactions": item["Successfull_transactions"],
#             "Failed_transactions": item["Failed_transactions"],
#         }
#         for item in data
#     ]
#
#
# class TestTransactionReport(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["tests/fixtures/stagelog.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2021-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.trans = TransactionChartsViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction(self, mock_middleware):
#         result = self.trans.successful_transaction(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_goal_completed(self, mock_middleware):
#         result = self.trans.successful_transaction_goal_completed(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_goal_not_completed(self, mock_middleware):
#         result = self.trans.successful_transaction_goal_not_completed(self.request)
#         self.assertEqual(result.data, {"count": 0})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Failed_transaction(self, mock_middleware):
#         result = self.trans.failed_transaction(self.request)
#         self.assertEqual(result.data, {"count": 2})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_System_aborted(self, mock_middleware):
#         result = self.trans.system_aborted(self.request)
#         self.assertEqual(result.data, {"count": 0})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_User_aborted(self, mock_middleware):
#         result = self.trans.user_aborted(self.request)
#         self.assertEqual(result.data, {"count": 2})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_rpt(self, mock_middleware):
#         result = self.trans.successful_transaction_rpt(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["successful_transaction"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_export(self, mock_middleware):
#         result = self.trans.successful_transaction_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=successful_transactions.csv",
#         )
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_export_pdf(self, mock_middleware):
#         result = self.trans.successful_transaction_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=successful_transactions.pdf",
#         )
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Failed_transaction_rpt(self, mock_middleware):
#         result = self.trans.failed_transaction_rpt(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["failed_transaction"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Failed_transaction_export(self, mock_middleware):
#         result = self.trans.failed_transaction_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=failed_transactions.csv",
#         )
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Failed_transaction_export_pdf(self, mock_middleware):
#         result = self.trans.failed_transaction_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=failed_transactions.pdf",
#         )
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transactions_linechart(self, mock_middleware):
#         result = self.trans.transactions_linechart(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = self.parse_json["multiline_chart"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Successful_transaction_partition(self, mock_middleware):
#         result = self.trans.successful_transaction_partition(self.request)
#         actual_output = self.parse_json["success_partition"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_failed_transaction_partition(self, mock_middleware):
#         result = self.trans.failed_transaction_partition(self.request)
#         actual_output = self.parse_json["failed_partition"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_API_calls_FAQ(self, mock_middleware):
#         result = self.trans.total_api_calls_faq(self.request)
#         self.assertEqual(result.data, {"count": 7})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_API_calls_Trans(self, mock_middleware):
#         result = self.trans.total_api_calls_trans(self.request)
#         self.assertEqual(result.data, {"count": 7})
#
#     @mock.patch(
#         "console.services.transaction_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_all_transaction_breakdown_sunburst(self, mock_middleware):
#         result = self.trans.all_transaction_breakdown_sunburst(self.request)
#         actual_output = self.parse_json["all_transactions_partition"]
#         self.assertEqual(result.data, actual_output)
