# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from handoff.views.agent_reports_views import AgentReportViewSet
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
# def date_to_string(data):
#     for item in data["results"]:
#         item["Date"] = str(item["Date"])
#     return data
#
#
# class TestAgentReports(APITestCase):
#     databases = {"handoff"}
#     fixtures = [
#         "tests/fixtures/analyticssocialevent.json",
#         "tests/fixtures/handoffflow.json",
#         "tests/fixtures/socialconversationagent.json",
#         "tests/fixtures/socialconversationtempsocialuser.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2021-03-11T00:00:00Z", "2023-07-28T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.agent = AgentReportViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_arrived_bigNumber(self, mock_middleware):
#         result = self.agent.interaction_arrived_bignumber(self.request)
#         self.assertEqual(list(result.data), [{"Channel": "webchat", "Count": 1}])
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_arrived(self, mock_middleware):
#         result = self.agent.interaction_arrived(self.request)
#         actual_output = self.parse_json["interactions_arrived"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_arrived_export(self, mock_middleware):
#         result = self.agent.interaction_arrived_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=interactions.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(b"Agent Name,Date,Channel,Interactions")
#         )
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_arrived_details_export_pdf(self, mock_middleware):
#         result = self.agent.interaction_arrived_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=interactions.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_accepted_channelwise(self, mock_middleware):
#         result = self.agent.interaction_accepted_channelwise(self.request)
#         self.assertEqual(list(result.data), [{"Channel": "webchat", "Count": 1}])
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_accepted(self, mock_middleware):
#         result = self.agent.interaction_accepted(self.request)
#         actual_output = self.parse_json["interactions_accepted"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_accepted_export(self, mock_middleware):
#         result = self.agent.interaction_accepted_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=interactions.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(b"Agent Name,Date,Channel,Interactions")
#         )
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_accepted_export_pdf(self, mock_middleware):
#         result = self.agent.interaction_accepted_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=interactions.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time(self, mock_middleware):
#         result = self.agent.average_session_time(self.request)
#         formatted_result = date_to_string(result.data)
#         actual_output = self.parse_json["avg_session_time"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_export(self, mock_middleware):
#         result = self.agent.average_session_time_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=average_handling_time.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Agent Name,Date,Channel,Average Handling time(in Minutes)"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_average_session_time_export_pdf(self, mock_middleware):
#         result = self.agent.average_session_time_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=average_handling_time.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_entered_accepted(self, mock_middleware):
#         result = self.agent.entered_accepted(self.request)
#         actual_output = self.parse_json["entered_queue"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_entered_accepted_export(self, mock_middleware):
#         result = self.agent.entered_accepted_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Aggregate_agents_report.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"channel,Entered_in_Queue,Accepted_by_Agent,Unhandled_Chats,Abandoned_Chats"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_entered_accepted_pdf_download(self, mock_middleware):
#         result = self.agent.entered_accepted_pdf_download(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=Aggregate_agents_report.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_messages_in_each_interactions(self, mock_middleware):
#         result = self.agent.messages_in_each_interactions(self.request)
#         for item in result.data["results"]:
#             item["Timestamp"] = str(item["Timestamp"])
#         actual_output = self.parse_json["messages_in_interactions"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_messages_in_interactions_export(self, mock_middleware):
#         result = self.agent.messages_in_interactions_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=messages_interactions.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Agent_Name,Customer_Name,Session,Channel,Timestamp,Count"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_messages_in_interactions_export_pdf(self, mock_middleware):
#         result = self.agent.messages_in_interactions_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=messages_interactions.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_reports_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handoff_flow_shankey_chart(self, mock_middleware):
#         result = self.agent.handoff_flow_shankey_chart(self.request)
#         actual_output = self.parse_json["sankey_chart"]
#         self.assertEqual(list(result.data["values"]), actual_output["values"])
#         self.assertEqual(list(result.data["links"]), actual_output["links"])
