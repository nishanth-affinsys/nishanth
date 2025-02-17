# import json
#
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from console.views.reports_views import ReportsAtGlanceViewSet
# from unittest import mock
#
#
# def get_current_tenant_name():
#     return "lebacpsix"
#
#
# def datetime_to_string(data):
#     response_list = []
#     for result in data:
#         result_dict = result.copy()
#         result_dict["Date"] = str(result_dict["Date"])
#         response_list.append(result_dict)
#     return response_list
#
#
# class TestReportAtGlance(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["tests/fixtures/messagelog.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2022-01-01T00:00:00Z", "2023-9-20T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.bot = ReportsAtGlanceViewSet()
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_customer(self, mock_middleware):
#         result = self.bot.active_customer(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "Active_Customer": 3}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_session_per_day(self, mock_middleware):
#         result = self.bot.session_per_day(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "Total_sessions": 3}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_session_per_user(self, mock_middleware):
#         result = self.bot.session_per_user(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "sessions_per_user": 1}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session(self, mock_middleware):
#         result = self.bot.total_session(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "total_session": 3}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_cust_per_day(self, mock_middleware):
#         result = self.bot.cust_per_day(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "cust_per_day": 3}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session(self, mock_middleware):
#         result = self.bot.message_per_session(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "message_per_session": 1}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.report_at_glance_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_linechart(self, mock_middleware):
#         result = self.bot.average_session_time_linechart(self.request)
#         formatted_result = datetime_to_string(result.data)
#         actual_output = [
#             {
#                 "Date": "2023-01-03",
#                 "Average Session Time": 40.043,
#                 "displayAverage Session Time": "00:00:40",
#             }
#         ]
#         self.assertEqual(formatted_result, actual_output)
