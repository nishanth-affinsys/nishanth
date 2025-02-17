# import json
#
# from rest_framework.test import APITestCase, APIRequestFactory
#
# from console.tests.test_user_behaviour import date_to_string
# from console.views.service_status_views import ServiceStatusViewSet
#
#
# def parse_json(response_path):
#     with open(response_path, "r") as f:
#         json_body = json.load(f)
#     return json_body
#
#
# class TestServiceStatus(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["console/tests/fixtures/servicestatus.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2011-11-01T00:00:00Z", "2023-12-30T00:00:00Z"]
#         }
#         self.serv = ServiceStatusViewSet()
#         self.pdf_content = "application/pdf"
#         self.csv_content = "text/csv"
#
#     def test_service_status(self):
#         result = self.serv.service_status(self.request)
#         formatted_result = date_to_string(result.data, "Timestamp")
#         actual_output = {
#             "count": 8,
#             "next": None,
#             "previous": None,
#             "results": [
#                 {
#                     "Service": "Agent Provider",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-22 08:56:52+00:00",
#                 },
#                 {
#                     "Service": "Bot",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-21 09:52:07+00:00",
#                 },
#                 {
#                     "Service": "Bot Builder",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-22 08:56:47+00:00",
#                 },
#                 {
#                     "Service": "Charges",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-22 08:56:53+00:00",
#                 },
#                 {
#                     "Service": "EventLogger",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-22 08:56:47+00:00",
#                 },
#                 {
#                     "Service": "Notification",
#                     "Health_Status": "200",
#                     "Live_Status": "200",
#                     "Timestamp": "2023-11-22 08:56:49+00:00",
#                 },
#                 {
#                     "Service": "OTP",
#                     "Health_Status": "-1",
#                     "Live_Status": "-1",
#                     "Timestamp": "2023-11-22 08:56:53+00:00",
#                 },
#                 {
#                     "Service": "QR - SVC",
#                     "Health_Status": "-1",
#                     "Live_Status": "-1",
#                     "Timestamp": "2023-11-22 08:56:52+00:00",
#                 },
#             ],
#         }
#         self.assertEqual(formatted_result, actual_output)
#
#     def test_service_status_export_csv(self):
#         result = self.serv.service_status_export_csv(self.request)
#         self.assertEqual(result.get("Content-Type"), self.csv_content)
#         self.assertEqual(
#             result.get("Content-Disposition"),
#             "attachment; filename=service_status.csv",
#         )
#
#     def test_service_status_export_pdf_limit(self):
#         with self.settings(MAX_PDF_LIMIT=0):
#             result = self.serv.service_status_export_pdf(self.request)
#
#             self.assertEqual(result.get("Content-Type"), self.pdf_content)
#             self.assertEqual(
#                 result.get("Content-Disposition"), "inline; filename=service_status.pdf"
#             )
#
#     def test_service_status_export_pdf(self):
#         result = self.serv.service_status_export_pdf(self.request)
#         self.assertEqual(result.get("Content-Type"), self.pdf_content)
#         self.assertEqual(
#             result.get("Content-Disposition"), "inline; filename=service_status.pdf"
#         )
