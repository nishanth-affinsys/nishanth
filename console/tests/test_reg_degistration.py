# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from console.views.reg_deregistration import RegDeregViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "stanbickenya"
#
#
# path = f"{BASE_DIR}/tests/responses/reg_deregistration_responses.json"
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# def datetime_to_string(result):
#     modified_result = result.copy()
#     for item in modified_result["results"]:
#         item["Date"] = str(item["Date"])
#     return modified_result
#
#
# class TestRegDeregistration(APITestCase):
#     databases = {"analytics"}
#     fixtures = [
#         "tests/fixtures/netregistrationactivity.json",
#         "tests/fixtures/latestregistrationactivity.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.reg = RegDeregViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_net_registration_activity(self, mock_middleware):
#         result = self.reg.net_registration_activity(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = self.parse_json["net_reg_activity"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_net_registration_activity_export(self, mock_middleware):
#         result = self.reg.net_registration_activity_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=net_registration_activities.csv",
#         )
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_net_registration_activity_export_pdf(self, mock_middleware):
#         result = self.reg.net_registration_activity_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=net_registration_activities.pdf",
#         )
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_registrations_bigno(self, mock_middleware):
#         result = self.reg.number_of_registrations_bigno(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_deregistrations_bigno(self, mock_middleware):
#         result = self.reg.number_of_deregistrations_bigno(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_registrations_list(self, mock_middleware):
#         result = self.reg.number_of_registrations_list(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["register_list"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_registrations_list_export(self, mock_middleware):
#         result = self.reg.number_of_registrations_list_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=registrations_list.csv",
#         )
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_registrations_list_export_pdf(self, mock_middleware):
#         result = self.reg.number_of_registrations_list_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=registrations_list.pdf",
#         )
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_deregistrations_list(self, mock_middleware):
#         result = self.reg.number_of_deregistrations_list(self.request)
#         formatted_output = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["deregister_list"]
#         self.assertEqual(formatted_output, actual_output)
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_deregistrations_list_export(self, mock_middleware):
#         result = self.reg.number_of_deregistrations_list_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=deregistrations_list.csv",
#         )
#
#     @mock.patch(
#         "console.services.reg_deregistration_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_deregistrations_list_export_pdf(self, mock_middleware):
#         result = self.reg.number_of_deregistrations_list_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=deregistrations_list.pdf",
#         )
