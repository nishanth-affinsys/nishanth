from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from main.health import get_liveness, get_healthz

API_PREFIX = "analytics-new/reports/"

urlpatterns = [
    path(
        API_PREFIX + "openapi/",
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "schema/swagger-ui/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "schema/redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
            ]
        ),
    ),
    path(API_PREFIX + "openapi/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path(API_PREFIX, include('reports.urls')),
    path(API_PREFIX, include("handoff.urls")),
    path(API_PREFIX, include("onboarding.urls")),
    path(API_PREFIX, include("console.urls")),
    path(API_PREFIX, include("campaign_manager.urls")),
    path(API_PREFIX, include("clickstream.urls")),
    path(API_PREFIX, include("client_specific.urls")),
    path(API_PREFIX, include("complaints.urls")),
    path(API_PREFIX, include("vision.urls")),
    path(API_PREFIX, include("wallet.urls")),
    path(API_PREFIX, include("profile_data.urls")),
    path(API_PREFIX, include("scheduler.urls")),  # + "webhooks/schedule-complete/"
    path(API_PREFIX + "vcs/", include("metadata.urls")),
    path(API_PREFIX + "conf/", include("conf.urls")),
    path("livez/", get_liveness),
    path("healthz/", get_healthz),
]
