import json

from locust import HttpUser, task, between
from settings import BASE_DIR
from gevent.pool import Pool


class AnalyticsUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.tenant = "lebacpsix"
        self.body = {
            "timestamp__range": ["2001-01-01T00:00:00", "2023-08-03T00:00:00"],
            "channel": [
                "messenger",
                "instagram",
                "webchat",
                "line",
                "telegram",
                "twitter",
                "viber",
                "smst",
                "email",
                "whatsapp",
                "whatsappc",
                "whatsappi",
                "whatsapps",
                "whatsappk",
                "whatsapprcm",
                "whatsappt",
            ],
            "campaign_variants": [1, 2, 3, 4, 5, 6],
        }

        def parse_json(path):
            with open(path, "r") as f:
                json_body = json.load(f)
            return json_body

        self.endpoints = parse_json(f"{BASE_DIR}/main/endpoints.json")

    def concurrent_request(self, url, request_type):
        if request_type == "post":
            return self.client.post(
                url,
                json=self.body,
                cookies={"tenant": self.tenant},
            )
        else:
            return self.client.get(url, cookies={"tenant": self.tenant})

    @task
    def bot_report_requests(self):
        endpoints = self.endpoints["bot_report"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def agent_report_request(self):
        endpoints = self.endpoints["agent_report"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def api_analysis_request(self):
        endpoints = self.endpoints["api_analysis"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def detailed_report_request(self):
        endpoints = self.endpoints["detailed_report"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def queue_report_request(self):
        endpoints = self.endpoints["queue_report"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def daily_traffic_request(self):
        endpoints = self.endpoints["daily_traffic"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def transaction_status_request(self):
        endpoints = self.endpoints["transaction_status"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def reports_request(self):
        endpoints = self.endpoints["reports"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def user_behaviour_request(self):
        endpoints = self.endpoints["user_behaviour"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def live_data_request(self):
        endpoints = self.endpoints["live_data"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def visitors_data_request(self):
        endpoints = self.endpoints["visitors_data"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def campaign_details_request(self):
        endpoints = self.endpoints["campaign_details"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def clickstream_etb_request(self):
        endpoints = self.endpoints["clickstream_etb"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def clickstream_ntb_request(self):
        endpoints = self.endpoints["clickstream_ntb"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def lead_generator_request(self):
        endpoints = self.endpoints["lead_generator"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def campaign_status_request(self):
        endpoints = self.endpoints["campaign_status"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def campaign_types_request(self):
        endpoints = self.endpoints["campaign_types"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def campaign_summary_request(self):
        endpoints = self.endpoints["campaign_summary"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    @task
    def agent_transfer_request(self):
        endpoints = self.endpoints["agent_transfer"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()

    # @task
    # def onboarding_ageing_reports_rt_request(self):
    #     endpoints = self.endpoints["onboarding_ageing_reports_rt"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_ageing_reports_sp_request(self):
    #     endpoints = self.endpoints["onboarding_ageing_reports_sp"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_transaction_reports_rt_request(self):
    #     endpoints = self.endpoints["onboarding_transaction_reports_rt"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_transaction_reports_sp_request(self):
    #     endpoints = self.endpoints["onboarding_transaction_reports_sp"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_detailed_reports_rt_request(self):
    #     endpoints = self.endpoints["onboarding_detailed_reports_rt"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_detailed_reports_sp_request(self):
    #     endpoints = self.endpoints["onboarding_detailed_reports_sp"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_retailstage_reports_request(self):
    #     endpoints = self.endpoints["onboarding_retailstage_reports"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def onboarding_spstage_reports_request(self):
    #     endpoints = self.endpoints["onboarding_spstage_reports"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def trend_analysis_rt_request(self):
    #     endpoints = self.endpoints["trend_analysis_rt"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()
    #
    # @task
    # def trend_analysis_sp_request(self):
    #     endpoints = self.endpoints["trend_analysis_sp"]
    #     pool = Pool()
    #     pool.spawn(self.concurrent_request, endpoints[0], "get")
    #     for url in endpoints[1:]:
    #         pool.spawn(self.concurrent_request, url, "post")
    #     pool.join()

    @task
    def complaint_management_request(self):
        endpoints = self.endpoints["complaint_management"]
        pool = Pool()
        pool.spawn(self.concurrent_request, endpoints[0], "get")
        for url in endpoints[1:]:
            pool.spawn(self.concurrent_request, url, "post")
        pool.join()
