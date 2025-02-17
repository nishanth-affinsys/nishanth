from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from console.services.kinaxchange_transaction_utils import (
    wallet_transactions_bigno,
    wallet_transactions_multilinechart_generic,
    wallet_transactions_details,
    wallet_transactions_percentage,
)
from main.utils.boiler_plate import get_generic_response


class KINATransactionViewSet(GenericViewSet):  # for Transaction Report
    # Total Successful Transactions
    @extend_schema(
        operation_id="wallet_successful_transaction",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_successful_transaction")
    def wallet_successful_transaction(self, request, *args, **kwargs):
        params = wallet_transactions_bigno(request, "S")
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_successful_transaction_percentage",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_successful_transaction_percentage",
    )
    def wallet_successful_transaction_percentage(self, request, *args, **kwargs):
        response = wallet_transactions_percentage(request, "S")
        return Response(response)

    @extend_schema(
        operation_id="wallet_failed_transaction",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_failed_transaction")
    def wallet_failed_transaction(self, request, *args, **kwargs):
        params = wallet_transactions_bigno(request, "F")
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_failed_transaction_percentage",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_failed_transaction_percentage"
    )
    def wallet_failed_transaction_percentage(self, request, *args, **kwargs):
        response = wallet_transactions_percentage(request, "F")
        return Response(response)

    @extend_schema(
        operation_id="wallet_aggregate_transactions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_aggregate_transactions")
    def wallet_aggregate_transactions(self, request, *args, **kwargs):
        params = wallet_transactions_multilinechart_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="wallet_successful_transaction_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_successful_transaction_details"
    )
    def wallet_successful_transaction_details(self, request, *args, **kwargs):
        params = wallet_transactions_details(request, "S")
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_successful_transaction_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_successful_transaction_details_export_csv",
    )
    def wallet_successful_transaction_details_export_csv(
        self, request, *args, **kwargs
    ):
        params = wallet_transactions_details(
            request,
            "S",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Transaction_id",
                    "Currency",
                    "Amount",
                    "Sender",
                    "Receiver",
                    "Timestamp",
                ],
                "fileName": "successful_transactions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_successful_transaction_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_successful_transaction_details_export_pdf",
    )
    def wallet_successful_transaction_details_export_pdf(
        self, request, *args, **kwargs
    ):
        params = wallet_transactions_details(
            request,
            "S",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Transaction_id",
                    "Currency",
                    "Amount",
                    "Sender",
                    "Receiver",
                    "Timestamp",
                ],
                "fileName": "successful_transactions.pdf",
                "title": "Successful Transactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_failed_transaction_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total failed Transactions",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_failed_transaction_details"
    )
    def wallet_failed_transaction_details(self, request, *args, **kwargs):
        params = wallet_transactions_details(request, "F")
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_failed_transaction_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_failed_transaction_details_export_csv",
    )
    def wallet_failed_transaction_details_export_csv(self, request, *args, **kwargs):
        params = wallet_transactions_details(
            request,
            "F",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Transaction_id",
                    "Currency",
                    "Amount",
                    "Sender",
                    "Receiver",
                    "Timestamp",
                ],
                "fileName": "failed_transactions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="wallet_failed_transaction_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="wallet_failed_transaction_details_export_pdf",
    )
    def wallet_failed_transaction_details_export_pdf(self, request, *args, **kwargs):
        params = wallet_transactions_details(
            request,
            "F",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Transaction_id",
                    "Currency",
                    "Amount",
                    "Sender",
                    "Receiver",
                    "Timestamp",
                ],
                "fileName": "failed_transactions.pdf",
                "title": "Failed Transactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
