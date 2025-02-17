# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from unittest import mock
# from onboarding.views.onboarding_transaction_report_views import (
#     TransactionReportViewSet,
# )
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "rw"
#
#
# path = f"{BASE_DIR}/tests/responses/onboarding_transaction_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# def date_to_string(data, key):
#     for item in data["results"]:
#         item[key] = str(item[key])
#     return data
#
#
# class TestOnboardingTransaction(APITestCase):
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
#             "timestamp__range": ["2022-08-11T00:00:00Z", "2023-08-30T00:00:00Z"]
#         }
#         self.onboard = TransactionReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_rt(self, mock_middleware):
#         result = self.onboard.successful_transaction_rt(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_sp(self, mock_middleware):
#         result = self.onboard.successful_transaction_sp(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_failed_transaction_sp(self, mock_middleware):
#         result = self.onboard.failed_transaction_sp(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_failed_transaction_rt(self, mock_middleware):
#         result = self.onboard.failed_transaction_rt(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_exception_transaction_rt(self, mock_middleware):
#         result = self.onboard.exception_transaction_rt(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_rt(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_rt(self.request)
#         formatted_output = date_to_string(result.data, "Approved_timestamp")
#         actual_output = self.parse_json["success_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_rt_export_csv(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=successful_transaction_report_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=successful_transaction_report_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_sp(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_sp(self.request)
#         formatted_output = date_to_string(result.data, "Approved_timestamp")
#         actual_output = self.parse_json["success_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_sp_export_csv(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_sp_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=successful_transaction_report_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_successful_transaction_report_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.successful_transaction_report_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=successful_transaction_report_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_rt(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_rt(self.request)
#         formatted_output = date_to_string(result.data, "Rejected_timestamp")
#         actual_output = self.parse_json["rejected_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_rt_export(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=rejected_transaction_report_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=rejected_transaction_report_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_sp(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_sp(self.request)
#         formatted_output = date_to_string(result.data, "Rejected_timestamp")
#         actual_output = self.parse_json["rejected_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_sp_export(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=rejected_transaction_report_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_rejected_transactions_report_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.rejected_transactions_report_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=rejected_transaction_report_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_discarded_transaction_report_rt(self, mock_middleware):
#         result = self.onboard.discarded_transaction_report_rt(self.request)
#         formatted_output = date_to_string(result.data, "Abandoned_timestamp")
#         actual_output = self.parse_json["abandoned_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_discarded_transaction_report_rt_export_csv(self, mock_middleware):
#         result = self.onboard.discarded_transaction_report_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=abandoned_transaction_report_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_discarded_transaction_report_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.discarded_transaction_report_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=abandoned_transaction_report_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_exception_transaction_report_rt(self, mock_middleware):
#         result = self.onboard.exception_transaction_report_rt(self.request)
#         formatted_output = date_to_string(result.data, "Last_modified_timestamp")
#         actual_output = self.parse_json["abandoned_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_exception_transaction_report_rt_export_csv(self, mock_middleware):
#         result = self.onboard.exception_transaction_report_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=exception_transaction_report_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_transaction_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_exception_transaction_report_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.exception_transaction_report_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=exception_transaction_report_rt.pdf",
#         )
