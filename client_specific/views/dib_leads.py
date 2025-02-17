from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from client_specific.services.dib_leads import (
    leads_generated_count,
    leads_generated_generic,
)
from main.utils.boiler_plate import (
    get_generic_response,
)


class DIBLeadsDashboard(GenericViewSet):

    @extend_schema(
        operation_id="leads_generated_count",
        tags=[AuthTags.AUTHORIZE],
        description="This displays the count of total leads generated.",
    )
    @action(methods=["POST"], detail=False, url_path="leads_generated_count")
    def leads_generated_count(self, request):
        params = leads_generated_count(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="leads_generated_details",
        tags=[AuthTags.AUTHORIZE],
        description="This displays the details of leads generated.",
    )
    @action(methods=["POST"], detail=False, url_path="leads_generated_details")
    def leads_generated_details(self, request):
        params = leads_generated_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="leads_generated_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to export the details of leads generated in csv",
    )
    @action(
        methods=["POST"], detail=False, url_path="leads_generated_details_export_csv"
    )
    def leads_generated_details_export_csv(self, request):
        params = leads_generated_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Message",
                    "Intent",
                    "Timestamp",
                    "Customer_type",
                ],
                "fileName": "Leads generated.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="leads_generated_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to export the details of leads generated in csv",
    )
    @action(
        methods=["POST"], detail=False, url_path="leads_generated_details_export_pdf"
    )
    def leads_generated_details_export_pdf(self, request):
        params = leads_generated_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Message",
                    "Intent",
                    "Timestamp",
                    "Customer_type",
                ],
                "fileName": "Leads generated.csv",
                "title": "Leads Generated",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
