from __future__ import annotations

from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import (
    return_table,
)
from main.utils.export import export_csv, export_pdf
from vision.services.vision_ocr_utils import (
    ocr_stage_bigno_generic,
    successful_vs_failed_trendline_ocr_generic,
    detailed_report_ocr_generic,
)

user_error = "User Error"
system_error = "System Error"
success = "Success"


class VisionOCRViewSet(GenericViewSet):
    @extend_schema(
        operation_id="total_ocr_calls_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of successful ocr",
    )
    @action(methods=["POST"], detail=False, url_path="total_ocr_calls_bigno")
    def total_ocr_calls_bigno(self, request, *args, **kwargs):
        params = ocr_stage_bigno_generic(
            request,
            [success, user_error, system_error],
        )
        return Response(params)

    @extend_schema(
        operation_id="total_successful_ocr_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of successful ocr",
    )
    @action(methods=["POST"], detail=False, url_path="total_successful_ocr_bigno")
    def total_successful_ocr_bigno(self, request, *args, **kwargs):
        params = ocr_stage_bigno_generic(
            request,
            [success],
        )
        return Response(params)

    @extend_schema(
        operation_id="total_failed_ocr_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="total_failed_ocr_bigno")
    def total_failed_ocr_bigno(self, request, *args, **kwargs):
        params = ocr_stage_bigno_generic(request, [user_error, system_error])
        return Response(params)

    @extend_schema(
        operation_id="successful_vs_failed_trendline_ocr",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(
        methods=["POST"], detail=False, url_path="successful_vs_failed_trendline_ocr"
    )
    def successful_vs_failed_trendline_ocr(self, request, *args, **kwargs):
        items, _, _ = successful_vs_failed_trendline_ocr_generic(request)
        return Response(items)

    @extend_schema(
        operation_id="aggregate_ocr_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="aggregate_ocr_details")
    def aggregate_ocr_details(self, request, *args, **kwargs):
        items, _, _ = successful_vs_failed_trendline_ocr_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="aggregate_ocr_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="aggregate_ocr_details_export_csv")
    def aggregate_ocr_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = successful_vs_failed_trendline_ocr_generic(
            request
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="aggregate_ocr_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="aggregate_ocr_details_export_pdf")
    def aggregate_ocr_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = successful_vs_failed_trendline_ocr_generic(
            request
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Aggregate Analysis of Users",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="successful_detailed_ocr_report",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="successful_detailed_ocr_report")
    def successful_detailed_ocr_report(self, request, *args, **kwargs):
        response, _, _ = detailed_report_ocr_generic(request, [success])
        return return_table(response, request)

    @extend_schema(
        operation_id="successful_detailed_ocr_report_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_detailed_ocr_report_export_csv",
    )
    def successful_detailed_ocr_report_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = detailed_report_ocr_generic(
            request, [success]
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="successful_detailed_ocr_report_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_detailed_ocr_report_export_pdf",
    )
    def successful_detailed_ocr_report_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = detailed_report_ocr_generic(
            request, [success]
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Successful Detections",
            request.user.username,
        )
        return items

    # failed ocr
    @extend_schema(
        operation_id="failed_detailed_ocr_report",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(methods=["POST"], detail=False, url_path="failed_detailed_ocr_report")
    def failed_detailed_ocr_report(self, request, *args, **kwargs):
        response, _, _ = detailed_report_ocr_generic(
            request, [user_error, system_error]
        )
        return return_table(response, request)

    @extend_schema(
        operation_id="failed_detailed_ocr_report_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="failed_detailed_ocr_report_export_csv",
    )
    def failed_detailed_ocr_report_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = detailed_report_ocr_generic(
            request, [user_error, system_error]
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="failed_detailed_ocr_report_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of failed ocr",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="failed_detailed_ocr_report_export_pdf",
    )
    def failed_detailed_ocr_report_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = detailed_report_ocr_generic(
            request, [user_error, system_error]
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Failed OCR Detections",
            request.user.username,
        )
        return items
