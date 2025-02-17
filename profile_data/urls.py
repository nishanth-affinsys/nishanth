from django.urls import path, include
from .views import profile_analytics_views, profile_interactions_views
from rest_framework import routers


app_name = "profile_data"

router = routers.DefaultRouter()

router.register(
    "profile_data",
    profile_analytics_views.ProfileDataViewSet,
    basename="profile_data",
)

router.register(
    "profile_interactions",
    profile_interactions_views.ProfileInteractionsViewSet,
    basename="profile_interactions",
)

urlpatterns = [
    path("", include(router.urls)),
]
