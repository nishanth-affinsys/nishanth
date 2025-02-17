from auth.tags import AuthTags

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.conf import settings
from main.utils.export import export_csv, export_pdf
from main.utils.boiler_plate import (
    get_generic_response,
    return_table,
)
from profile_data.services.profile_analytics_utils import (
    total_profiles_created,
    total_is_authenticated_profiles,
    authenticated_or_not,
    authenticated_details,
    unauthenticated_details,
    profile_opted_in_or_out_details,
)


from drf_spectacular.utils import extend_schema


class ProfileDataViewSet(GenericViewSet):
    @extend_schema(
        operation_id="profile_total_profiles_created",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the ig number of the total profiles created",
    )
    @action(methods=["POST"], detail=False, url_path="profile_total_profiles_created")
    def profile_total_profiles_created(self, request, *args, **kwargs):
        params = total_profiles_created(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_total_verified",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the ig number of the total profiles are verified",
    )
    @action(methods=["POST"], detail=False, url_path="profile_total_authenticated")
    def profile_total_authenticated(self, request, *args, **kwargs):
        params = total_is_authenticated_profiles(request, True)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_total_unauthenticated",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the ig number of the total profiles that are unauthenticated",
    )
    @action(methods=["POST"], detail=False, url_path="profile_total_unauthenticated")
    def profile_total_unauthenticated(self, request, *args, **kwargs):
        params = total_is_authenticated_profiles(request, False)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_authenticated_or_not",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the big number authenticated profiles or not",
    )
    @action(methods=["POST"], detail=False, url_path="profile_authenticated_or_not")
    def profile_authenticated_or_not(self, request, *args, **kwargs):
        params = authenticated_or_not(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_verified_user_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user",
    )
    @action(methods=["POST"], detail=False, url_path="profile_verified_user_details")
    def profile_verified_user_details(self, request, *args, **kwargs):
        params, field_names, file_name = authenticated_details(request)
        return return_table(params, request)

    @extend_schema(
        operation_id="profile_verified_user_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_verified_user_details_export_csv",
    )
    def profile_verified_user_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = authenticated_details(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="profile_verified_user_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_verified_user_details_export_pdf",
    )
    def profile_verified_user_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = authenticated_details(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Verified Profile Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="profile_unverified_user_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user",
    )
    @action(methods=["POST"], detail=False, url_path="profile_unverified_user_details")
    def profile_unverified_user_details(self, request, *args, **kwargs):
        params, _, _ = unauthenticated_details(request)
        return return_table(params, request)

    @extend_schema(
        operation_id="profile_unverified_user_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_unverified_user_details_export_csv",
    )
    def profile_unverified_user_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = unauthenticated_details(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="profile_unverified_user_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_unverified_user_details_export_pdf",
    )
    def profile_unverified_user_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = unauthenticated_details(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Unverified User Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="profile_opted_category_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of opted in or opted out  user",
    )
    @action(methods=["POST"], detail=False, url_path="profile_opted_category_details")
    def profile_opted_category_details(self, request, *args, **kwargs):
        params = profile_opted_in_or_out_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_opted_category_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_opted_category_details_export_csv",
    )
    def profile_opted_category_details_export_csv(self, request, *args, **kwargs):
        params = profile_opted_in_or_out_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Username",
                    "Channel",
                    "Channel_Id",
                    "Opted_In",
                    "Opted_Out",
                    "Timestamp",
                ],
                "fileName": "opted_category_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_opted_category_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the details of authenticated user in export pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_opted_category_details_export_pdf",
    )
    def profile_opted_category_details_export_pdf(self, request, *args, **kwargs):
        params = profile_opted_in_or_out_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Username",
                    "Phone_Number",
                    "Email",
                    "Timestamp",
                ],
                "fileName": "opted_category_details.pdf",
                "title": "Opted Category Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
