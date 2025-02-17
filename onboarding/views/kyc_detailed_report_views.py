from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from main.utils.boiler_plate import get_generic_response

from onboarding.services.kyc_detailed_report_utils import kyc_detailed_report_generic, \
    kyc_onboarding_detailed_report_generic


class KYCDetailedReport(GenericViewSet):
    @extend_schema(
        operation_id="kyc_detailed_report",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_report")
    def kyc_detailed_report(self, request, *args, **kwargs):
        params = kyc_detailed_report_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_detailed_report_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_report_export_csv")
    def kyc_detailed_report_export_csv(self, request, *args, **kwargs):
        params = kyc_detailed_report_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Product_name",
                    "Customer_name",
                    "Phone_Number",
                    "Created_by",
                    "Created_timestamp",
                    "Last_action_performed_by",
                    "Last_action_perform_timestamp",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_stage",
                    "Customer_type",
                    "Channel",
                ],
                "fileName": "kyc_detailed_report.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_detailed_report_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_report_export_pdf")
    def kyc_detailed_report_export_pdf(self, request, *args, **kwargs):
        params = kyc_detailed_report_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Product_name",
                    "Customer_name",
                    "Phone_Number",
                    "Created_by",
                    "Created_timestamp",
                    "Last_action_performed_by",
                    "Last_action_performed_timestamp",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_stage",
                    "Customer_type",
                    "Channel",
                ],
                "fileName": "kyc_detailed_report.pdf",
                "title": "KYC Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_detailed_comments_report",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_comments_report")
    def kyc_detailed_comments_report(self, request, *args, **kwargs):
        params = kyc_onboarding_detailed_report_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_detailed_comments_report_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_comments_report_export_csv")
    def kyc_detailed_comments_report_export_csv(self, request, *args, **kwargs):
        params = kyc_onboarding_detailed_report_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Product_name",
                    "Customer_name",
                    "Phone_Number",
                    "Created_by",
                    "Created_timestamp",
                    "Last_action_performed_by",
                    "Last_action_perform_timestamp",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_stage",
                    "Customer_type",
                    "Channel",
                    "Comments"
                ],
                "fileName": "kyc_detailed_comments_report.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_detailed_comments_report_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of kyc",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_detailed_comments_report_export_pdf")
    def kyc_detailed_comments_report_export_pdf(self, request, *args, **kwargs):
        params = kyc_onboarding_detailed_report_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Product_name",
                    "Customer_name",
                    "Phone_Number",
                    "Created_by",
                    "Created_timestamp",
                    "Last_action_performed_by",
                    "Last_action_performed_timestamp",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_stage",
                    "Customer_type",
                    "Channel",
                    "Comments"
                ],
                "fileName": "kyc_detailed_comments_report.pdf",
                "title": "KYC Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
