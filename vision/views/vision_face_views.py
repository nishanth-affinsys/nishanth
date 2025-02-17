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
from vision.services.vision_face_utils import (
    face_stage_bigno_generic,
    successful_vs_failed_trendline_face_generic,
    success_face_stage_bigno_generic,
    face_success_details_generic,
    face_failed_details_generic,
)

user_error = "User Error"
system_error = "System Error"


class VisionFaceViewSet(GenericViewSet):
    @extend_schema(
        operation_id="total_face_detections_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="total_face_detections_bigno")
    def total_face_detections_bigno(self, request, *args, **kwargs):
        params = face_stage_bigno_generic(
            request, ["Success", user_error, system_error]
        )
        return Response(params)

    @extend_schema(
        operation_id="total_success_detect_verification_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="total_success_detect_verification_bigno",
    )
    def total_success_detect_verification_bigno(self, request, *args, **kwargs):
        params = success_face_stage_bigno_generic(
            request, ["Detection_Only_Passed", "Verification_Passed"]
        )
        return Response(params)

    @extend_schema(
        operation_id="total_success_detections_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="total_success_detections_bigno",
    )
    def total_success_detections_bigno(self, request, *args, **kwargs):
        params = success_face_stage_bigno_generic(request, ["Detection_Only_Passed"])
        return Response(params)

    @extend_schema(
        operation_id="total_success_verifications_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="total_success_verifications_bigno",
    )
    def total_success_verifications_bigno(self, request, *args, **kwargs):
        params = success_face_stage_bigno_generic(request, ["Verification_Passed"])
        return Response(params)

    @extend_schema(
        operation_id="failed_face_detections_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(methods=["POST"], detail=False, url_path="failed_face_detections_bigno")
    def failed_face_detections_bigno(self, request, *args, **kwargs):
        params = face_stage_bigno_generic(request, [user_error, system_error])
        return Response(params)

    @extend_schema(
        operation_id="system_error_face_detections_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total successful faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="system_error_face_detections_bigno"
    )
    def system_error_face_detections_bigno(self, request, *args, **kwargs):
        params = face_stage_bigno_generic(request, [system_error])
        return Response(params)

    @extend_schema(
        operation_id="user_error_face_detections_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(methods=["POST"], detail=False, url_path="user_error_face_detections_bigno")
    def user_error_face_detections_bigno(self, request, *args, **kwargs):
        params = face_stage_bigno_generic(request, [user_error])
        return Response(params)

    @extend_schema(
        operation_id="successful_vs_failed_face_trendline",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="successful_vs_failed_face_trendline"
    )
    def successful_vs_failed_face_trendline(self, request, *args, **kwargs):
        items, _, _ = successful_vs_failed_trendline_face_generic(request)
        return Response(items)

    @extend_schema(
        operation_id="face_successful_detection_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="face_successful_detection_details"
    )
    def face_successful_detection_details(self, request, *args, **kwargs):
        response, _, _ = face_success_details_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="face_successful_detection_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="face_successful_detection_details_export_csv",
    )
    def face_successful_detection_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = face_success_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="face_successful_detection_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="face_successful_detection_details_export_pdf",
    )
    def face_successful_detection_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = face_success_details_generic(request)
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

    # @extend_schema(
    #     operation_id="face_successful_verification_details",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total count of total faces",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="face_successful_verification_details"
    # )
    # def face_successful_verification_details(self, request, *args, **kwargs):
    #     response, _, _ = face_success_details_generic(
    #         request, "face_verification_score", "face_verification_threshold"
    #     )
    #     return return_table(response, request)
    #
    # @extend_schema(
    #     operation_id="face_successful_verification_details_export_csv",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total count of total user error faces",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="face_successful_verification_details_export_csv",
    # )
    # def face_successful_verification_details_export_csv(self, request, *args, **kwargs):
    #     response, field_names, file_name = face_success_details_generic(
    #         request, "face_verification_score", "face_verification_threshold"
    #     )
    #     items = export_csv(response, field_names, f"{file_name}.csv")
    #     return items
    #
    # @extend_schema(
    #     operation_id="face_successful_verification_details_export_pdf",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total count of total user error faces",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="face_successful_verification_details_export_pdf",
    # )
    # def face_successful_verification_details_export_pdf(self, request, *args, **kwargs):
    #     response, field_names, file_name = face_success_details_generic(
    #         request, "face_verification_score", "face_verification_threshold"
    #     )
    #     if len(response) > MAX_PDF_LIMIT:
    #         response = response[:MAX_PDF_LIMIT]
    #     items = export_pdf(
    #         response, field_names, f"{file_name}.pdf", "Successful Verification",request.user.username
    #     )
    #     return items

    @extend_schema(
        operation_id="face_failed_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(methods=["POST"], detail=False, url_path="face_failed_details")
    def face_failed_details(self, request, *args, **kwargs):
        params, _, _ = face_failed_details_generic(request)
        return return_table(params, request)

    @extend_schema(
        operation_id="face_failed_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(methods=["POST"], detail=False, url_path="face_failed_details_export_csv")
    def face_failed_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = face_failed_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="face_failed_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(methods=["POST"], detail=False, url_path="face_failed_details_export_pdf")
    def face_failed_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = face_failed_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Failed Recognitions",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="aggregate_analysis_face",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(methods=["POST"], detail=False, url_path="aggregate_analysis_face")
    def aggregate_analysis_face(self, request, *args, **kwargs):
        items, _, _ = successful_vs_failed_trendline_face_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="aggregate_analysis_face_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="aggregate_analysis_face_export_csv"
    )
    def aggregate_analysis_face_export_csv(self, request, *args, **kwargs):
        params, field_names, file_name = successful_vs_failed_trendline_face_generic(
            request
        )
        items = export_csv(params, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="aggregate_analysis_face_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of total user error faces",
    )
    @action(
        methods=["POST"], detail=False, url_path="aggregate_analysis_face_export_pdf"
    )
    def aggregate_analysis_face_export_pdf(self, request, *args, **kwargs):
        params, field_names, file_name = successful_vs_failed_trendline_face_generic(
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
