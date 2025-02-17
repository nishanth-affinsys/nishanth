from __future__ import annotations

from auth.tags import AuthTags
from auth.user_types import UserType
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from wallet.services.admin_transaction_logs_utils import (
    wallet_admin_transaction_logs_generic,
    wallet_admin_reconciliation_report,
)
from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf, export_excel


class AdminTransactionLogsViewSet(GenericViewSet):
    @extend_schema(
        operation_id="wallet_admin_transaction_logs",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of transaction logs",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_admin_transaction_logs")
    def wallet_admin_transaction_logs(self, request, *args, **kwargs):
        items, _, _ = wallet_admin_transaction_logs_generic(request)
        items = return_table(items, request)
        return items

    @extend_schema(
        operation_id="wallet_admin_transaction_logs_export_csv",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of transaction logs",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_transaction_logs_export_csv",
    )
    def wallet_admin_transaction_logs_export_csv(self, request, *args, **kwargs):
        items, fieldNames, fileName = wallet_admin_transaction_logs_generic(request)
        items = export_csv(items, fieldNames, f"{fileName}.csv")
        return items

    # @extend_schema(
    #     operation_id="wallet_admin_transaction_logs_export_pdf",
    #     tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
    #     description="Used for displaying the data of transaction logs",
    # )
    # @action(methods=["POST"], detail=False, url_path="wallet_admin_transaction_logs_export_pdf")
    # def wallet_admin_transaction_logs_export_pdf(self, request, *args, **kwargs):
    #     items, fieldNames, fileName = wallet_admin_transaction_logs_generic(request)
    #     items = export_pdf(items, fieldNames, f"{fileName}.pdf", "Transaction Logs Report", request.user.username)
    #     return items

    @extend_schema(
        operation_id="wallet_admin_transaction_logs_export_excel",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of transaction logs",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_transaction_logs_export_excel",
    )
    def wallet_admin_transaction_logs_export_excel(self, request, *args, **kwargs):
        items, fieldNames, fileName = wallet_admin_transaction_logs_generic(request)
        items = export_excel(items, ["Timestamp"], f"{fileName}.xlsx")
        return items


class AdminReconciliationReportViewSet(GenericViewSet):
    @extend_schema(
        operation_id="wallet_admin_reconciliation_report_details",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of reconciliation report",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_reconciliation_report_details",
    )
    def wallet_admin_reconciliation_report(self, request, *args, **kwargs):
        items, _, _ = wallet_admin_reconciliation_report(request)
        items = return_table(items, request)
        return items

    @extend_schema(
        operation_id="wallet_admin_reconciliation_report_export_csv",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of reconciliation report csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_reconciliation_report_export_csv",
    )
    def wallet_admin_reconciliation_report_export_csv(self, request, *args, **kwargs):
        items, fieldNames, fileName = wallet_admin_reconciliation_report(request)
        items = export_csv(items, fieldNames, f"{fileName}.csv")
        return items

    @extend_schema(
        operation_id="wallet_admin_reconciliation_report_export_pdf",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of reconciliation report pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_reconciliation_report_export_pdf",
    )
    def wallet_admin_reconciliation_report_export_pdf(self, request, *args, **kwargs):
        items, fieldNames, fileName = wallet_admin_reconciliation_report(request)
        items = export_pdf(
            items,
            fieldNames,
            f"{fileName}.pdf",
            "Reconciliation Report",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="wallet_admin_reconciliation_report_export_excel",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the data of reconciliation report excel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_admin_reconciliation_report_export_excel",
    )
    def wallet_admin_reconciliation_report_export_excel(self, request, *args, **kwargs):
        items, fieldNames, fileName = wallet_admin_reconciliation_report(request)
        items = export_excel(items, ["transaction_timestamp"], f"{fileName}.xlsx")
        return items
