# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from unittest import mock
#
# from onboarding.tests.test_onboarding_stage_report_sp import date_to_string
# from onboarding.views.onboarding_stage_reports_views import StageReportViewSet
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "rw"
#
#
# path = f"{BASE_DIR}/tests/responses/onboarding_stage_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestOnboardingStageRT(APITestCase):
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
#             "timestamp__range": ["2022-09-11T00:00:00Z", "2023-09-30T00:00:00Z"]
#         }
#         self.onboard = StageReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_started_flow_retail(self, mock_middleware):
#         result = self.onboard.agent_started_flow_retail(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_cif_created_retail(self, mock_middleware):
#         result = self.onboard.agent_cif_created_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_cif_failed_retail(self, mock_middleware):
#         result = self.onboard.agent_cif_failed_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_rt(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["agent_success_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_successful_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_successful_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_rt(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["agent_failed_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_failed_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_failed_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_started_flow_retail(self, mock_middleware):
#         result = self.onboard.self_started_flow_retail(self.request)
#         self.assertEqual(result.data, {"count": 6})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_cif_created_retail(self, mock_middleware):
#         result = self.onboard.self_cif_created_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_cif_failed_retail(self, mock_middleware):
#         result = self.onboard.self_cif_failed_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_retail(self, mock_middleware):
#         result = self.onboard.self_discarded_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_rt(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["self_success_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_successful_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_successful_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_rt(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["self_failed_rt"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_failed_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_failed_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_rt(self, mock_middleware):
#         result = self.onboard.self_discarded_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Abandoned_timestamp"]
#         )
#         actual_output = self.parse_json["self_discarded_rt"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_rt_export(self, mock_middleware):
#         result = self.onboard.self_discarded_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_abandoned_applications.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.self_discarded_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_abandoned_applications.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_started_flow_retail(self, mock_middleware):
#         result = self.onboard.staff_started_flow_retail(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_cif_created_retail(self, mock_middleware):
#         result = self.onboard.staff_cif_created_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_cif_failed_retail(self, mock_middleware):
#         result = self.onboard.staff_cif_failed_retail(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_rt(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["staff_success_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=staff_successful_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=staff_successful_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_rt(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_rt(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["staff_failed_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_rt_export(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_rt_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=staff_failed_cif_details_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=staff_failed_cif_details_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_maker_bigNo_rt(self, mock_middleware):
#         result = self.onboard.applications_with_maker_bigNo_rt(self.request)
#         self.assertEqual(result.data, {"count": 2})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_verifier_bigNo_rt(self, mock_middleware):
#         result = self.onboard.applications_with_verifier_bigNo_rt(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_approvers_bigno_rt(self, mock_middleware):
#         result = self.onboard.applications_with_approvers_bigno_rt(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_processed_bigNo_rt(self, mock_middleware):
#         result = self.onboard.applications_processed_bigNo_rt(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_rejected_bigNo_rt(self, mock_middleware):
#         result = self.onboard.applications_rejected_bigNo_rt(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_exceptions_bigNo_rt(self, mock_middleware):
#         result = self.onboard.applications_exceptions_bigNo_rt(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_overall_application_stages_rt_stacked(self, mock_middleware):
#         result = self.onboard.overall_application_stages_rt_stacked(self.request)
#         actual_output = self.parse_json["stacked_bar_rt"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_queuecodes_pie_rt(self, mock_middleware):
#         result = self.onboard.agent_queuecodes_pie_rt(self.request)
#         actual_output = [
#             {"label": "Exceptions", "count": 1},
#             {"label": "Rejected", "count": 1},
#             {"label": "Successful", "count": 1},
#         ]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_queuecodes_pie_rt(self, mock_middleware):
#         result = self.onboard.staff_queuecodes_pie_rt(self.request)
#         actual_output = [
#             {"label": "In Progress", "count": 1},
#             {"label": "Rejected", "count": 1},
#             {"label": "Successful", "count": 1},
#         ]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_queuecodes_pie_rt(self, mock_middleware):
#         result = self.onboard.self_queuecodes_pie_rt(self.request)
#         actual_output = self.parse_json["self_pie_rt"]
#         self.assertEqual(list(result.data), actual_output)
