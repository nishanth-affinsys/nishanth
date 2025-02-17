from auth.tags import AuthTags
from django.db.models import (
    Sum,
    Max,
    Avg,
)
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from main.utils.boiler_plate import get_generic_response, return_table
from main.utils.export import export_csv, export_pdf
from wallet.services.merchant_transaction_utils import (
    merchant_transactions_bigno_generic,
    merchant_revenue_earned_bigno_generic,
    merchant_max_revenue_earned_generic,
    merchant_transaction_trend_by_day_generic,
    merchant_revenue_trend_by_day_generic,
    merchant_transaction_history,
    merchant_revenue_hierarchy_sunburst_generic,
    merchant_trans_initiated_bigno_generic,
)


class MerchantTransactionWalletViewSet(GenericViewSet):
    @extend_schema(
        operation_id="merchant_transactions_initiated_by_customer_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count transactions initiated",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transactions_initiated_by_customer_bigno",
    )
    def merchant_transactions_initiated_by_customer_bigno(
        self, request, *args, **kwargs
    ):
        params = merchant_trans_initiated_bigno_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="merchant_successful_transactions_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count transactions that were successful",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_successful_transactions_bigno",
    )
    def merchant_successful_transactions_bigno(self, request, *args, **kwargs):
        params = merchant_transactions_bigno_generic(request, "S")
        return Response(params)

    @extend_schema(
        operation_id="merchant_failed_transactions_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count transactions that failed",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_failed_transactions_bigno",
    )
    def merchant_failed_transactions_bigno(self, request, *args, **kwargs):
        params = merchant_transactions_bigno_generic(request, "F")
        return Response(params)

    @extend_schema(
        operation_id="merchant_inprogress_transactions_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count transactions that are in progress",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_inprogress_transactions_bigno",
    )
    def merchant_inprogress_transactions_bigno(self, request, *args, **kwargs):
        params = merchant_transactions_bigno_generic(request, "P")
        return Response(params)

    @extend_schema(
        operation_id="merchant_abandoned_transactions_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count transactions that are abandoned",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_abandoned_transactions_bigno",
    )
    def merchant_abandoned_transactions_bigno(self, request, *args, **kwargs):
        params = merchant_transactions_bigno_generic(request, "A")
        return Response(params)

    @extend_schema(
        operation_id="merchant_revenue_earned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_revenue_earned_bigno",
    )
    def merchant_revenue_earned_bigno(self, request, *args, **kwargs):
        params = merchant_revenue_earned_bigno_generic(request, Sum)
        return Response(params)

    @extend_schema(
        operation_id="merchant_avg_revenue_earned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_avg_revenue_earned_bigno",
    )
    def merchant_avg_revenue_earned_bigno(self, request, *args, **kwargs):
        params = merchant_revenue_earned_bigno_generic(request, Avg)
        return Response(params)

    @extend_schema(
        operation_id="merchant_max_revenue_earned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_max_revenue_earned_bigno",
    )
    def merchant_max_revenue_earned_bigno(self, request, *args, **kwargs):
        params = merchant_revenue_earned_bigno_generic(request, Max)
        return Response(params)

    @extend_schema(
        operation_id="merchant_max_revenue_earned",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants for the product",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_max_revenue_earned",
    )
    def merchant_max_revenue_earned(self, request, *args, **kwargs):
        params, _, _ = merchant_max_revenue_earned_generic(request)
        return return_table(params, request)

    @extend_schema(
        operation_id="merchant_max_revenue_earned_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_max_revenue_earned_export_csv",
    )
    def merchant_max_revenue_earned_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_max_revenue_earned_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="merchant_max_revenue_earned_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_max_revenue_earned_export_pdf",
    )
    def merchant_max_revenue_earned_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_max_revenue_earned_generic(request)
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Max Revenue",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="merchant_transaction_trendline",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_trendline",
    )
    def merchant_transaction_trendline(self, request, *args, **kwargs):
        params = merchant_transaction_trend_by_day_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="merchant_revenue_trendline",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_revenue_trendline",
    )
    def merchant_revenue_trendline(self, request, *args, **kwargs):
        params = merchant_revenue_trend_by_day_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="merchant_transaction_history",
        tags=[AuthTags.AUTHORIZE],
        description="gives the retails of merchant revenue that was recieved",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_history",
    )
    def merchant_transaction_history(self, request, *args, **kwargs):
        items, _, _ = merchant_transaction_history(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="merchant_transaction_history_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="gives the retails of merchant revenue that was recieved",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_history_export_csv",
    )
    def merchant_transaction_history_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_transaction_history(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="merchant_transaction_history_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="gives the retails of merchant revenue that was recieved",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_history_export_pdf",
    )
    def merchant_transaction_history_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_transaction_history(request)
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Transaction Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="merchant_revenue_hierarchy_sunburst",
        tags=[AuthTags.AUTHORIZE],
        description="gives the retails of merchant revenue hierarchy for every merchant",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_revenue_hierarchy_sunburst",
    )
    def merchant_revenue_hierarchy_sunburst(self, request, *args, **kwargs):
        items = merchant_revenue_hierarchy_sunburst_generic(request, "revenue")
        return Response(items)

    @extend_schema(
        operation_id="merchant_transactions_hierarchy_sunburst",
        tags=[AuthTags.AUTHORIZE],
        description="gives the retails of merchant revenue hierarchy for every merchant",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transactions_hierarchy_sunburst",
    )
    def merchant_transactions_hierarchy_sunburst(self, request, *args, **kwargs):
        items = merchant_revenue_hierarchy_sunburst_generic(request, "transactions")
        return Response(items)
