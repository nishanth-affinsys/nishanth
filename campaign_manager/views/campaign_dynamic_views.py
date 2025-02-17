from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from campaign_manager.services.campaign_dynamic_utils import (
    rolled_campaigns_bignum_generic,
    rolled_campaigns_details,
    campaign_cta_clicked_count,
    campaign_cta_clicked_details,
    campaign_targeted_users_count,
    campaign_targeted_users_generic,
    campaign_dynamic_campaign_aggregate_generic,
)

from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import get_generic_response, return_table
from main.utils.export import export_csv, export_pdf


class CampaignDynamicDashboardViewSet(GenericViewSet):
    @extend_schema(
        operation_id="campaign_rolled_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Rolled campaign - BigNumber",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_rolled_bigNum")
    def campaign_rolled_bigNum(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is not paginated, and it returns a count of the number of variants for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = rolled_campaigns_bignum_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaign_rolled_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Rolled campaign- Details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_rolled_details")
    def campaign_rolled_details(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = rolled_campaigns_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaign_rolled_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Rolled campaign- Details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_rolled_details_export_csv"
    )
    def campaign_rolled_details_export_csv(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = rolled_campaigns_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "campaign_id",
                    "campaign_name",
                    "subcampaign_id",
                    "subcampaign_name",
                    "run_id",
                    "Timestamp",
                ],
                "fileName": "Dynamic_Campaign_Rolled.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaign_rolled_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Rolled campaign- Details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_rolled_details_export_pdf"
    )
    def campaign_rolled_details_export_pdf(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = rolled_campaigns_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "campaign_id",
                    "campaign_name",
                    "subcampaign_id",
                    "subcampaign_name",
                    "run_id",
                    "Timestamp",
                ],
                "fileName": "Dynamic_Campaign_Rolled.pdf",
                "title": "Dynamic Campaign Rolled Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaign_cta_clicked_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - BigNum",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_cta_clicked_bigNum")
    def campaign_cta_clicked_bigNum(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response = campaign_cta_clicked_count(request)
        return get_generic_response(response)

    @extend_schema(
        operation_id="campaign_cta_clicked",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - Details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_cta_clicked")
    def campaign_cta_clicked(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, _, _ = campaign_cta_clicked_details(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="campaign_cta_clicked_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - Details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_cta_clicked_export_csv")
    def campaign_cta_clicked_export_csv(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_cta_clicked_details(request)
        items = export_csv(response, fieldNames, fileName)
        return items

    @extend_schema(
        operation_id="campaign_cta_clicked_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - Details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_cta_clicked_export_pdf")
    def campaign_cta_clicked_export_pdf(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_cta_clicked_details(request)
        items = export_pdf(
            response,
            fieldNames,
            fileName,
            "Campaign CTA Clicked Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_targeted_users_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - Details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_targeted_users_bigNum")
    def campaign_targeted_users_Num(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response = campaign_targeted_users_count(request)
        return get_generic_response(response)

    @extend_schema(
        operation_id="campaign_targeted_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total CTA Clicked - BigNum",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_targeted_users")
    def campaign_targeted_users(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, _, _ = campaign_targeted_users_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="campaign_targeted_users_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Targeted Users - Details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_targeted_users_export_csv"
    )
    def campaign_targeted_users_export_csv(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_targeted_users_generic(request)
        items = export_csv(response, fieldNames, fileName)
        return items

    @extend_schema(
        operation_id="campaign_targeted_users_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Targeted Users - Details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_targeted_users_export_pdf"
    )
    def campaign_targeted_users_export_pdf(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_targeted_users_generic(request)
        items = export_pdf(
            response,
            fieldNames,
            fileName,
            "Campaign Targeted Users",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_dynamic_campaign_aggregate",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying aggregate analysis of dynamic campaign",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_dynamic_campaign_aggregate"
    )
    def campaign_dynamic_campaign_aggregate(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, _, _ = campaign_dynamic_campaign_aggregate_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="campaign_dynamic_campaign_aggregate_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying aggregate analysis of dynamic campaign",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_dynamic_campaign_aggregate_export_csv",
    )
    def campaign_dynamic_campaign_aggregate_export_csv(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_dynamic_campaign_aggregate_generic(
            request
        )
        return export_csv(response, fieldNames, fileName)

    @extend_schema(
        operation_id="campaign_dynamic_campaign_aggregate_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying aggregate analysis of dynamic campaign",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_dynamic_campaign_aggregate_export_pdf",
    )
    def campaign_dynamic_campaign_aggregate_export_pdf(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns Rolled by the current tenant.
        The function is paginated, and it returns the details for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, fieldNames, fileName = campaign_dynamic_campaign_aggregate_generic(
            request
        )
        return export_pdf(
            response,
            fieldNames,
            fileName,
            "Aggregate Dynamic Campaign Details",
            request.user.username,
        )
