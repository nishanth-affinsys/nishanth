# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from unittest import mock
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
# def date_to_string(data, keys):
#     for item in data["results"]:
#         for key in keys:
#             item[key] = str(item[key])
#     return data
#
#
# class TestOnboardingStageSP(APITestCase):
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
#             "timestamp__range": ["2021-01-11T00:00:00Z", "2023-11-30T00:00:00Z"]
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
#     def test_agent_started_flow_sp(self, mock_middleware):
#         result = self.onboard.agent_started_flow_sp(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_cif_created_sp(self, mock_middleware):
#         result = self.onboard.agent_cif_created_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_cif_failed_sp(self, mock_middleware):
#         result = self.onboard.agent_cif_failed_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_sp(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["agent_success_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_successful_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_successful_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.agent_successful_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_successful_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_sp(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["agent_failed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_failed_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_failed_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.agent_failed_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_failed_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_started_flow_sp(self, mock_middleware):
#         result = self.onboard.self_started_flow_sp(self.request)
#         self.assertEqual(result.data, {"count": 4})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_cif_failed_sp(self, mock_middleware):
#         result = self.onboard.self_cif_failed_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_sp(self, mock_middleware):
#         result = self.onboard.self_discarded_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_sp(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["self_success_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_successful_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_successful_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.self_successful_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_successful_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_sp(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["self_failed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_failed_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_failed_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.self_failed_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_failed_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_sp(self, mock_middleware):
#         result = self.onboard.self_discarded_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Abandoned_timestamp"]
#         )
#         actual_output = self.parse_json["self_discarded_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_sp_export(self, mock_middleware):
#         result = self.onboard.self_discarded_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=self_abandoned_applications_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_discarded_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.self_discarded_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=self_abandoned_applications_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_started_flow_sp(self, mock_middleware):
#         result = self.onboard.staff_started_flow_sp(self.request)
#         self.assertEqual(result.data, {"count": 4})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_cif_created_sp(self, mock_middleware):
#         result = self.onboard.staff_cif_created_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_cif_failed_sp(self, mock_middleware):
#         result = self.onboard.staff_cif_failed_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_sp(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Approved_timestamp"]
#         )
#         actual_output = self.parse_json["staff_success_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=staff_successful_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_successful_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.staff_successful_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=staff_successful_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_sp(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_sp(self.request)
#         formatted_output = date_to_string(
#             result.data, ["Created_timestamp", "Rejected_timestamp"]
#         )
#         actual_output = self.parse_json["staff_failed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_sp_export(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_sp_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=staff_failed_cif_details_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_failed_cif_details_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.staff_failed_cif_details_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=staff_failed_cif_details_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_maker_bigNo_sp(self, mock_middleware):
#         result = self.onboard.applications_with_maker_bigNo_sp(self.request)
#         self.assertEqual(result.data, {"count": 2})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_approvers_bigno_sp(self, mock_middleware):
#         result = self.onboard.applications_with_approvers_bigno_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_processed_bigNo_sp(self, mock_middleware):
#         result = self.onboard.applications_processed_bigNo_sp(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_rejected_bigNo_sp(self, mock_middleware):
#         result = self.onboard.applications_rejected_bigNo_sp(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_with_verifier_bigNo_sp(self, mock_middleware):
#         result = self.onboard.applications_with_verifier_bigNo_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_overall_application_stages_sp_stacked(self, mock_middleware):
#         result = self.onboard.overall_application_stages_sp_stacked(self.request)
#         actual_output = self.parse_json["stacked_bar_sp"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_queuecodes_pie_sp(self, mock_middleware):
#         result = self.onboard.agent_queuecodes_pie_sp(self.request)
#         actual_output = [
#             {"label": "Pending Approval", "count": 1},
#             {"label": "Rejected", "count": 1},
#             {"label": "Successful", "count": 1},
#         ]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_staff_queuecodes_pie_sp(self, mock_middleware):
#         result = self.onboard.staff_queuecodes_pie_sp(self.request)
#         actual_output = [
#             {"label": "In Progress", "count": 1},
#             {"label": "Pending Verification", "count": 1},
#             {"label": "Rejected", "count": 1},
#             {"label": "Successful", "count": 1},
#         ]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_stage_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_self_queuecodes_pie_sp(self, mock_middleware):
#         result = self.onboard.self_queuecodes_pie_sp(self.request)
#         actual_output = [
#             {"label": "Abandoned", "count": 1},
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
#     def test_self_cif_created_sp(self, mock_middleware):
#         result = self.onboard.self_cif_created_sp(self.request)
#         self.assertEqual(result.data, {"count": 1})
