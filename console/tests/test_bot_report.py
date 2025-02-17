# import json
#
# from django.db.models import QuerySet
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from console.views.bot_reports_views import BotChartsViewSet
# from handoff.views.live_reports_views import LiveDataViewSet
# from handoff.views.detail_report_views import DetailReportViewSet
#
# from unittest import mock
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
# class TestBotReport(APITestCase):
#     # databases = {"analytics", "handoff"}
#     fixtures = [
#         "console/tests/fixtures/messagelog.json",
#         "console/tests/fixtures/analyticssocialevent.json",
#         "console/tests/fixtures/socialconversationagent.json",
#         "console/tests/fixtures/socialconversationtempsocialuser.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.bot = BotChartsViewSet()
#         self.live = LiveDataViewSet()
#         self.detail = DetailReportViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_faq(self, mock_middleware):
#         result = self.bot.messages_faq(self.request)
#         actual_output = self.parse_json["message_faq"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_faq_messages_export_csv(self, mock_middleware):
#         result = self.bot.faq_messages_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=bot_messages.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_faq_messages_export_pdf(self, mock_middleware):
#         result = self.bot.faq_messages_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=bot_messages.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_faq_messages_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.faq_messages_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"), "inline; filename=bot_messages.pdf"
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_message(self, mock_middleware):
#         result = self.bot.total_message(self.request)
#         actual_output = self.parse_json["total_message"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_messages_export_csv(self, mock_middleware):
#         result = self.bot.total_messages_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=messages_by_session.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_messages_export_pdf(self, mock_middleware):
#         result = self.bot.total_messages_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=messages_by_session.pdf",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_messages_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.total_messages_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=messages_by_session.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_intents(self, mock_middleware):
#         result = self.bot.top_intents(self.request)
#         actual_output = self.parse_json["top_intents"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_intent_export_csv(self, mock_middleware):
#         result = self.bot.top_intent_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=top_matched_intents.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_intent_export_pdf(self, mock_middleware):
#         result = self.bot.top_intent_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=top_matched_intents.pdf",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_intent_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.top_intent_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=top_matched_intents.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_messages(self, mock_middleware):
#         result = self.bot.top_messages(self.request)
#         actual_output = self.parse_json["topMessage"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_messages_export_csv(self, mock_middleware):
#         result = self.bot.top_messages_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=top_messages.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_messages_export_pdf(self, mock_middleware):
#         result = self.bot.top_messages_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=top_messages.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_messages_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.top_messages_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"), "inline; filename=top_messages.pdf"
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_matched_intents(self, mock_middleware):
#         result = self.bot.total_matched_intents(self.request)
#         actual_output = self.parse_json["matched_intents"]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_intents_matched_export_csv(self, mock_middleware):
#         result = self.bot.total_intents_matched_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_intents_by_channel.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_intents_matched_export_pdf(self, mock_middleware):
#         result = self.bot.total_intents_matched_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=total_intents_by_channel.pdf",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_ten_matched_intents_by_channel(self, mock_middleware):
#         result = self.bot.top_ten_matched_intents_by_channel(self.request)
#         actual_output = self.parse_json["top_10_matched_intents"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_ten_matched_intents_by_channel_export_csv(self, mock_middleware):
#         result = self.bot.top_ten_matched_intents_by_channel_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=matched_intents.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_ten_matched_intents_by_channel_export_pdf(self, mock_middleware):
#         result = self.bot.top_messages_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=matched_intents.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_ten_matched_intents_by_channel_export_pdf(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.top_ten_matched_intents_by_channel_export_pdf(
#                 self.request
#             )
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=matched_intents.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_unmatched_intents(self, mock_middleware):
#         result = self.bot.total_unmatched_intents(self.request)
#         actual_output = self.parse_json["unmatched_intents"]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_intents_unmatched_export_csv(self, mock_middleware):
#         result = self.bot.total_intents_unmatched_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=total_unmatched_intents.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_intents_unmatched_export_pdf(self, mock_middleware):
#         result = self.bot.total_intents_unmatched_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=total_unmatched_intents.pdf",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_active_customers(self, mock_middleware):
#         result = self.bot.total_active_customers(self.request)
#         actual_output = self.parse_json["active_customers"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_customers_export_csv(self, mock_middleware):
#         result = self.bot.active_customers_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=active_customers.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_customers_export_pdf(self, mock_middleware):
#         result = self.bot.active_customers_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=active_customers.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_active_customers_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.active_customers_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=active_customers.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_number_of_users_interactions(self, mock_middleware):
#         result = self.bot.number_of_users_interactions(self.request)
#         actual_output = self.parse_json["user_interactions"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_user_interactions_export_csv(self, mock_middleware):
#         result = self.bot.user_interactions_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=user_interactions.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_user_interactions_export_pdf(self, mock_middleware):
#         result = self.bot.user_interactions_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=user_interactions.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_user_interactions_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.user_interactions_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=user_interactions.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time(self, mock_middleware):
#         result = self.bot.average_session_time(self.request)
#         actual_output = self.parse_json["avg_session_time"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_export_csv(self, mock_middleware):
#         result = self.bot.average_session_time_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=avg_session_time.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_export_pdf(self, mock_middleware):
#         result = self.bot.average_session_time_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=avg_session_time.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.average_session_time_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=avg_session_time.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_message(self, mock_middleware):
#         result = self.bot.average_message(self.request)
#         actual_output = self.parse_json["avg_message"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_message_export_csv(self, mock_middleware):
#         result = self.bot.average_message_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=avg_msg_per_session.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_message_export_pdf(self, mock_middleware):
#         result = self.bot.average_message_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=avg_msg_per_session.pdf",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_message_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.average_message_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=avg_msg_per_session.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_bot(self, mock_middleware):
#         result = self.bot.new_user_in_bot(self.request)
#         formatted_result = date_to_string(result.data, "Time")
#         actual_output = self.parse_json["new_user_bot"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_bot_export(self, mock_middleware):
#         result = self.bot.new_user_in_bot_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=new_user_in_BOT.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_bot_export_pdf(self, mock_middleware):
#         result = self.bot.new_user_in_bot_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=new_user_in_BOT.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_new_user_in_bot_export_pdf_env(self, mock_middleware):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.bot.new_user_in_bot_export_pdf(self.request)
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"),
#                 "inline; filename=new_user_in_BOT.pdf",
#             )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Conversations(self, mock_middleware):
#         result = self.bot.conversations(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = self.parse_json["conversations"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_conversations_export(self, mock_middleware):
#         result = self.bot.conversations_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "attachment; filename=conversations.csv"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_conversations_export_pdf(self, mock_middleware):
#         result = self.bot.conversations_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=conversations.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Returning_user_in_bot(self, mock_middleware):
#         result = self.bot.returning_user_in_bot(self.request)
#         actual_output = self.parse_json["returning_user_bot"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_return_user_in_bot_export(self, mock_middleware):
#         result = self.bot.return_user_in_bot_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Return_user_in_BOT.csv",
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_return_user_in_bot_export_pdf(self, mock_middleware):
#         result = self.bot.return_user_in_bot_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=Return_user_in_BOT.pdf"
#         )
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_user_flow_shankey_chart(self, mock_middleware):
#         result = self.bot.user_flow_shankey_chart(self.request)
#         self.assertEqual(list(result.data["values"]), [])
#         self.assertEqual(list(result.data["links"]), [])
#
#     @mock.patch(
#         "console.services.bot_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_user_messages_heatmap(self, mock_middleware):
#         result = self.bot.user_messages_heatmap(self.request)
#         result_date_range = [
#             [date.strftime("%Y-%m-%d") for date in date_range]
#             for date_range in result.data["date_range"]
#         ]
#         result_values = [
#             {"date": date["date"].strftime("%Y-%m-%d"), "count": date["count"]}
#             for date in result.data["values"]
#         ]
#         actual_output = self.parse_json["heat_map"]
#         self.assertEqual(result_date_range, actual_output["date_range"])
#         self.assertEqual(result_values, actual_output["values"])
#
#     # for live report charts which refers to event database
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_online_customers_bot(self, mock_middleware):
#         result = self.live.online_customers_bot(self.request)
#         self.assertIsInstance(result.data, dict)
#         self.assertIsInstance(result.data["count"], int)
#         self.assertGreaterEqual(result.data["count"], 0)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_Conversations_live(self, mock_middleware):
#         result = self.live.conversations_live(self.request)
#         actual_output = self.parse_json["conversations_live"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_top_messages_live(self, mock_middleware):
#         result = self.live.top_messages_live(self.request)
#         actual_output = self.parse_json["top_message_live"]
#         self.assertEqual(result.data, actual_output)
#
#     # for detail report charts
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_message_from_user_to_bot(self, mock_middleware):
#         result = self.detail.total_message_from_user_to_bot(self.request)
#         self.assertEqual(result.data, {"count": 3})
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_bot_interactions(self, mock_middleware):
#         result = self.detail.bot_interactions(self.request)
#         self.assertIsInstance(result.data, QuerySet)
#         self.assertGreaterEqual(len(result.data), 0)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_chatbot_message_interactions(self, mock_middleware):
#         result = self.detail.chatbot_message_interactions(self.request)
#         actual_output = self.parse_json["chatbot_message_interactions"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_chatbot_message_interactions_export(self, mock_middleware):
#         result = self.detail.chatbot_message_interactions_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=chatbot_messages_interactions.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Channel,Total_messages_user_to_agent,Total_messages_agent_to_user,Total_messages_user_to_bot"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.detail_queue_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_chatbot_message_interactions_export_pdf(self, mock_middleware):
#         result = self.detail.chatbot_message_interactions_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=chatbot_messages_interactions.pdf",
#         )
