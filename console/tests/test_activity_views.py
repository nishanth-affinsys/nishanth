import json

# from rest_framework.test import APITestCase, APIRequestFactory
# from console.views.activity_views import ActivityViewSet
# from unittest import mock
#
# from main.settings import BASE_DIR
#
#
def get_current_tenant_name():
    return "prathamtest"

#
# path = f"{BASE_DIR}/tests/responses/view_user_activity_responses.json"
#

def parse_json(response_path):
    with open(response_path, "r") as f:
        json_body = json.load(f)
    return json_body


def date_to_string(data, keys):
    for item in data["results"]:
        for key in keys:
            item[key] = str(item[key])
    return data
#
#
# class TestActivityViews(APITestCase):
#     databases = {"analytics"}
#     fixtures = ["tests/fixtures/activity.json"]
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.post("analytics-new/reports/")
#         self.request.data = {
#             "timestamp__range": ["2001-01-01T00:00:00Z", "2023-06-30T00:00:00Z"],
#             "channel": ["webchat"],
#         }
#         self.activity = ActivityViewSet()
#         self.parse_json = parse_json(path)
#
#     @mock.patch(
#         "console.services.activity_utils.get_current_tenant_name",
#         side_effect=get_current_tenant_name,
#     )
#     def test_complete_activity_details(self, mock_middleware):
#         result = self.activity.complete_activity_details(self.request)
#         formatted_result = date_to_string(
#             result.data, ["request_timestamp", "timestamp"]
#         )
#         actual_output = self.parse_json["activity"]
#         self.assertEqual(formatted_result, actual_output)
