from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from onboarding.models import SingleCifRetailData, SingleCifSpData
from onboarding.services.onboarding_trend_report_utils import (
    channelwise_onboarding_generic,
    total_customer_onboarded_generic,
    productwise_account_opened_generic,
)


class TrendReportViewSet(GenericViewSet):
    # retail reports
    @extend_schema(
        operation_id="channelwise_etb_onboarding_rt",
        tags=[AuthTags.AUTHORIZE],
        description="A multiline chart of which shows agent,staff,self successful onboarding count",
    )
    @action(methods=["POST"], detail=False, url_path="channelwise_etb_onboarding_rt")
    def channelwise_etb_onboarding_rt(self, request, *args, **kwargs):
        items = channelwise_onboarding_generic(request, SingleCifRetailData, "etb")
        return Response(items)

    @extend_schema(
        operation_id="channelwise_ntb_onboarding_rt",
        tags=[AuthTags.AUTHORIZE],
        description="A multiline chart of which shows agent,staff,self successful onboarding count",
    )
    @action(methods=["POST"], detail=False, url_path="channelwise_ntb_onboarding_rt")
    def channelwise_ntb_onboarding_rt(self, request, *args, **kwargs):
        items = channelwise_onboarding_generic(request, SingleCifRetailData, "ntb")
        return Response(items)

    @extend_schema(
        operation_id="total_customer_onboarded_etb_rt",
        tags=[AuthTags.AUTHORIZE],
        description="A line chart Total ETB customers onboarded every month",
    )
    @action(methods=["POST"], detail=False, url_path="total_customer_onboarded_etb_rt")
    def total_customer_onboarded_etb_rt(self, request, *args, **kwargs):
        items = total_customer_onboarded_generic(request, SingleCifRetailData, "etb")
        return Response(items)

    @extend_schema(
        operation_id="total_customer_onboarded_ntb_rt",
        tags=[AuthTags.AUTHORIZE],
        description="A line chart Total NTB customers onboarded every month",
    )
    @action(methods=["POST"], detail=False, url_path="total_customer_onboarded_ntb_rt")
    def total_customer_onboarded_ntb_rt(self, request, *args, **kwargs):
        items = total_customer_onboarded_generic(request, SingleCifRetailData, "ntb")
        return Response(items)

    @extend_schema(
        operation_id="productwise_account_opened_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Productwise no of successful accounts opened",
    )
    @action(methods=["POST"], detail=False, url_path="productwise_account_opened_rt")
    def productwise_account_opened_rt(self, request, *args, **kwargs):
        items = productwise_account_opened_generic(request, SingleCifRetailData)
        return Response(items)

    # SP reports
    @extend_schema(
        operation_id="channelwise_etb_onboarding_sp",
        tags=[AuthTags.AUTHORIZE],
        description="A multiline chart of which shows agent,staff,self successful onboarding count",
    )
    @action(methods=["POST"], detail=False, url_path="channelwise_etb_onboarding_sp")
    def channelwise_etb_onboarding_sp(self, request, *args, **kwargs):
        items = channelwise_onboarding_generic(request, SingleCifSpData, "etb")
        return Response(items)

    @extend_schema(
        operation_id="channelwise_ntb_onboarding_sp",
        tags=[AuthTags.AUTHORIZE],
        description="A multiline chart of which shows agent,staff,self successful onboarding count",
    )
    @action(methods=["POST"], detail=False, url_path="channelwise_ntb_onboarding_sp")
    def channelwise_ntb_onboarding_sp(self, request, *args, **kwargs):
        items = channelwise_onboarding_generic(request, SingleCifSpData, "ntb")
        return Response(items)

    @extend_schema(
        operation_id="total_customer_onboarded_etb_sp",
        tags=[AuthTags.AUTHORIZE],
        description="A line chart Total ETB customers onboarded every month",
    )
    @action(methods=["POST"], detail=False, url_path="total_customer_onboarded_etb_sp")
    def total_customer_onboarded_etb_sp(self, request, *args, **kwargs):
        items = total_customer_onboarded_generic(request, SingleCifSpData, "etb")
        return Response(items)

    @extend_schema(
        operation_id="total_customer_onboarded_ntb_sp",
        tags=[AuthTags.AUTHORIZE],
        description="A line chart Total NTB customers onboarded every month",
    )
    @action(methods=["POST"], detail=False, url_path="total_customer_onboarded_ntb_sp")
    def total_customer_onboarded_ntb_sp(self, request, *args, **kwargs):
        items = total_customer_onboarded_generic(request, SingleCifSpData, "ntb")
        return Response(items)

    @extend_schema(
        operation_id="productwise_account_opened_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Productwise no of successful accounts opened",
    )
    @action(methods=["POST"], detail=False, url_path="productwise_account_opened_sp")
    def productwise_account_opened_sp(self, request, *args, **kwargs):
        items = productwise_account_opened_generic(request, SingleCifSpData)
        return Response(items)
