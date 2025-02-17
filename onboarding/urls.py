from django.urls import path, include
from .views import (
    onboarding_stage_reports_views,
    onboarding_detailed_report_views,
    onboarding_transaction_report_views,
    onboarding_ageing_report_views,
    onboarding_trend_report_views,
    kyc_ageing_report_views,
    kyc_transactions_report_views,
    kyc_detailed_report_views,
    kyc_stage_report_views,
)
from rest_framework import routers


app_name = "onboarding"

router = routers.DefaultRouter()
router.register(
    "onboarding_stagereport_charts",
    onboarding_stage_reports_views.StageReportViewSet,
    basename="onboarding_stagereport_charts",
)
router.register(
    "onboarding_detailed_charts",
    onboarding_detailed_report_views.DetailedReportViewSet,
    basename="onboarding_detailed_charts",
)
router.register(
    "onboarding_transaction_charts",
    onboarding_transaction_report_views.TransactionReportViewSet,
    basename="onboarding_transaction_charts",
)
router.register(
    "onboarding_ageing_charts",
    onboarding_ageing_report_views.AgeingReportViewSet,
    basename="onboarding_ageing_charts",
)
router.register(
    "onboarding_trend_charts",
    onboarding_trend_report_views.TrendReportViewSet,
    basename="onboarding_trend_charts",
)


router.register(
    "kyc_stagereport_charts",
    kyc_stage_report_views.KYCStageReportViewSet,
    basename="kyc_stagereport_charts",
)
router.register(
    "kyc_detailed_charts",
    kyc_detailed_report_views.KYCDetailedReport,
    basename="kyc_detailed_charts",
)
router.register(
    "kyc_transaction_charts",
    kyc_transactions_report_views.KYCTransactionReportViewSet,
    basename="kyc_transaction_charts",
)
router.register(
    "kyc_ageing_charts",
    kyc_ageing_report_views.KYCAgeingReportViewSet,
    basename="kyc_ageing_charts",
)

urlpatterns = [path("", include(router.urls))]
