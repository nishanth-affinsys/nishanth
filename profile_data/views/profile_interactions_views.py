from auth.tags import AuthTags

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from main.utils.boiler_plate import (
    get_generic_response,
)
from profile_data.services.profile_interactions_utils import (
    user_interactions_by_service,
    interactions_by_service,
    profile_hourly_interactions_by_service,
    profile_bot_interactions,
    profile_handoff_interactions,
    profile_complaint_category,
    profile_complaint_category_interactions_details,
    profile_complaints_remarks_wordcloud,
    profile_complaints_channel_interactions,
    interaction_daily_heatmap,
    complaints_srn_category_interactions,
    top10_profiles_interactions,
)
from drf_spectacular.utils import extend_schema


class ProfileInteractionsViewSet(GenericViewSet):
    @extend_schema(
        operation_id="profile_interactions_by_service_and_user",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_by_service_and_user",
    )
    def profile_interactions_by_service_and_user(self, request, *args, **kwargs):
        params = user_interactions_by_service(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_by_service_and_user_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_by_service_and_user_export_csv",
    )
    def profile_interactions_by_service_and_user_export_csv(
        self, request, *args, **kwargs
    ):
        params = user_interactions_by_service(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Customer_Id",
                    "Username",
                    "Date",
                    "Bot",
                    "Handoff",
                    "Complaint",
                ],
                "fileName": "user_interaction_summary",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_by_service_and_user_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_by_service_and_user_export_pdf",
    )
    def profile_interactions_by_service_and_user_export_pdf(
        self, request, *args, **kwargs
    ):
        params = user_interactions_by_service(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Customer_Id",
                    "Username",
                    "Date",
                    "Bot",
                    "Handoff",
                    "Complaint",
                ],
                "fileName": "user_interaction_summary",
                "title": "User Interaction Summary",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_by_service",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(methods=["POST"], detail=False, url_path="profile_interactions_by_service")
    def profile_interactions_by_service(self, request, *args, **kwargs):
        params = interactions_by_service(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_hourly_by_services",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_hourly_by_services",
    )
    def profile_interactions_hourly_by_services(self, request, *args, **kwargs):
        params = profile_hourly_interactions_by_service(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_bot_by_channel",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"], detail=False, url_path="profile_interactions_bot_by_channel"
    )
    def profile_interactions_bot_by_channel(self, request, *args, **kwargs):
        params = profile_bot_interactions(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_handoff",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(methods=["POST"], detail=False, url_path="profile_interactions_handoff")
    def profile_interactions_handoff(self, request, *args, **kwargs):
        params = profile_handoff_interactions(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_handoff_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_handoff_export_csv",
    )
    def profile_interactions_handoff_export_csv(self, request, *args, **kwargs):
        params = profile_handoff_interactions(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Agent_Name",
                    "Customer_Id",
                    "Interactions",
                ],
                "fileName": "profile_handoff_interactions",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_handoff_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in handoff service as pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_handoff_export_pdf",
    )
    def profile_interactions_handoff_export_pdf(self, request, *args, **kwargs):
        params = profile_handoff_interactions(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Agent_Name",
                    "Customer_Id",
                    "Interactions",
                ],
                "fileName": "profile_handoff_interactions",
                "title": "Handoff Interactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_category",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_category",
    )
    def profile_interactions_complaints_category(self, request, *args, **kwargs):
        params = profile_complaint_category(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_category_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_category_details",
    )
    def profile_interactions_complaints_category_details(
        self, request, *args, **kwargs
    ):
        params = profile_complaint_category_interactions_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_category_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_category_details_export_csv",
    )
    def profile_interactions_complaints_category_details_export_csv(
        self, request, *args, **kwargs
    ):
        params = profile_complaint_category_interactions_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Username",
                    "Category",
                    "Interactions",
                ],
                "fileName": "profile_complaint_interactions_by_category",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_category_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in handoff service as pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_category_details_export_pdf",
    )
    def profile_interactions_complaints_category_details_export_pdf(
        self, request, *args, **kwargs
    ):
        params = profile_complaint_category_interactions_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Profile_Id",
                    "Username",
                    "Category",
                    "Interactions",
                ],
                "fileName": "profile_complaint_interactions_by_category",
                "title": "Complaint Interactions by Category",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_remarks_wordcloud",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_remarks_wordcloud",
    )
    def profile_interactions_complaints_remarks_wordcloud(
        self, request, *args, **kwargs
    ):
        params = profile_complaints_remarks_wordcloud(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_complaints_channel",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in services for every profile id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_complaints_channel",
    )
    def profile_interactions_complaints_channel(self, request, *args, **kwargs):
        params = profile_complaints_channel_interactions(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="profile_interactions_daily_heatmap",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in  all services for each day",
    )
    @action(
        methods=["POST"], detail=False, url_path="profile_interactions_daily_heatmap"
    )
    def profile_interactions_daily_heatmap(self, request, *args, **kwargs):
        response = interaction_daily_heatmap(request)
        return Response(response)

    @extend_schema(
        operation_id="profile_interactions_srn_category_interactions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the interactions in complaints for every srn",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_srn_category_interactions",
    )
    def profile_interactions_srn_category_interactions(self, request, *args, **kwargs):
        response = complaints_srn_category_interactions(request)
        return get_generic_response(response)

    @extend_schema(
        operation_id="profile_interactions_top_ten_profile_ids",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the top 10 profile ids",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="profile_interactions_top_ten_profile_ids",
    )
    def profile_interactions_top_ten_profile_ids(self, request, *args, **kwargs):
        response = top10_profiles_interactions(request)
        return Response(response)
