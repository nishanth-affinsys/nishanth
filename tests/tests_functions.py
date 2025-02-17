# from django.apps import apps
# from django.db.models import QuerySet, Count
# from rest_framework.test import APIRequestFactory, APITestCase
#
# from console.models import MessageLog
# from console.serializers import BotReportSerializer
# from main.utils.boiler_plate import query, get_generic_response
#
# app_models = apps.get_app_config("console").get_models()
#
#
# class FunctionTest(APITestCase):
#     fixtures = ["tests/fixtures/messagelog.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#
#     def test_query(self):
#         request = self.factory.post("analytics-new/reports/bot-charts/handled-msg")
#         request.data = {
#             "timestamp__range": ["2023-01-01 00:00:00", "2023-06-30 00:00:00"],
#             "channel": ["webchat"],
#         }
#         response = query(request, MessageLog, BotReportSerializer)
#         self.assertEqual(type(response), QuerySet)
#
#     def test_query_data(self):
#         request = self.factory.post("analytics-new/reports/bot-charts/handled-msg")
#         request.data = {
#             "timestamp__range": ["2023-01-01 00:00:00", "2023-06-30 00:00:00"],
#             "channel": ["webchat"],
#         }
#         params = {
#             "request": request,
#             "models": MessageLog,
#             "serializers": BotReportSerializer,
#             "db_schema": "default",
#             "filter_kwargs": {"handled": "Y", "source": "user", "tenant": "lebacpsix"},
#             "values": ["channel"],
#             "annotate": {"count": Count("intent")},
#             "order_by": ["-count"],
#         }
#         response = get_generic_response(params)
#         self.assertEqual(
#             response.data,
#             {
#                 "count": 1,
#                 "next": None,
#                 "previous": None,
#                 "results": [{"channel": "webchat", "count": 5}],
#             },
#         )
#
#     def test_get_generic_response_qs(self):
#         request = self.factory.post("analytics-new/reports/bot-charts/messages-faq")
#         request.data = {
#             "timestamp__range": ["2023-01-01 00:00:00", "2023-06-30 00:00:00"],
#             "channel": ["webchat"],
#         }
#         params = {
#             "request": request,
#             "models": MessageLog,
#             "serializers": BotReportSerializer,
#             "db_schema": "default",
#             "filter_kwargs": {
#                 "source": "user",
#                 "tenant": "lebacpsix",
#                 "message__isnull": False,
#             },
#             "values": ["channel"],
#             "annotate": {"Count": Count("message")},
#             "order_by": ["-Count"],
#         }
#         response = get_generic_response(params)
#         self.assertEqual(
#             response.data,
#             {
#                 "count": 1,
#                 "next": None,
#                 "previous": None,
#                 "results": [{"channel": "webchat", "Count": 4}],
#             },
#         )
