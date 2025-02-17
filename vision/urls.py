from django.urls import path, include
from .views import vision_ocr_views, vision_face_views, vision_forgery_views

from rest_framework import routers


app_name = "vision"


router = routers.DefaultRouter()

router.register("ocr-charts", vision_ocr_views.VisionOCRViewSet, basename="ocr-charts")

router.register(
    "face-charts", vision_face_views.VisionFaceViewSet, basename="face-charts"
)

router.register(
    "forgery-charts",
    vision_forgery_views.VisionForgeryViewSet,
    basename="forgery-charts",
)

urlpatterns = [
    path("", include(router.urls)),
]
