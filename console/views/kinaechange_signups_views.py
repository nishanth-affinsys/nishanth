from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from console.services.kinaechange_signups_utils import users_signups_generic
from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf


class KINASignupsViewSet(GenericViewSet):  # For kinaechange analytics

    @extend_schema(
        operation_id="users_signups_register_bigNo",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying total Registration",
    )
    @action(methods=["POST"], detail=False, url_path="users_signups_register_bigNo")
    def users_signups_register_bigno(self, request, *args, **kwargs):
        response, _, _ = users_signups_generic(request, "register-customer", True)
        return Response(data={"count": response})

    @extend_schema(
        operation_id="users_signups_register",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying total Registration",
    )
    @action(methods=["POST"], detail=False, url_path="users_signups_register")
    def users_signups_register(self, request, *args, **kwargs):
        response, _, _ = users_signups_generic(request, "register-customer", False)
        return return_table(response, request)

    @extend_schema(
        operation_id="users_signups_register_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying total Registration",
    )
    @action(
        methods=["POST"], detail=False, url_path="users_signups_register_export_csv"
    )
    def users_signups_register_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = users_signups_generic(
            request, "register-customer", False
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="users_signups_register_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying total Registration",
    )
    @action(
        methods=["POST"], detail=False, url_path="users_signups_register_export_pdf"
    )
    def users_signups_register_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = users_signups_generic(
            request, "register-customer", False
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Successful User Registrations",
            request.user.username,
        )
        return items
