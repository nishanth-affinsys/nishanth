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

from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf
from wallet.services.merchant_qr_utils import (
    total_merchant_qr_scanned_bigno_generic,
    total_merchant_qr_type_scanned_bigno_generic,
    merchant_revenue_by_qr_type_generic,
    merchant_qr_scanned_vs_successful_generic,
    merchant_transaction_details_by_qr,
    merchant_qr_created_generic,
)
from main.settings import MAX_PDF_LIMIT


class MerchantQRWalletViewSet(GenericViewSet):
    @extend_schema(
        operation_id="total_merchant_qr_scanned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="gives the count of the total qr scanned",
    )
    @action(methods=["POST"], detail=False, url_path="total_merchant_qr_scanned_bigno")
    def total_merchant_qr_scanned_bigno(self, request, *args, **kwargs):
        qs = total_merchant_qr_scanned_bigno_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="total_merchant_dynamic_qr_scanned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="gives the total count of dynamic qr scanned",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="total_merchant_dynamic_qr_scanned_bigno",
    )
    def total_merchant_dynamic_qr_scanned_bigno(self, request, *args, **kwargs):
        qs = total_merchant_qr_type_scanned_bigno_generic(request, "dynamic")
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="total_merchant_static_qr_scanned_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="total_merchant_static_qr_scanned_bigno",
    )
    def total_merchant_static_qr_scanned_bigno(self, request, *args, **kwargs):
        qs = total_merchant_qr_type_scanned_bigno_generic(request, "static")
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="merchant_qr_created",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(methods=["POST"], detail=False, url_path="merchant_qr_created")
    def merchant_qr_created(self, request, *args, **kwargs):
        qs = merchant_qr_created_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_qr_scanned_vs_successful",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"], detail=False, url_path="merchant_qr_scanned_vs_successful"
    )
    def merchant_qr_scanned_vs_successful(self, request, *args, **kwargs):
        qs = merchant_qr_scanned_vs_successful_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_average_revenue_by_qr_type",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"], detail=False, url_path="merchant_average_revenue_by_qr_type"
    )
    def merchant_average_revenue_by_qr_type(self, request, *args, **kwargs):
        qs = merchant_revenue_by_qr_type_generic(request, aggregation_function=Avg)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_max_revenue_by_qr_type",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(methods=["POST"], detail=False, url_path="merchant_max_revenue_by_qr_type")
    def merchant_max_revenue_by_qr_type(self, request, *args, **kwargs):
        qs = merchant_revenue_by_qr_type_generic(request, aggregation_function=Max)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_revenue_by_qr_type",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(methods=["POST"], detail=False, url_path="merchant_revenue_by_qr_type")
    def merchant_revenue_by_qr_type(self, request, *args, **kwargs):
        qs = merchant_revenue_by_qr_type_generic(request, aggregation_function=Sum)
        return Response(qs)

    @extend_schema(
        operation_id="merchant_transaction_details_by_qr",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"], detail=False, url_path="merchant_transaction_details_by_qr"
    )
    def merchant_transaction_details_by_qr(self, request, *args, **kwargs):
        qs, _, _ = merchant_transaction_details_by_qr(request)
        return return_table(qs, request)

    @extend_schema(
        operation_id="merchant_transaction_details_by_qr_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_details_by_qr_export_csv",
    )
    def merchant_transaction_details_by_qr_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_transaction_details_by_qr(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="merchant_transaction_details_by_qr_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Gives the total count of static QRs that were scanned",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="merchant_transaction_details_by_qr_export_pdf",
    )
    def merchant_transaction_details_by_qr_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = merchant_transaction_details_by_qr(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Transaction Details",
            request.user.username,
        )
        return items
