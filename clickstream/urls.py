from django.urls import path, include
from .views import (
    ip_info,
    device_info,
    clickstream_data,
    clickstream_ETB_views,
    clickstream_NTB_views,
)
from rest_framework import routers

app_name = "clickstream"

router = routers.DefaultRouter()
# router.register("ipinfo-charts", ip_info.IpInfoViewSet, basename="ipinfo-charts")
#
# router.register(
#     "deviceinfo-charts", device_info.DeviceInfoViewSet, basename="deviceinfo-charts"
# )
# router.register(
#     "clickstreamdata-charts",
#     clickstream_data.ClickStreamDataViewSet,
#     basename="clickstreamdata-charts",
# )
# router.register(
#     "clickstream_ETB", clickstream_ETB_views.ETBViewSet, basename="clickstream_ETB"
# )
# router.register(
#     "clickstream_NTB",
#     clickstream_NTB_views.NTBviewSet,
#     basename="clickstream_NTB",
# )
urlpatterns = [
    path("", include(router.urls)),
]
