from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from wallet.services.merchant_profit_utils import (
    customer_segmentation_bubbles_generic,
    average_revenue_trendline_merch_generic,
    merchant_hourly_analysis_generic,
)


class MerchantProfitWalletViewSet(GenericViewSet):
    @extend_schema(
        operation_id="customer_segmentation_bubbles_merch",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the details of average transaction anount, transaction and no of people",
    )
    @action(
        methods=["POST"], detail=False, url_path="customer_segmentation_bubbles_merch"
    )
    def customer_segmentation_bubbles_merch(self, request, *args, **kwargs):
        qs = customer_segmentation_bubbles_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="average_revenue_trendline_merch",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the details of average transaction anount, transaction and no of people",
    )
    @action(methods=["POST"], detail=False, url_path="average_revenue_trendline_merch")
    def average_revenue_trendline_merch(self, request, *args, **kwargs):
        qs = average_revenue_trendline_merch_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_hourly_trendline",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the max revenue earned by merchants",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_hourly_trendline",
    )
    def merchant_hourly_trendline(self, request, *args, **kwargs):
        params = merchant_hourly_analysis_generic(request)
        return Response(params)
