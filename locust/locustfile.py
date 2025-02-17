from gevent.pool import Pool
from locust import HttpUser, task, between


class AnalyticsUser(HttpUser):

    def on_start(self):
        self.tenant = "prathamtest"
        self.body = {
            "timestamp__range": [
                "2000-05-23T00:00:00+05:30",
                "2025-05-24T00:00:00+05:30"
            ],
            "channel": [
                "webchat"
            ]
        }

    def concurrent_request(self, url, request_type):
        if request_type == "post":
            return self.client.post(
                url,
                json=self.body,
                cookies={"tenant": self.tenant},
            )
        else:
            return self.client.get(url, cookies={"tenant": self.tenant})

    @task()
    def report_request(self):
        pool = Pool()
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_average_session_time/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_avg_msgs_per_session/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_new_user/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_returning_user/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_conversations/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_user_flow_sankey_chart/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_top_ten_matched_intents_by_channel/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_no_of_user_sessions/", "post")
        pool.join()

    @task(10)
    def report_response(self):
        pool = Pool()
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_no_of_msgs_coming_to_bot/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_total_messages_by_session/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_top_matched_intents/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_top_messages/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_total_matched_intents/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_total_unmatched_intents/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_active_customers/", "post")
        pool.spawn(self.concurrent_request, "/analytics-new/reports/bot-charts/bot_daily_user_messages_heatmap/", "post")
        pool.join()
