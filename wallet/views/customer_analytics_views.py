from __future__ import annotations
from __future__ import annotations

from auth.tags import AuthTags
from auth.user_types import UserType
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from wallet.services.customer_analytics_utils import (
    total_money_sent_cust,
    total_money_received_cust,
    transaction_status_linechart_cust,
    income_vs_expenses_cust,
    spent_received_qr_payments_cust,
    money_spent_categories,
)


class CustomerWalletAnalyticsViewSet(GenericViewSet):
    def logged_user_id(self, request):
        return request.user.user_id

    def user_provider(self, request):
        return request.user.provider

    # Total money sent by customer
    @extend_schema(
        operation_id="total_money_sent_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total money sent by the customer",
    )
    @action(methods=["POST"], detail=False, url_path="total_money_sent_cust")
    def total_money_sent_cust(self, request, *args, **kwargs):
        response = total_money_sent_cust(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(data={"count": response})

    @extend_schema(
        operation_id="total_money_received_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total money received by the customer",
    )
    @action(methods=["POST"], detail=False, url_path="total_money_received_cust")
    def total_money_received_cust(self, request, *args, **kwargs):
        response = total_money_received_cust(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(data={"count": response})

    @extend_schema(
        operation_id="transaction_status_linechart_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the different status of transaction like success, failed, etc",
    )
    @action(
        methods=["POST"], detail=False, url_path="transaction_status_linechart_cust"
    )
    def transaction_status_linechart_cust(self, request, *args, **kwargs):
        qs1 = transaction_status_linechart_cust(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(qs1)

    @extend_schema(
        operation_id="income_vs_expenses_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the expenses vs income",
    )
    @action(methods=["POST"], detail=False, url_path="income_vs_expenses_cust")
    def income_vs_expenses_cust(self, request, *args, **kwargs):
        result = income_vs_expenses_cust(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(result)

    @extend_schema(
        operation_id="spent_received_qr_payments_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the spent and received",
    )
    @action(methods=["POST"], detail=False, url_path="spent_received_qr_payments_cust")
    def spent_received_qr_payments_cust(self, request, *args, **kwargs):
        payload = spent_received_qr_payments_cust(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(payload)

    @extend_schema(
        operation_id="money_spent_categories_cust",
        tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
        description="Used for displaying the total money spent by the customer on different categories",
    )
    @action(methods=["POST"], detail=False, url_path="money_spent_categories_cust")
    def money_spent_categories_cust(self, request, *args, **kwargs):
        items = money_spent_categories(
            request, self.user_provider(request), self.logged_user_id(request)
        )
        return Response(items)
