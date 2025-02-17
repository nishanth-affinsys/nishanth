# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from handoff.views.detail_report_views import DetailReportViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
# def get_current_tenant_name():
#     return "lebahandofffive"
#
#
# path = f"{BASE_DIR}/tests/responses/agent_reports_responses.json"
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
# class TestAgentDetailReport(APITestCase):
#     databases = {"handoff"}
#     fixtures = [
#         "tests/fixtures/analyticssocialevent.json",
#         "tests/fixtures/socialconversationagent.json",
#         "tests/fixtures/socialconversationtempsocialuser.json",
#         "tests/fixtures/newuserinhandoff.json",
#         "tests/fixtures/returninguserinhandoff.json",
#         "tests/fixtures/abondaneddetails.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2021-03-11T00:00:00Z", "2023-07-28T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.detail = DetailReportViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#         self.MAX_PDF_LIMIT = 500
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_entered_queue(self, mock_middleware):
#         result = self.detail.entered_queue(self.request)
#         self.assertEqual(result.data, {"count": 2})
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_accept(self, mock_middleware):
#         result = self.detail.agent_accept(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_abandoned_chats(self, mock_middleware):
#         result = self.detail.abandoned_chats(self.request)
#         actual_output = self.parse_json["abandoned_chats"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_message_from_user_to_agent(self, mock_middleware):
#         result = self.detail.total_message_from_user_to_agent(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_message_from_agent_to_user(self, mock_middleware):
#         result = self.detail.total_message_from_agent_to_user(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time(self, mock_middleware):
#         result = self.detail.total_session_time(self.request)
#         format_result = date_to_string(result.data, "Date")
#         actual_output = self.parse_json["total_session_time"]
#         self.assertEqual(format_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_export(self, mock_middleware):
#         result = self.detail.total_session_time_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Total_handled_time.csv",
#         )
#         self.assertTrue(
#             result.content.startswith(
#                 b"Agent Name,Date,Total Handling time(in Minutes)"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_session_time_export_pdf(self, mock_middleware):
#         result = self.detail.total_session_time_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=Total_handled_time.pdf",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_cust_req_for_handoff(self, mock_middleware):
#         result = self.detail.cust_req_for_handoff(self.request)
#         format_result = date_to_string(result.data, "Date")
#         actual_output = self.parse_json["cust_req_handoff"]
#         self.assertEqual(format_result, actual_output)
#
#     # @mock.patch(
#     #     "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#     #     side_effect=get_current_tenant_name,
#     # )
#     # def test_agent_interactions(self, mock_middleware):
#     #     result = self.detail.agent_interactions(self.request)
#     #     for item in result.data:
#     #         item["Date"] = str(item["Date"])
#     #     actual_output = [{"Date": "2023-04-26 09:34:06+00:00", "count": 1}]
#     #     self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_handoff(self, mock_middleware):
#         result = self.detail.new_user_in_handoff(self.request)
#         for item in result.data["results"]:
#             item["Timestamp"] = str(item["Timestamp"])
#         actual_output = self.parse_json["new_user_handoff"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_handoff_export(self, mock_middleware):
#         result = self.detail.new_user_in_handoff_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=user_in_handoff.csv",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_handoff_export_pdf(self, mock_middleware):
#         result = self.detail.new_user_in_handoff_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=user_in_handoff.pdf",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_returning_user_in_handoff(self, mock_middleware):
#         result = self.detail.returning_user_in_handoff(self.request)
#         for item in result.data["results"]:
#             item["Timestamp"] = str(item["Timestamp"])
#         actual_output = self.parse_json["returning_user_handoff"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_return_user_in_handoff_export(self, mock_middleware):
#         result = self.detail.return_user_in_handoff_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=user_in_handoff.csv",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_return_user_in_handoff_export_pdf(self, mock_middleware):
#         result = self.detail.return_user_in_handoff_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=user_in_handoff.pdf",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_abandoned_users_details(self, mock_middleware):
#         result = self.detail.abandoned_users_details(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["abandoned_users_details"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_abandoned_users_details_export(self, mock_middleware):
#         result = self.detail.abandoned_users_details_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=abandoned_chat_details.csv",
#         )
#         self.assertTrue(
#             result.content.startswith(
#                 b"Customer_name,Phone_Number,Email,Channel,Session,Timestamp"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_abandoned_users_details_export_pdf(self, mock_middleware):
#         result = self.detail.abandoned_users_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=abandoned_chat_details.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_seconds(self, mock_middleware):
#         result = self.detail.average_session_time_seconds(self.request)
#         formatted_result = date_to_string(result.data, "Date")
#         actual_output = self.parse_json["average_handling_time"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_seconds_export(self, mock_middleware):
#         result = self.detail.average_session_time_seconds_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=average_handling_time_mins.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Agent Name,Date,Average Handling time(in Minutes)"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_seconds_export_pdf(self, mock_middleware):
#         result = self.detail.average_session_time_seconds_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=average_handling_time_mins.pdf",
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_customer_activity(self, mock_middleware):
#         result = self.detail.customer_activity(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["customer_activity"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_customer_activity_export(self, mock_middleware):
#         result = self.detail.customer_activity_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=customer_activity.csv",
#         )
#         self.assertTrue(
#             result.content.startswith(
#                 b"Customer,Skill,Phone_Number,Email,Channel,Timestamp"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_customer_activity_export_pdf(self, mock_middleware):
#         result = self.detail.customer_activity_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=customer_activity.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_handoff_details(self, mock_middleware):
#         result = self.detail.agent_handoff_details(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["agent_handoff_details"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_handoff_details_export(self, mock_middleware):
#         result = self.detail.agent_handoff_details_export(self.request)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_handoff_details.csv",
#         )
#         self.assertTrue(
#             result.content.startswith(
#                 b"Agent_Name,Customer_Name,Phone_Number,Email,Channel,Timestamp"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_handoff_details_export_pdf(self, mock_middleware):
#         result = self.detail.agent_handoff_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_handoff_details.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handled_ended_chats(self, mock_middleware):
#         result = self.detail.handled_ended_chats(self.request)
#         actual_output = [{"label": "User Ended Chats", "count": 1}]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_unhandled_chats(self, mock_middleware):
#         result = self.detail.unhandled_chats(self.request)
#         actual_output = [{"label": "Agent Unavailable or Busy", "count": 1}]
#         self.assertEqual(list(result.data), actual_output)
