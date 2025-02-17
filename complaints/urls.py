from django.urls import path, include
from .views import complaint_views
from rest_framework import routers


app_name = "complaints"

router = routers.DefaultRouter()

router.register(
    "complaint_management",
    complaint_views.ComplaintManagementViewSet,
    basename="complaint_management",
)

urlpatterns = [
    path("", include(router.urls)),
]
