from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.utils.boiler_plate import get_generic_response
from onboarding.services.kyc_stage_report_utils import (
    kyc_discarded_generic,
    kyc_discarded_details_generic,
    self_queuecodes_pie_kyc_generic,
    queuecodes_pie_kyc_generic,
    kyc_total_applications_self_generic,
    kyc_total_applications_staff_generic,
)


class KYCStageReportViewSet(GenericViewSet):
    @extend_schema(
        operation_id="kyc_total_application_self",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_total_application_self")
    def kyc_total_application_self(self, request, *args, **kwargs):
        params = kyc_total_applications_self_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_total_application_staff",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_total_application_staff")
    def kyc_total_application_staff(self, request, *args, **kwargs):
        params = kyc_total_applications_staff_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_queuecodes_pie_kyc",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_queuecodes_pie_kyc")
    def self_queuecodes_pie_kyc(self, request, *args, **kwargs):
        items = self_queuecodes_pie_kyc_generic(request)
        return Response(items)

    @extend_schema(
        operation_id="staff_queuecodes_pie_kyc",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications by self at stages",
    )
    @action(methods=["POST"], detail=False, url_path="staff_queuecodes_pie_kyc")
    def staff_queuecodes_pie_kyc(self, request, *args, **kwargs):
        items = queuecodes_pie_kyc_generic(request, "Staff")
        return Response(items)

    # BIG NUMBER abandoned (discarded) applications self
    @extend_schema(
        operation_id="kyc_discarded_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_discarded_big_no")
    def kyc_discarded_big_no(self, request, *args, **kwargs):
        params = kyc_discarded_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_discarded_details",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_discarded_details")
    def kyc_discarded_details(self, request, *args, **kwargs):
        params = kyc_discarded_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_discarded_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_discarded_details_export_csv")
    def kyc_discarded_details_export_csv(self, request, *args, **kwargs):
        params = kyc_discarded_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "discarded_kyc.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_discarded_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_discarded_details_export_pdf")
    def kyc_discarded_details_export_pdf(self, request, *args, **kwargs):
        params = kyc_discarded_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "discarded_kyc.pdf",
                "title": "Discarded details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
