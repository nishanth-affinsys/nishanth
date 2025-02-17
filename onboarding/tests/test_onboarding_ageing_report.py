# import json
# from datetime import datetime
# from unittest import mock
#
#
# import pytz
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from onboarding.views.onboarding_ageing_report_views import AgeingReportViewSet
#
# from django.conf import settings
#
#
# def get_current_tenant_name():
#     return "rw"
#
#
# path = f"{settings.BASE_DIR}/tests/responses/onboarding_ageing_responses.json"
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
# def mock_now():
#     tz_info = pytz.timezone(settings.TIME_ZONE)
#     return datetime(2023, 6, 23, 9, 8, 24, 172884, tz_info)
#
#
# class TestOnboardingAgeing(APITestCase):
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
#         self.onb = AgeingReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_rt(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_rt(self.request)
#         formatted_output = date_to_string(result.data, "Created_timestamp")
#         actual_output = self.parse_json["ageing_rt"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_rt_export_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_rt_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=application_ageing_retail.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_rt_export_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_rt_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=application_ageing_retail.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_sp(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_sp(self.request)
#         formatted_output = date_to_string(result.data, "Created_timestamp")
#         actual_output = self.parse_json["ageing_sp"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_sp_export_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_sp_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=application_ageing_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_application_ageing_report_sp_export_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.application_ageing_report_sp_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=application_ageing_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_rt(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_rt(self.request)
#         formatted_result = date_to_string(result.data, "Created_date")
#         actual_output = self.parse_json["agent_rt"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_rt_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_rt_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_agent_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_rt_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_rt_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_agent_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_rt(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_rt(self.request)
#         formatted_result = date_to_string(result.data, "Created_date")
#         actual_output = self.parse_json["staff_rt"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_rt_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_rt_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_staff_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_rt_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_rt_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_staff_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_rt(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_rt(self.request)
#         formatted_result = date_to_string(result.data, "Created_date")
#         actual_output = self.parse_json["self_rt"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_rt_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_rt_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_self_rt.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_rt_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_rt_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_self_rt.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_sp(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_sp(self.request)
#         formatted_result = date_to_string(result.data, "Created_date")
#         actual_output = self.parse_json["agent_sp"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_sp_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_sp_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_agent_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_agent_sp_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_agent_sp_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_agent_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_sp(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_sp(self.request)
#         formatted_result = date_to_string(result.data, "Created_date")
#         actual_output = self.parse_json["staff_sp"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_sp_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_sp_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_staff_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_staff_sp_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_staff_sp_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_staff_sp.pdf",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_sp(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_sp(self.request)
#         actual_output = self.parse_json["self_sp"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_sp_csv(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_sp_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=scheduled_report_self_sp.csv",
#         )
#
#     @mock.patch(
#         "onboarding.services.onboarding_ageing_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     @mock.patch("onboarding.services.onboarding_ageing_report_utils.datetime")
#     def test_scheduled_ageing_report_self_sp_pdf(self, mock_date, mock_middleware):
#         mock_date.now.return_value = mock_now()
#         result = self.onb.scheduled_ageing_report_self_sp_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=scheduled_report_self_sp.pdf",
#         )
