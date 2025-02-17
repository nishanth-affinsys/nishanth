# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
# from handoff.views.agent_transfer_views import AgentTransferViewSet
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
#     data_list = list(data)
#     for item in data_list:
#         item["Date"] = str(item["Date"])
#     return data_list
#
#
# class TestAgentTransfer(APITestCase):
#     databases = {"handoff"}
#     fixtures = [
#         "tests/fixtures/analyticssocialevent.json",
#         "tests/fixtures/agenttransfer.json",
#         "tests/fixtures/socialconversationagent.json",
#         "tests/fixtures/socialconversationtempsocialuser.json",
#     ]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.bot = AgentTransferViewSet()
#         self.parse_json = parse_json(path)
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_transfer_initiated_bigNo(self, mock_middleware):
#         result = self.bot.total_transfer_initiated_bigno(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_successful_transfer_bigNo(self, mock_middleware):
#         result = self.bot.total_successful_transfer_bigno(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_total_failed_transfer_bigNo(self, mock_middleware):
#         result = self.bot.total_failed_transfer_bigno(self.request)
#         self.assertEqual(result.data, {"count": 1})
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfers_initiated_linechart(self, mock_middleware):
#         result = self.bot.transfers_initiated_linechart(self.request)
#         formatted_result = date_to_string(result.data)
#         actual_output = [{"Date": "2023-04-26", "transfers_initiated": 1}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfers_accepted_linechart(self, mock_middleware):
#         result = self.bot.transfers_accepted_linechart(self.request)
#         formatted_result = date_to_string(result.data)
#         actual_output = [{"Date": "2023-04-26", "transfers_accepted": 1}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfers_failed_linechart(self, mock_middleware):
#         result = self.bot.transfers_failed_linechart(self.request)
#         formatted_result = date_to_string(result.data)
#         actual_output = [{"Date": "2023-04-26", "transfers_failed": 1}]
#         self.assertEqual(formatted_result, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_agent_initiated_transfers(self, mock_middleware):
#         result = self.bot.agent_initiated_transfers(self.request)
#         actual_output = [{"Agent_Name": "Aswin", "count": 1}]
#         self.assertEqual(list(result.data), actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfer_details(self, mock_middleware):
#         result = self.bot.transfer_details(self.request)
#         for i in result.data["results"]:
#             i["Initialized_time"] = str(i["Initialized_time"])
#         actual_output = self.parse_json["transfer_details"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfer_details_export(self, mock_middleware):
#         result = self.bot.transfer_details_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=handoff_duration.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Username,Parent_Session_Id,Initial_Agent,Agents_Transferred,Channel,Initialized_time,Total_session_time"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_transfer_details_export_pdf(self, mock_middleware):
#         result = self.bot.transfer_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=handoff_duration.pdf",
#         )
#         self.assertTrue(result.content)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_only_transfer_details(self, mock_middleware):
#         result = self.bot.only_transfer_details(self.request)
#         for i in result.data["results"]:
#             i["Initialized_time"] = str(i["Initialized_time"])
#         actual_output = self.parse_json["only_transfer"]
#         self.assertEqual(result.data, actual_output)
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_only_transfer_details_export(self, mock_middleware):
#         result = self.bot.only_transfer_details_export(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=Agent_transfer_details.csv",
#         )
#         self.assertTrue(result.content)
#         self.assertTrue(
#             result.content.startswith(
#                 b"Username,Parent_Session_Id,Initial_Agent,Agents_Transferred,Channel,Initialized_time,Accept_time,Total_session_time"
#             )
#         )
#
#     @mock.patch(
#         "handoff.services.agent_transfer_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_only_transfer_details_export_pdf(self, mock_middleware):
#         result = self.bot.only_transfer_details_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "inline; filename=Agent_transfer_details.pdf",
#         )
#         self.assertTrue(result.content)
