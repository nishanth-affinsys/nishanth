from django.urls import path, include
from .views import (
    live_transactions_views,
    nbf_lead_generator_views,
    dib_session,
    digibankr,
    kina,
    dib,
    dib_leads,
)

from rest_framework import routers

app_name = "client_specific"
router = routers.DefaultRouter()

router.register(
    "live_transaction",
    live_transactions_views.LiveTransactionViewSet,
    basename="live_transaction",
)
# router.register(
#     "dib-session",
#     dib_session.SessionViewSet,
#     basename="dib-session",
# )

router.register(
    "stock_management",
    digibankr.StockManagementViewSet,
    basename="stock_management",
)

router.register(
    "card_management",
    digibankr.CardManagementViewSet,
    basename="card_management",
)

router.register(
    "onboarding_audit_report",
    kina.OnboardingAuditViewSet,
    basename="onboarding_audit_report",
)

router.register(
    "subscription_dashboard",
    dib.SubscriptionDashboardViewSet,
    basename="subscription_dashboard",
)

router.register(
    "leads_dashboard",
    dib_leads.DIBLeadsDashboard,
    basename="leads_dashboard",
)

urlpatterns = [
    path("", include(router.urls)),
]
