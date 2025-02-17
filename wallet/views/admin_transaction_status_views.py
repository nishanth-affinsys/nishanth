from __future__ import annotations
from __future__ import annotations

from auth.tags import AuthTags
from auth.user_types import UserType
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from wallet.services.admin_transaction_status_utils import (
    wallet_mw_generic,
)


class AdminTransactionStatusViewSet(GenericViewSet):

    @extend_schema(
        operation_id="wallet_mw_transactions_initiated",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total number of transactions initiated",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_mw_transactions_initiated")
    def wallet_mw_transactions_initiated(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["S", "P", "I", "F", "R", "C", "M", "A"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_transactions_not_submitted",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total number of transactions where weren't submitted",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_mw_transactions_not_submitted"
    )
    def wallet_mw_transactions_not_submitted(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["I", "P"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_submitted_unprocessed",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of transactions which were submitted but aren't processed",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_mw_submitted_unprocessed")
    def wallet_mw_submitted_unprocessed(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["A"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_processed_successfully",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of transactions which were processed successfully",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_mw_processed_successfully")
    def wallet_mw_processed_successfully(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["S"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_processed_failed",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of transactions which were processed but failed",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_mw_processed_failed")
    def wallet_mw_processed_failed(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["F"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_processed_reversed",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of reversed transactions",
    )
    @action(methods=["POST"], detail=False, url_path="wallet_mw_processed_reversed")
    def wallet_mw_processed_reversed(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, "R")
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_processed_status_unknown",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of processed transactions but current status is not known",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_mw_processed_status_unknown"
    )
    def wallet_mw_processed_status_unknown(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["F"])
        return Response(data={"count": response})

    @extend_schema(
        operation_id="wallet_mw_require_manual_statement",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total no of transactions which require manual statement",
    )
    @action(
        methods=["POST"], detail=False, url_path="wallet_mw_require_manual_statement"
    )
    def wallet_mw_require_manual_statement(self, request, *args, **kwargs):
        response = wallet_mw_generic(request, ["M"])
        return Response(data={"count": response})
