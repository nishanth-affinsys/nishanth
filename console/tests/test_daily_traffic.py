# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from console.views.daily_traffic_views import DailyTrafficViewSet
# from unittest import mock
# from main.utils.boiler_plate import get_generic_response
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebacpsix"
#
#
# path = f"{BASE_DIR}/tests/responses/bot_reports_responses.json"
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
#         {"Date": item["Date"].strftime("%Y-%m-%d"), "count": item["count"]}
#         for item in data
#     ]
#
#
# class TestDailyTraffic(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["tests/fixtures/messagelog.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.daily = DailyTrafficViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users_periodic(self, mock_middleware):
#         result = self.daily.total_users_periodic(self.request)
#         self.assertIsInstance(result.data, dict)
#         self.assertIsInstance(result.data["count"], int)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users_periodic_export_csv(self, mock_middleware):
#         result = self.daily.total_users_periodic_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_users_periodic.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users_periodic_export_pdf(self, mock_middleware):
#         result = self.daily.total_users_periodic_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=total_users_periodic.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users(self, mock_middleware):
#         result = self.daily.total_users(self.request)
#         formatted_actual_data = datetime_to_string(result.data)
#         actual_output = [{"Date": "2023-01-03", "count": 3}]
#         self.assertEqual(formatted_actual_data, actual_output)
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users_export_csv(self, mock_middleware):
#         result = self.daily.total_users_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "attachment; filename=total_users.csv"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_users_export_pdf(self, mock_middleware):
#         result = self.daily.total_users_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=total_users.pdf"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions_periodic(self, mock_middleware):
#         result = self.daily.total_sessions_periodic(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions_periodic_export_csv(self, mock_middleware):
#         result = self.daily.total_sessions_periodic_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_sessions_periodic.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions_periodic_export_pdf(self, mock_middleware):
#         result = self.daily.total_sessions_periodic_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=total_sessions_periodic.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions(self, mock_middleware):
#         result = self.daily.total_sessions(self.request)
#         formatted_result = datetime_to_string(result.data)
#         self.assertEqual(formatted_result, [{"Date": "2023-01-03", "count": 3}])
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions_export_csv(self, mock_middleware):
#         result = self.daily.total_sessions_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "attachment; filename=total_sessions.csv"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_sessions_export_pdf(self, mock_middleware):
#         result = self.daily.total_sessions_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=total_sessions.pdf"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_users_periodic(self, mock_middleware):
#         result = self.daily.sessions_per_users_periodic(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_users_periodic_export_csv(self, mock_middleware):
#         result = self.daily.sessions_per_users_periodic_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=sessions_per_users_periodic.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_users_periodic_export_pdf(self, mock_middleware):
#         result = self.daily.sessions_per_users_periodic_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=sessions_per_users_periodic.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_user(self, mock_middleware):
#         result = self.daily.sessions_per_user(self.request)
#         formatted_result = datetime_to_string(result.data)
#         self.assertEqual(formatted_result, [{"Date": "2023-01-03", "count": 1}])
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_user_export_csv(self, mock_middleware):
#         result = self.daily.sessions_per_user_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=sessions_per_user.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_sessions_per_user_export_pdf(self, mock_middleware):
#         result = self.daily.sessions_per_user_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=sessions_per_user.pdf"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_periodic(self, mock_middleware):
#         result = self.daily.message_per_session_periodic(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_periodic_export_csv(self, mock_middleware):
#         result = self.daily.message_per_session_periodic_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=sessions_per_users_periodic.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_periodic_export_pdf(self, mock_middleware):
#         result = self.daily.message_per_session_periodic_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=sessions_per_users_periodic.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session(self, mock_middleware):
#         result = self.daily.message_per_session(self.request)
#         formatted_result = datetime_to_string(result.data)
#         self.assertEqual(formatted_result, [{"Date": "2023-01-03", "count": 1}])
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_export_csv(self, mock_middleware):
#         result = self.daily.message_per_session_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=messages_per_session.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_export_pdf(self, mock_middleware):
#         result = self.daily.message_per_session_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=messages_per_session.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_per_session_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.daily.message_per_session_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=messages_per_session.pdf",
#             )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_periodic(self, mock_middleware):
#         result = self.daily.total_session_time_periodic(self.request)
#         self.assertEqual(result.data, {"count": 120.129, "display": "00:02:00"})
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_periodic_export_csv(self, mock_middleware):
#         result = self.daily.total_session_time_periodic_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_session_time_periodic.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_periodic_export_pdf(self, mock_middleware):
#         result = self.daily.total_session_time_periodic_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=total_session_time_periodic.pdf",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_test_total_session_time_periodic_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.daily.total_session_time_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=total_session_time.pdf",
#             )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time(self, mock_middleware):
#         result = self.daily.total_session_time(self.request)
#         formatted_result = datetime_to_string(result.data)
#         self.assertEqual(formatted_result, [{"Date": "2023-01-03", "count": 120.129}])
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_export_csv(self, mock_middleware):
#         result = self.daily.total_session_time_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_session_time.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_export_pdf(self, mock_middleware):
#         result = self.daily.total_session_time_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=total_session_time.pdf"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_or_not(self, mock_middleware):
#         result = self.daily.handled_or_not(self.request)
#         self.assertEqual(list(result.data), [{"label": "Y", "count": 4}])
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_message(self, mock_middleware):
#         result = self.daily.handled_message(self.request)
#         actual_output = {
#             "count": 3,
#             "next": None,
#             "previous": None,
#             "results": [
#                 {"Message": "hi", "count": 2},
#                 {"Message": "cards", "count": 1},
#                 {"Message": "heyy", "count": 1},
#             ],
#         }
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_msg_export_csv(self, mock_middleware):
#         result = self.daily.handled_msg_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=handled_messages.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_msg_export_pdf(self, mock_middleware):
#         result = self.daily.handled_msg_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=handled_messages.pdf"
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_msg_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=2):
#             result = self.daily.handled_msg_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=handled_messages.pdf",
#             )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_unhandled_message(self, mock_middleware):
#         result = self.daily.unhandled_message(self.request)
#         actual_output = {"count": 0, "next": None, "previous": None, "results": []}
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_unhandled_msg_export_csv(self, mock_middleware):
#         result = self.daily.unhandled_msg_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=unhandled_messages.csv",
#         )
#
#     @mock.patch(
#         "console.services.daily_traffic_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_msg_export_pdf(self, mock_middleware):
#         result = self.daily.unhandled_msg_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=unhandled_messages.pdf"
#         )
