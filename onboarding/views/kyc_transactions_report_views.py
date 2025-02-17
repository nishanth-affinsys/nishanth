from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from main.utils.boiler_plate import get_generic_response
from onboarding.services.kyc_transactions_report_utils import (
    kyc_success_bigno_generic,
    kyc_failed_bigno_generic,
    kyc_exceptions_big_no_generic,
    kyc_transaction_details_report_generic,
    kyc_onboarding_details_comments_generic,
    kyc_onboarding_success_bigno_generic,
)


class KYCTransactionReportViewSet(GenericViewSet):
    @extend_schema(
        operation_id="kyc_onboarding_successful_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_onboarding_successful_big_no")
    def kyc_onboarding_successful_big_no(self, request, *args, **kwargs):
        params = kyc_onboarding_success_bigno_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_successful_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_successful_big_no")
    def kyc_successful_big_no(self, request, *args, **kwargs):
        params = kyc_success_bigno_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_successful_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_successful_details")
    def kyc_successful_details(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(request, "QSUCCESS")
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_successful_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_successful_details_export_csv"
    )
    def kyc_successful_details_export_csv(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QSUCCESS",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "KYC_successful_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_successful_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_successful_details_export_pdf"
    )
    def kyc_successful_details_export_pdf(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QSUCCESS",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "KYC_successful_details.pdf",
                "title": "KYC Successful Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_failed_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_failed_big_no")
    def kyc_failed_big_no(self, request, *args, **kwargs):
        params = kyc_failed_bigno_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_onboarding_successful_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_onboarding_successful_details")
    def kyc_onboarding_successful_details(self, request, *args, **kwargs):
        params = kyc_onboarding_details_comments_generic(request, "QSUCCESS")
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_onboarding_successful_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_onboarding_successful_details_export_csv"
    )
    def kyc_onboarding_successful_details_export_csv(self, request, *args, **kwargs):
        params = kyc_onboarding_details_comments_generic(
            request,
            "QSUCCESS",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_status",
                    "Comments",
                    "Last_modified_timestamp",
                    "Action_code"
                ],
                "fileName": "KYC_successful_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_onboarding_successful_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_onboarding_successful_details_export_pdf"
    )
    def kyc_onboarding_successful_details_export_pdf(self, request, *args, **kwargs):
        params = kyc_onboarding_details_comments_generic(
            request,
            "QSUCCESS",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Approved_by",
                    "Approved_timestamp",
                    "Application_status",
                    "Comments",
                    "Last_modified_timestamp",
                    "Action_code"
                ],
                "fileName": "KYC_successful_details.pdf",
                "title": "KYC Successful Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_rejected_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_rejected_details")
    def kyc_rejected_details(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(request, "QREJECT")
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_rejected_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_rejected_details_export_csv")
    def kyc_rejected_details_export_csv(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QREJECT",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Rejected_by",
                    "Rejected_timestamp",
                    "Application_status",
                    "Comments",
                    "Last_modified_timestamp",
                    "Action_code"
                ],
                "fileName": "KYC_rejected_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_rejected_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_rejected_details_export_pdf")
    def kyc_rejected_details_export_pdf(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QREJECT",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Rejected_by",
                    "Rejected_timestamp",
                    "Application_status",
                    "Comments",
                    "Last_modified_timestamp",
                    "Action_code"
                ],
                "fileName": "KYC_rejected_details.pdf",
                "title": "Rejected KYCs",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_exceptions_big_no",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_exceptions_big_no")
    def kyc_exceptions_big_no(self, request, *args, **kwargs):
        params = kyc_exceptions_big_no_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_exceptions_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_exceptions_details")
    def kyc_exceptions_details(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(request, "QEXCEPTION")
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_exceptions_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_exceptions_details_export_csv"
    )
    def kyc_exceptions_details_export_csv(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QEXCEPTION",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                ],
                "fileName": "KYC_exception_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="kyc_exceptions_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all failed transactions for retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="kyc_exceptions_details_export_pdf"
    )
    def kyc_exceptions_details_export_pdf(self, request, *args, **kwargs):
        params = kyc_transaction_details_report_generic(
            request,
            "QEXCEPTION",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "KYC_number",
                    "Customer_name",
                    "Customer_type",
                    "Channel",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                ],
                "fileName": "KYC_exception_details.pdf",
                "title": "KYC Exceptions Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
