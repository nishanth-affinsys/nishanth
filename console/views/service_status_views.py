from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from console.services.service_status_utils import service_status_generic
from django.conf import settings
from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf


class ServiceStatusViewSet(GenericViewSet):
    @extend_schema(
        operation_id="service_status",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the service status of each service",
    )
    @action(methods=["POST"], detail=False, url_path="service_status")
    def service_status(self, request, *args, **kwargs):
        response, _, _ = service_status_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="service_status_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the service status in csv",
    )
    @action(methods=["POST"], detail=False, url_path="service_status_export_csv")
    def service_status_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = service_status_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="service_status_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the service status in pdf",
    )
    @action(methods=["POST"], detail=False, url_path="service_status_export_pdf")
    def service_status_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = service_status_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Service Status",
            request.user.username,
        )
        return items
