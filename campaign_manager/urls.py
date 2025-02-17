from django.urls import path, include
from .views import (
    campaign_views,
    campaign_active_inactive_views,
    campaign_type,
    campaign_dynamic_views,
)
from rest_framework import routers


app_name = "campaign_manager"

router = routers.DefaultRouter()

router.register(
    "campaign-charts", campaign_views.CampaignViewSet, basename="campaign-charts"
)

router.register(
    "campaign_active_inactive",
    campaign_active_inactive_views.CampaignActiveInActiveViewSet,
    basename="campaign_active_inactive",
)

router.register(
    "campaign_type", campaign_type.CamapignTypeViewSet, basename="campaign_type"
)

router.register(
    "campaign_dynamic_dashboard",
    campaign_dynamic_views.CampaignDynamicDashboardViewSet,
    basename="campaign_dynamic_dashboard",
)

urlpatterns = [path("", include(router.urls))]
