from auth.tags import AuthTags
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from client_specific.services.kina import (
    audit_trail_generic,
    onboarding_campaign_details_util
)
from main.utils.boiler_plate import get_generic_response


class OnboardingAuditViewSet(GenericViewSet):

    @extend_schema(
        operation_id="onboarding_audit_trail",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the audit trail for an onboarding application",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_audit_trail")
    def onboarding_audit_trail(self, request):
        params = audit_trail_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_audit_trail_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the audit trail for an onboarding application",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_audit_trail_export_csv"
    )
    def onboarding_audit_trail_export_csv(self, request):
        params = audit_trail_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Onboarding_reference_number",
                    "Kyc_reference",
                    "Event",
                    "Comment",
                    "Action_performed_by",
                    "Action_perform_timestamp"
                ],
                "fileName": "Audit_Trail.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_audit_trail_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the audit trail for an onboarding application",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_audit_trail_export_pdf"
    )
    def onboarding_audit_trail_export_pdf(self, request):
        params = audit_trail_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Onboarding_reference_number",
                    "Kyc_reference",
                    "Event",
                    "Comment",
                    "Action_performed_by",
                    "Action_perform_timestamp"
                ],
                "fileName": "Audit_Trail.pdf",
                "title": "Onboarding Audit Trail",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_campaign_details",
        tags=[AuthTags.INTERNAL],
        description="used to send the campaign the details of users who haven't completed the application",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_campaign_details")
    def onboarding_campaign_details(self, request):
        response = onboarding_campaign_details_util(request)
        return Response(response)
