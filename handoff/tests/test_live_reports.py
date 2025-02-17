# import json
#
# from django.db.models import QuerySet
# from django.utils import timezone
# from datetime import timedelta
# from rest_framework.test import APITestCase, APIRequestFactory
# from handoff.views.live_reports_views import LiveDataViewSet
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
# class TestLiveReports(APITestCase):
#     databases = {"handoff"}
#     fixtures = [
#         "tests/fixtures/analyticssocialevent.json",
#         "tests/fixtures/agenttransfer.json",
#         "tests/fixtures/socialconversationagent.json",
#         "tests/fixtures/socialconversationtempsocialuser.json",
#         "tests/fixtures/agentskill.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.live = LiveDataViewSet()
#         self.today = timezone.now() - timedelta(minutes=3)
#         self.tomorrow = timezone.now()
#         self.parse_json = parse_json(path)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_online_agents(self, mock_middleware):
#         result = self.live.online_agents(self.request)
#         self.assertGreaterEqual(result.data["count"], 0)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_message_agent_and_user(self, mock_middleware):
#         result = self.live.message_agent_and_user(self.request)
#         self.assertGreaterEqual(result.data["count"], 0)
#         self.assertTrue(self.today <= self.tomorrow)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_chats_in_queue(self, mock_middleware):
#         result = self.live.chats_in_queue(self.request)
#         self.assertIsInstance(result.data["count"], int)
#         self.assertGreaterEqual(result.data["count"], 0)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_chats_in_queue_detail(self, mock_middleware):
#         result = self.live.chats_in_queue_detail(self.request)
#         self.assertIsInstance(result.data["results"], list)
#         self.assertGreaterEqual(result.data["results"], [])
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handoff_called_today(self, mock_middleware):
#         result = self.live.handoff_called_today(self.request)
#         self.assertIsInstance(result.data, dict)
#         self.assertIsInstance(result.data["count"], int)
#         self.assertGreaterEqual(result.data["count"], 0)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_online_detail(self, mock_middleware):
#         result = self.live.online_detail(self.request)
#         self.assertIsInstance(result.data, dict)
#         self.assertIsInstance(result.data["results"], list)
#         self.assertTrue(
#             all(result["Status"] in ["Yes", "No"] for result in result.data["results"])
#         )
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_online_customers_agent(self, mock_middleware):
#         result = self.live.online_customers_agent(self.request)
#         self.assertIsInstance(result.data, dict)
#         self.assertIsInstance(result.data["count"], int)
#         self.assertGreaterEqual(result.data["count"], 0)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_handoff_duration(self, mock_middleware):
#         result = self.live.handoff_duration(self.request)
#         actual_output = self.parse_json["ongoing_max_chats"]
#         self.assertEqual(result.data, actual_output)
#         self.assertIsInstance(result.data, dict)
#         self.assertTrue(
#             all(result["username"] is type(str) for result in result.data["results"])
#         )
#         self.assertTrue(
#             all(result["Duration"] is type(int) for result in result.data["results"])
#         )
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_last_activity_time(self, mock_middleware):
#         result = self.live.agent_last_activity_time(self.request)
#         self.assertEqual(result.status_code, 200)
#         self.assertIsInstance(result.data, dict)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_ended_chats(self, mock_middleware):
#         result = self.live.ended_chats(self.request)
#         self.assertIsInstance(result.data, QuerySet)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_skill(self, mock_middleware):
#         result = self.live.agent_skill(self.request)
#         for item in result.data["results"]:
#             item["Skills"] = list(item["Skills"])
#         actual_output = self.parse_json["agent_skill"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_ongoing_max_chats(self, mock_middleware):
#         result = self.live.ongoing_max_chats(self.request)
#         actual_output = self.parse_json["ongoing_max_chats"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_current_loggedin_skills(self, mock_middleware):
#         result = self.live.current_loggedin_skills(self.request)
#         self.assertIsInstance(result.data, QuerySet)
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_abandoned_users_details_live(self, mock_middleware):
#         result = self.live.abandoned_users_details_live(self.request)
#         self.assertEqual(result.data["results"], [])
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_arrived_live(self, mock_middleware):
#         result = self.live.interaction_arrived_live(self.request)
#         self.assertTrue(
#             all(
#                 result["Interactions Arrived"] is type(int)
#                 for result in result.data["results"]
#             )
#         )
#         self.assertTrue(
#             all(result["Agent"] is type(str) for result in result.data["results"])
#         )
#
#     @mock.patch(
#         "handoff.services.live_report_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_interaction_accepted_live(self, mock_middleware):
#         result = self.live.interaction_accepted_live(self.request)
#         self.assertTrue(
#             all(
#                 result["Interactions Accepted"] is type(int)
#                 for result in result.data["results"]
#             )
#         )
