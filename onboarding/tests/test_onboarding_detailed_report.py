# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from unittest import mock
#
# from onboarding.tests.test_onboarding_stage_report_sp import date_to_string
# from onboarding.views.onboarding_detailed_report_views import DetailedReportViewSet
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "rw"
#
#
# path = f"{BASE_DIR}/tests/responses/onboarding_detailed_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestOnboardingDetailed(APITestCase):
#     databases = {"onboarding"}
#     fixtures = [
#         "tests/fixtures/detailedreporttablert.json",
#         "tests/fixtures/detailedreporttablesp.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2022-08-11T00:00:00Z", "2023-08-30T00:00:00Z"]
#         }
#         self.onboard = DetailedReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_rt(self, mock_middleware):
#         result = self.onboard.applications_report_agent_rt(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["agent_detailed_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_rt_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_agent_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_agent_rt.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_agent_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_agent_rt.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_sp(self, mock_middleware):
#         result = self.onboard.applications_report_agent_sp(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["agent_detailed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_sp_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_agent_sp_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_agent_SP.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_agent_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_agent_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_agent_SP.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_rt(self, mock_middleware):
#         result = self.onboard.applications_report_self_rt(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["self_detailed_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_rt_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_self_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_self_RT.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_self_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_self_RT.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_sp(self, mock_middleware):
#         result = self.onboard.applications_report_self_sp(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["self_detailed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_sp_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_self_sp_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_self_SP.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_self_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_self_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_self_SP.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_rt(self, mock_middleware):
#         result = self.onboard.applications_report_staff_rt(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["staff_detailed_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_rt_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_staff_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_staff_RT.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_rt_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_staff_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_staff_RT.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_sp(self, mock_middleware):
#         result = self.onboard.applications_report_staff_sp(self.request)
#         formatted_output = date_to_string(
#             result.data,
#             [
#                 "Created_timestamp",
#                 "Last_modified_timestamp",
#                 "Verified_timestamp",
#                 "Approved_timestamp",
#             ],
#         )
#         actual_output = self.parse_json["staff_detailed_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_sp_export_csv(self, mock_middleware):
#         result = self.onboard.applications_report_staff_sp_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=applications_report_staff_SP.csv",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "onboarding.services.onboarding_detailed_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_applications_report_staff_sp_export_pdf(self, mock_middleware):
#         result = self.onboard.applications_report_staff_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=applications_report_staff_SP.pdf",
#         )
#         self.assertTrue(result.content)
