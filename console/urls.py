from django.urls import path, include
from .views import (
    bot_reports_views,
    api_logs_views,
    daily_traffic_views,
    dashboards_views,
    user_behaviours_views,
    transactions_reports_views,
    reports_views,
    reg_deregistration,
    activity_views,
    llm_reports_views,
    service_status_views,
    kinaechange_transaction_views,
    kinaechange_signups_views,
)

from rest_framework import routers

app_name = "console"

router = routers.DefaultRouter()
router.register("bot-charts", bot_reports_views.BotChartsViewSet, basename="bot-charts")

router.register(
    "transaction-charts",
    transactions_reports_views.TransactionChartsViewSet,
    basename="transaction-charts",
)
router.register(
    "api-charts", api_logs_views.ApiLogsChartsViewSet, basename="api-charts"
)
router.register(
    "dailytraffic-charts",
    daily_traffic_views.DailyTrafficViewSet,
    basename="dailytraffic-charts",
)
router.register(
    "userbehaviour-charts",
    user_behaviours_views.UserBehaviourChartsViewSet,
    basename="userbehaviour-charts",
)
router.register(
    "reportglance-charts",
    reports_views.ReportsAtGlanceViewSet,
    basename="reportglance-charts",
)
router.register(
    "registration", reg_deregistration.RegDeregViewSet, basename="registration"
)
router.register("activity", activity_views.ActivityViewSet, basename="activity")

router.register(
    "llm-reports", llm_reports_views.LLMReportsViewSet, basename="llm-reports"
)

router.register(
    "service-status-reports",
    service_status_views.ServiceStatusViewSet,
    basename="service-status-reports",
)

# for kina exchange app
router.register(
    "wallet-transactions",
    kinaechange_transaction_views.KINATransactionViewSet,
    basename="wallet-transactions",
)

router.register(
    "user-signups",
    kinaechange_signups_views.KINASignupsViewSet,
    basename="user-signups",
)

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/live_transaction", dashboards_views.live_transaction),
    path("dashboard/<chartid>", dashboards_views.dashboard),
    path("get_channels/", dashboards_views.channels),
    path("get_campaigns/", dashboards_views.campaign_names),
    # path("endpoints/", dashboards_views.endpoints),
    path("get_dashboard_details/", dashboards_views.get_dashboard_name),
    path("check_changes/", dashboards_views.handle_request),
    path("get_intents/", dashboards_views.get_intents),
    path("get_customer_types/", dashboards_views.get_customer_types),
    path("get_timezones/", dashboards_views.get_timezones),
]
