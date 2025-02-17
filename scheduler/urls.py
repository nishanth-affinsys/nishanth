from django.urls import path, include

from rest_framework import routers
from scheduler.views import SchedulerViewSet

router = routers.DefaultRouter()

router.register(
    "webhooks",
    SchedulerViewSet,
    basename="webhooks",
)

urlpatterns = [
    path("", include(router.urls)),
]
