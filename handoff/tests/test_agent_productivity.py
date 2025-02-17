# import json
#
#
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from handoff.views.agent_productivity_views import AgentProductivityViewSet
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
# class TestAgentProductivity(APITestCase):
#     databases = {"handoff"}
#     fixtures = [
#         "tests/fixtures/analyticssocialevent.json",
#         "tests/fixtures/agenttransfer.json",
#         "tests/fixtures/socialconversationagent.json",
#         "tests/fixtures/socialconversationtempsocialuser.json",
#         "tests/fixtures/agentproductivity.json",
#         "tests/fixtures/auditloglogentry.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2021-01-11T00:00:00Z", "2023-09-28T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.productivity = AgentProductivityViewSet()
#         self.parse_json = parse_json(path)
#         self.csv_content = "text/csv"
#         self.pdf_content = "application/pdf"
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_routing(self, mock_middleware):
#         result = self.productivity.agent_routing(self.request)
#         formatted_result = date_to_string(result.data, "initialized_time")
#         actual_output = self.parse_json["agent_routing"]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_routing_export(self, mock_middleware):
#         result = self.productivity.agent_routing_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_routing.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"username,agent_routed,session_id,channel,agent_accept,accepted_time(Seconds),initialized_time"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_routing_export_pdf(self, mock_middleware):
#         result = self.productivity.agent_routing_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_routing.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_login_status(self, mock_middleware):
#         result = self.productivity.agent_login_status(self.request)
#         actual_output = self.parse_json["agent_login"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_login_status_export(self, mock_middleware):
#         result = self.productivity.agent_login_status_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_login_status.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(result.content.startswith(b"Agent_Name,Status,Timestamp"))
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_login_status_export_pdf(self, mock_middleware):
#         result = self.productivity.agent_login_status_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_login_status.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_availability(self, mock_middleware):
#         result = self.productivity.agent_availability(self.request)
#         actual_output = self.parse_json["agent_availability"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_availability_export(self, mock_middleware):
#         result = self.productivity.agent_availability_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=agent_availability_status.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(result.content.startswith(b"Agent_name,Status,Timestamp"))
#
#     @mock.patch(
#         "handoff.services.agent_productivity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_availability_export_pdf(self, mock_middleware):
#         result = self.productivity.agent_availability_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=agent_availability_status.pdf",
#         )
#         self.assertTrue(result.content)
