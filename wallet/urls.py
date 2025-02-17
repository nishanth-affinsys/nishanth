from django.urls import path, include
from rest_framework import routers

from .views import (
    customer_analytics_views,
    merchant_qr_views,
    merchant_transaction_views,
    merchant_profit_views,
    admin_transaction_status_views,
    admin_transaction_logs_views,
)

app_name = "wallet"

router = routers.DefaultRouter()
router.register(
    "wallet_customer",
    customer_analytics_views.CustomerWalletAnalyticsViewSet,
    basename="wallet_customer",
)
router.register(
    "wallet_merchant_qr",
    merchant_qr_views.MerchantQRWalletViewSet,
    basename="wallet_merchant_qr",
)
router.register(
    "wallet_merchant_transactions",
    merchant_transaction_views.MerchantTransactionWalletViewSet,
    basename="wallet_merchant_transactions",
)

router.register(
    "wallet_merchant_profit",
    merchant_profit_views.MerchantProfitWalletViewSet,
    basename="wallet_merchant_profit",
)

router.register(
    "wallet_admin_transactions_status",
    admin_transaction_status_views.AdminTransactionStatusViewSet,
    "wallet_admin_transactions_status",
)

router.register(
    "wallet_admin_transactions_logs",
    admin_transaction_logs_views.AdminTransactionLogsViewSet,
    "wallet_admin_transactions_logs",
)

router.register(
    "wallet_admin_reconciliation_report",
    admin_transaction_logs_views.AdminReconciliationReportViewSet,
    "wallet_admin_reconciliation_report",
)

urlpatterns = [
    path("", include(router.urls)),
]
