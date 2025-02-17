import json

from rest_framework.test import APITestCase, APIRequestFactory
from console.views.user_behaviours_views import UserBehaviourChartsViewSet
from unittest import mock
from django.db import connections
from main.settings import BASE_DIR
from main.utils.dynamic_db import dynamic_db_connection


def mock_get_db_name(*args):
    return "analytics"


def mock_dynamic_db(*args):
    return ""
            # dynamic_db_connection("analytics", "prathamtest")


path = f"{BASE_DIR}/tests/responses/user_behaviour_responses.json"


def parse_json(response_path):
    with open(response_path, "r") as f:
        json_body = json.load(f)
    return json_body


def date_to_string(data, key):
    for item in data["results"]:
        item[key] = str(item[key])
    return data


class TestUserBehaviourLogs(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Close all database connections explicitly
        for connection in connections.all():
            connection.close()

    databases = {"analytics"}
    fixtures = ["tests/fixtures/messagelog.json"]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.post("analytics-new/reports/")
        self.request.data = {
            "timestamp__range": ["2023-01-01T00:00:00Z", "2023-12-20T00:00:00Z"],
            "channel": ["webchat", "messenger"],
        }
        self.user_behaviour = UserBehaviourChartsViewSet()
        self.parse_json = parse_json(path)
        self.pdf_content = "application/pdf"
        self.csv_content = "text/csv"

    @mock.patch(
        "console.services.user_behaviour_utils.dynamic_db_connection",
        side_effect=mock_dynamic_db,
    )
    @mock.patch(
        "console.services.user_behaviour_utils.get_db_name",
        side_effect=mock_get_db_name,
    )
    def test_top_10_message(self, mock_get_db_name, mock_dynamic_db):
        result = self.user_behaviour.top_10_message(self.request)
        actual_output = self.parse_json["top_10_message"]
        self.assertEqual(result.data, actual_output)
