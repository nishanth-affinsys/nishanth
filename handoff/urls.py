from django.urls import path, include

from .views import (
    agent_productivity_views,
    agent_reports_views,
    detail_report_views,
    agent_transfer_views,
    live_reports_views,
)

from rest_framework import routers

app_name = "handoff"

router = routers.DefaultRouter()
router.register(
    "agentreport-charts",
    agent_reports_views.AgentReportViewSet,
    basename="agentreport-charts",
)

router.register(
    "livereport-charts",
    live_reports_views.LiveDataViewSet,
    basename="livereport-charts",
)

router.register(
    "detailreport-charts",
    detail_report_views.DetailReportViewSet,
    basename="detailreport-charts",
)

router.register(
    "agent_productivity",
    agent_productivity_views.AgentProductivityViewSet,
    basename="agent_productivity",
)

router.register(
    "agent_transfer_charts",
    agent_transfer_views.AgentTransferViewSet,
    basename="agent_transfer_charts",
)

urlpatterns = [
    path("", include(router.urls)),
]
