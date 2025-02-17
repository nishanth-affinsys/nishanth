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
from vision.services.vision_forgery_utils import (
    forgery_check_big_no,
    successful_vs_failed_trendline_forgery_generic,
    forgery_details_generic,
    system_error_forgery_details_generic,
)

user_error = "User Error"
system_error = "System Error"
success = "Success"


class VisionForgeryViewSet(GenericViewSet):
    @extend_schema(
        operation_id="total_forgery_check_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="total_forgery_check_big_no")
    def total_forgery_check_big_no(self, request, *args, **kwargs):
        params = forgery_check_big_no(request, [success, user_error, system_error])
        return Response(params)

    @extend_schema(
        operation_id="genuine_docs_detected_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="genuine_docs_detected_big_no")
    def genuine_docs_detected_big_no(self, request, *args, **kwargs):
        params = forgery_check_big_no(request, [success])
        return Response(params)

    @extend_schema(
        operation_id="forged_docs_detected_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="forged_docs_detected_big_no")
    def forged_docs_detected_big_no(self, request, *args, **kwargs):
        params = forgery_check_big_no(request, [user_error])
        return Response(params)

    @extend_schema(
        operation_id="forgery_system_error_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="forgery_system_error_big_no")
    def forgery_system_error_big_no(self, request, *args, **kwargs):
        params = forgery_check_big_no(request, [system_error])
        return Response(params)

    @extend_schema(
        operation_id="forgery_genuine_vs_forged_trendline",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="forgery_genuine_vs_forged_trendline"
    )
    def forgery_genuine_vs_forged_trendline(self, request, *args, **kwargs):
        params, _, _ = successful_vs_failed_trendline_forgery_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="forgery_genuine_docs_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="forgery_genuine_docs_details")
    def forgery_genuine_docs_details(self, request, *args, **kwargs):
        result, _, _ = forgery_details_generic(request, [success])
        return return_table(result, request)

    @extend_schema(
        operation_id="forgery_genuine_docs_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_genuine_docs_details_export_csv",
    )
    def forgery_genuine_docs_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = forgery_details_generic(request, [success])
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="forgery_genuine_docs_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_genuine_docs_details_export_pdf",
    )
    def forgery_genuine_docs_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = forgery_details_generic(request, [success])
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Genuine Documents",
            request.user.username,
        )
        return items

    # forged docs details

    @extend_schema(
        operation_id="forgery_docs_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="forgery_docs_details")
    def forgery_docs_details(self, request, *args, **kwargs):
        response, _, _ = forgery_details_generic(request, [user_error])
        return return_table(response, request)

    @extend_schema(
        operation_id="forgery_docs_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_docs_details_export_csv",
    )
    def forgery_docs_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = forgery_details_generic(
            request, [user_error]
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="forgery_docs_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_docs_details_export_pdf",
    )
    def forgery_docs_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = forgery_details_generic(
            request, [user_error]
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Forged Documents",
            request.user.username,
        )
        return items

    # system error details

    @extend_schema(
        operation_id="forgery_system_error_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="forgery_system_error_details")
    def forgery_system_error_details(self, request, *args, **kwargs):
        response, _, _ = system_error_forgery_details_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="forgery_system_error_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_system_error_details_export_csv",
    )
    def forgery_system_error_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = system_error_forgery_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="forgery_system_error_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="forgery_system_error_details_export_pdf",
    )
    def forgery_system_error_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = system_error_forgery_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "System Error",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="aggregate_analysis_forgery",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="aggregate_analysis_forgery")
    def aggregate_analysis_forgery(self, request, *args, **kwargs):
        params, _, _ = successful_vs_failed_trendline_forgery_generic(request)
        return return_table(params, request)

    @extend_schema(
        operation_id="aggregate_analysis_forgery_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="aggregate_analysis_forgery_export_csv"
    )
    def aggregate_analysis_forgery_export_csv(self, request, *args, **kwargs):
        params, field_names, file_name = successful_vs_failed_trendline_forgery_generic(
            request
        )
        items = export_csv(params, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="aggregate_analysis_forgery_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="aggregate_analysis_forgery_export_pdf"
    )
    def aggregate_analysis_forgery_export_pdf(self, request, *args, **kwargs):
        params, field_names, file_name = successful_vs_failed_trendline_forgery_generic(
            request
        )
        if len(params) > MAX_PDF_LIMIT:
            params = params[:MAX_PDF_LIMIT]
        items = export_pdf(
            params,
            field_names,
            f"{file_name}.pdf",
            "Aggregate Analysis",
            request.user.username,
        )
        return items
