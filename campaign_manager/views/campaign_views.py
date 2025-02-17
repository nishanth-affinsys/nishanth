from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from campaign_manager.services.campaign_views_utils import (
    campaign_notification_details_generic,
    target_users_by_run_id_generic,
    opted_in_out_details_generic,
    total_users_by_channel_generic,
    total_messages_per_channel_generic,
    total_converted_users_per_run_generic,
    campaign_user_reply_button_details_generic,
)
from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import (
    return_table,
)
from main.utils.export import export_csv, export_pdf


class CampaignViewSet(GenericViewSet):
    @extend_schema(
        operation_id="campaign_notification_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying full details of a campaign",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_notification_details")
    def campaign_notification_details(self, request, *args, **kwargs):
        """
        The campaign_notification_details function is used to pull the detailed broadcast message status for a campaign.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, with each dictionary containing the following keys:
        """

        response, _, _ = campaign_notification_details_generic(request)
        items = return_table(response, request)
        return items

    # Campaign pull broadcast
    @extend_schema(
        operation_id="campaign_notification_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for download full details of a campaign",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_notification_details_export_csv",
    )
    def campaign_notification_details_export(self, request, *args, **kwargs):
        """
        The campaign_notification_details_export function is used to export the campaign details in a csv file.
            The function takes request as an argument and returns the items.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        response, field_names, file_name = campaign_notification_details_generic(
            request
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_notification_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for download full details of a campaign",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_notification_details_export_pdf",
    )
    def campaign_notification_details_export_pdf(self, request, *args, **kwargs):
        """
        The campaign_notification_details_export_pdf function is used to export the campaign details in a pdf format.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The response
        :doc-author: Trelent
        """
        response, field_names, file_name = campaign_notification_details_generic(
            request
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Campaign Notification details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_target_users_by_run_id",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying targetted users for each run id",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_target_users_by_run_id")
    def target_users_by_run_id(self, request, *args, **kwargs):
        """
        The campaign_notification_details function is used to pull the detailed broadcast message status for a campaign.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, with each dictionary containing the following keys:
        """

        response, _, _ = target_users_by_run_id_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_target_users_by_run_id_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying targetted users for each run id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_target_users_by_run_id_export_csv",
    )
    def target_users_by_run_id_export_csv(self, request, *args, **kwargs):
        """
        The campaign_notification_details function is used to pull the detailed broadcast message status for a campaign.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, with each dictionary containing the following keys:
        """
        response, field_names, file_name = target_users_by_run_id_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_target_users_by_run_id_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying targetted users for each run id",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_target_users_by_run_id_export_pdf",
    )
    def target_users_by_run_id_export_pdf(self, request, *args, **kwargs):
        """
        The campaign_notification_details function is used to pull the detailed broadcast message status for a campaign.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, with each dictionary containing the following keys:
        """
        response, field_names, file_name = target_users_by_run_id_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Targeted Users by Run",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_total_marketing_users_by_channel",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_marketing_users_by_channel",
    )
    def total_marketing_users_by_channel(self, request, *args, **kwargs):
        response, _, _ = total_users_by_channel_generic(
            request, "Marketing", "MARKETING", "UTILITY"
        )
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_total_marketing_users_by_channel_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_marketing_users_by_channel_export_csv",
    )
    def total_marketing_users_by_channel_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = total_users_by_channel_generic(
            request, "Marketing", "MARKETING", "UTILITY"
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="campaign_total_marketing_users_by_channel_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_marketing_users_by_channel_export_pdf",
    )
    def total_marketing_users_by_channel_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = total_users_by_channel_generic(
            request, "Marketing", "MARKETING", "UTILITY"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Marketing Aggregate Users",
            request.user.username,
        )
        return items

        # for utility users

    @extend_schema(
        operation_id="campaign_total_utility_users_by_channel",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_utility_users_by_channel",
    )
    def total_utility_users_by_channel(self, request, *args, **kwargs):
        response, _, _ = total_users_by_channel_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        items = return_table(response, request)
        return items

        # for utility users

    @extend_schema(
        operation_id="campaign_total_utility_users_by_channel_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_utility_users_by_channel_export_csv",
    )
    def total_utility_users_by_channel_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = total_users_by_channel_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="campaign_total_utility_users_by_channel_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Counts the users there in campaign for different channels",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_utility_users_by_channel_export_pdf",
    )
    def total_utility_users_by_channel_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = total_users_by_channel_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Utility Aggregate Users",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_opted_in_out_details_marketing",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_marketing",
    )
    def opted_in_out_details_marketing(self, request, *args, **kwargs):
        """
        The opted_in_out_details function returns a table of all the channels that are opted in or out.
            The function takes in a request and uses it to get the current tenant name. It then queries
            ProfileDataChanneldata for all channel_id's, channel_name's, and is_opted values where the tenant is equal to
            the current tenant name. It then annotates each row with either &quot;Opted In&quot; or &quot;Opted Out&quot; depending on whether
            is_opted was true or false respectively.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The channel id, name and status of the user
        """
        response, _, _ = opted_in_out_details_generic(
            request, "Marketing", "MARKETING", "UTILITY"
        )
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_opted_in_out_details_marketing_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_marketing_export_csv",
    )
    def opted_in_out_details_marketing_export_csv(self, request, *args, **kwargs):
        """
        The opted_in_out_details_export_csv function is used to export the opted in/out details of a user.
            It takes request as an argument and returns a csv file containing the opted in/out details of a user.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to the function
        :return: A csv file with the following columns:

        """
        response, field_names, file_name = opted_in_out_details_generic(
            request, "Marketing", "MARKETING", "UTILITY"
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_opted_in_out_details_marketing_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_marketing_export_pdf",
    )
    def opted_in_out_details_marketing_export_pdf(self, request, *args, **kwargs):
        """
        The opted_in_out_details_export_pdf function is used to export the opted in or out details of a user.
            It takes request as an argument and returns items.
            The function uses the ProfileDataChanneldata model to get all the channel ids, channel names and status of a user from profile database.
            Then it calls export_pdf function which exports these data into pdf format.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = opted_in_out_details_generic(
            request,
            "Marketing",
            "MARKETING",
            "UTILITY",
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Marketing User Status details",
            request.user.username,
        )
        return items

    # utility campaign reports
    @extend_schema(
        operation_id="campaign_opted_in_out_details_utility",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_utility",
    )
    def opted_in_out_details_utility(self, request, *args, **kwargs):
        response, _, _ = opted_in_out_details_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_opted_in_out_details_utility_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_utility_export_csv",
    )
    def opted_in_out_details_utility_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = opted_in_out_details_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_opted_in_out_details_utility_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="details of the users that have opted out in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_opted_in_out_details_utility_export_pdf",
    )
    def opted_in_out_details_utility_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = opted_in_out_details_generic(
            request, "Utility", "UTILITY", "MARKETING"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Utility User Status details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_total_sent_messages_per_channel",
        tags=[AuthTags.AUTHORIZE],
        description="total number of messages sent in each channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_sent_messages_per_channel",
    )
    def total_sent_messages_per_channel(self, request, *args, **kwargs):
        response = total_messages_per_channel_generic(request, "sent")
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_total_delivered_messages_per_channel",
        tags=[AuthTags.AUTHORIZE],
        description="total number of messages delivered in each channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_delivered_messages_per_channel",
    )
    def total_delivered_messages_per_channel(self, request, *args, **kwargs):
        response = total_messages_per_channel_generic(request, "delivered")
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_total_read_messages_per_channel",
        tags=[AuthTags.AUTHORIZE],
        description="total number of messages read in each channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_total_read_messages_per_channel",
    )
    def total_read_messages_per_channel(self, request):
        response = total_messages_per_channel_generic(request, "read")
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_conversations",
        tags=[AuthTags.AUTHORIZE],
        description="total converted users in campaign",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_conversations",
    )
    def campaign_conversations(self, request):
        response = total_converted_users_per_run_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_call_to_action_details",
        tags=[AuthTags.AUTHORIZE],
        description="Displays details of the call to action button clicked by user",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_call_to_action_details",
    )
    def campaign_call_to_action_details(self, request):
        response, _, _ = campaign_user_reply_button_details_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_call_to_action_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays details of the call to action button clicked by user",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_call_to_action_details_export_csv",
    )
    def campaign_call_to_action_details_export_csv(self, request):
        response, field_names, file_name = campaign_user_reply_button_details_generic(
            request
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_call_to_action_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays details of the call to action button clicked by user",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_call_to_action_details_export_pdf",
    )
    def campaign_call_to_action_details_export_pdf(self, request):
        response, field_names, file_name = campaign_user_reply_button_details_generic(
            request
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "CTA Clicked Details",
            request.user.username,
        )
        return items

    # --------------------------------------old campaign manager---------------------------------------

    # @extend_schema(
    #     operation_id="pushbroadcast_completed_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of completed pushbroadcast campaigns",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pushbroadcast_completed_campaigns"
    # )
    # def pushbroadcast_completed_campaigns(self, request, *args, **kwargs):
    #     """
    #     The pushbroadcast_completed_campaigns function returns the number of completed campaigns.
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable-length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: A count of all completed campaigns
    #     """
    #     params = {
    #         "request": request,
    #         "models": CampaignsPushbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "completed": True,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "count": True,
    #     }
    #
    #     return get_generic_response(params)
    #
    # @extend_schema(
    #     operation_id="pullbroadcast_completed_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of completed pullbroadcast campaigns",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pullbroadcast_completed_campaigns"
    # )
    # def pullbroadcast_completed_campaigns(self, request, *args, **kwargs):
    #     """
    #     The pullbroadcast_completed_campaigns function is used to pull all completed campaigns from the database.
    #         It returns a count of the number of completed campaigns.
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Pass a non-keyworded, variable-length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The count of all the completed campaigns
    #     """
    #     now = timezone.now()
    #     params = {
    #         "request": request,
    #         "models": CampaignsPullbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "end_date__lte": now,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "values": {"campaign_variant_id"},
    #         "count": True,
    #     }
    #     return get_generic_response(params)
    #
    # @extend_schema(
    #     operation_id="total_completed_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of completed campaigns",
    # )
    # @action(methods=["POST"], detail=False, url_path="total_completed_campaigns")
    # def total_completed_campaigns(self, request, *args, **kwargs):
    #     """
    #     The total_completed_campaigns function returns the total number of completed campaigns.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Pass the request object to the function
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The total number of completed campaigns
    #     """
    #     now = timezone.now()
    #     params1 = {
    #         "request": request,
    #         "models": CampaignsPushbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "completed": True,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "query_set": True,
    #         "count": True,
    #     }
    #     params2 = {
    #         "request": request,
    #         "models": CampaignsPullbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "end_date__lte": now,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "values": {"campaign_variant_id"},
    #         "query_set": True,
    #         "count": True,
    #     }
    #     push_res = get_generic_response(params1)
    #     pull_res = get_generic_response(params2)
    #     add = push_res + pull_res
    #     return Response(data={"count": add})
    #
    # @extend_schema(
    #     operation_id="pushbroadcast_incomplete_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of incomplete pushbroadcast campaigns",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pushbroadcast_incomplete_campaigns"
    # )
    # def pushbroadcast_incomplete_campaigns(self, request, *args, **kwargs):
    #     """
    #     The pushbroadcast_incomplete_campaigns function returns the number of incomplete campaigns.
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Pass a non-keyworded, variable-length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of incomplete campaigns
    #     """
    #     params = {
    #         "request": request,
    #         "models": CampaignsPushbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "completed": False,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "count": True,
    #     }
    #     return get_generic_response(params)
    #
    # @extend_schema(
    #     operation_id="pushbroadcast_complete_incomplete",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying linechart of pushbroadcast completed and incompleted campaigns",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pushbroadcast_complete_incomplete"
    # )
    # def pushbroadcast_complete_incomplete(self, request, *args, **kwargs):
    #     """
    #     The pushbroadcast_complete_incomplete function is used to get the number of completed and incomplete campaigns for each day.
    #     The function takes in a request object, which contains information about the HTTP request that triggered this view.
    #     It also takes in *args and **kwargs arguments, which allow you to pass arbitrary arguments to a view function.
    #     This allows you to do things like construct dynamic URLs by passing additional parameters via the URLconf.
    #     The pushbroadcast_complete_incomplete function returns an HttpResponse object with an appropriate status code for the request.
    #
    #     :param self: Represent the instance of the object itself
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of completed and incomplete campaigns for each date
    #     """
    #     qs = query(
    #         request,
    #         CampaignsPushbroadcasttimeline,
    #         CampaignsPushtimeSerializer,
    #         db_schema="campaign",
    #     )
    #     qs1 = (
    #         qs.filter(
    #             campaign_variant__archived=False,
    #             campaign_variant__tenant=get_current_tenant_name(),
    #         )
    #         .values(Date=Cast("start_date", DateField()))
    #         .annotate(
    #             completed_Campaigns=Count(1, filter=Q(completed=True)),
    #             incomplete_Campaigns=Count(1, filter=Q(completed=False)),
    #         )
    #         .order_by("Date")
    #     )
    #     return Response(qs1)
    #
    # @extend_schema(
    #     operation_id="pullbroadcast_incomplete_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of incomplete pullbroadcast campaigns",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pullbroadcast_incomplete_campaigns"
    # )
    # def pullbroadcast_incomplete_campaigns(self, request, *args, **kwargs):
    #     """
    #     The pullbroadcast_incomplete_campaigns function is used to get the count of incomplete campaigns.
    #         ---
    #         # YAML (must be separated by `---`)
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Pass a non-keyworded, variable-length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of campaigns that are incomplete
    #     """
    #     now = timezone.now()
    #     params = {
    #         "request": request,
    #         "models": CampaignsPullbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "end_date__gte": now,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "values": {"campaign_variant_id"},
    #         "count": True,
    #     }
    #     return get_generic_response(params)
    #
    # @extend_schema(
    #     operation_id="total_incomplete_campaigns",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying total no of completed campaigns",
    # )
    # @action(methods=["POST"], detail=False, url_path="total_incomplete_campaigns")
    # def total_incomplete_campaigns(self, request, *args, **kwargs):
    #     """
    #     The total_incomplete_campaigns function returns the total number of incomplete campaigns.
    #         ---
    #         # YAML (must be separated by `---`)
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Pass a non-keyworded, variable-length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of incomplete campaigns
    #     """
    #     now = timezone.now()
    #     params1 = {
    #         "request": request,
    #         "models": CampaignsPushbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "completed": False,
    #             "campaign_variant__tenant": get_current_tenant_name(),
    #         },
    #         "query_set": True,
    #         "count": True,
    #     }
    #     params2 = {
    #         "request": request,
    #         "models": CampaignsPullbroadcasttimeline,
    #         "serializers": CampaignsPushtimeSerializer,
    #         "db_schema": "campaign",
    #         "filter_kwargs": {
    #             "campaign_variant__archived": False,
    #             "end_date__gte": now,
    #         },
    #         "values": {"campaign_variant_id"},
    #         "query_set": True,
    #         "count": True,
    #     }
    #     push_res = get_generic_response(params1)
    #     pull_res = get_generic_response(params2)
    #     add = push_res + pull_res
    #     return Response(data={"count": add})
    #
    # @extend_schema(
    #     operation_id="pullbroadcast_complete_incomplete",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying graph of Pull broadcast Line chart",
    # )
    # @action(
    #     methods=["POST"], detail=False, url_path="pullbroadcast_complete_incomplete"
    # )
    # def pullbroadcast_complete_incomplete(self, request, *args, **kwargs):
    #     """
    #     The pullbroadcast_complete_incomplete function is used to get the number of completed and incomplete campaigns for each day.
    #     The function takes in a request object, which contains information about the HTTP request that triggered this view.
    #     It also takes in *args and **kwargs, which are used to pass arbitrary arguments to a view function.
    #     This allows us to use the same API endpoint for different kinds of HTTP methods (GET/POST/PUT/DELETE).
    #     The pullbroadcast_complete_incomplete function returns an HttpResponse object with all of our data serialized as JSON.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: A list of dictionaries
    #     """
    #     now = timezone.now()
    #     qs = query(
    #         request,
    #         CampaignsPullbroadcasttimeline,
    #         CampaignsPushtimeSerializer,
    #         db_schema="campaign",
    #     )
    #     qs1 = (
    #         qs.filter(
    #             campaign_variant__archived=False,
    #             campaign_variant__tenant=get_current_tenant_name(),
    #         )
    #         .values(Date=Cast("start_date", DateField()))
    #         .annotate(
    #             completed_Campaigns=Count(
    #                 "campaign_variant_id", filter=Q(end_date__lte=now)
    #             ),
    #             incomplete_Campaigns=Count(
    #                 "campaign_variant_id", filter=Q(end_date__gte=now)
    #             ),
    #         )
    #         .order_by("Date")
    #     )
    #     return Response(qs1)
    #
    # @extend_schema(
    #     operation_id="active_campaign_details",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="active campaign details of pushbroadcast",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="active_campaign_details",
    # )
    # def active_campaign_details(self, request, *args, **kwargs):
    #     filter_data = request.data
    #     filter_data.update(**kwargs)
    #     qs = query(
    #         request, CampaignsCampaignvariant, CampaignVariantIdSerializer, "campaign"
    #     )
    #     qs1 = (
    #         qs.filter(
    #             tenant=get_current_tenant_name(),
    #             campaignscreativecontent__content_type="NOTIFICATION",
    #             status="ACTIVE",
    #         )
    #         .values(
    #             "id",
    #             "campaign__campaignscampaignvariant__name",
    #             "campaignscampaignvariantdetail__selected_users",
    #             "campaignspushbroadcasttimeline__recurrence_interval",
    #         )
    #         .annotate(
    #             total_channels_selected=Count(
    #                 "campaignscreativecontent__channel", distinct=True
    #             )
    #         )
    #     )
    #
    #     result = []
    #     for i in qs1:
    #         users_details = i["campaignscampaignvariantdetail__selected_users"]
    #         total_targeted_users = len(users_details)
    #         recurrence_interval = i.get(
    #             "campaignspushbroadcasttimeline__recurrence_interval"
    #         )
    #         if recurrence_interval > 0:
    #             recurrence = True
    #         else:
    #             recurrence = False
    #         data = {
    #             "Campaign_variant_id": i.get("id"),
    #             "Campaign_name": i.get("campaign__campaignscampaignvariant__name"),
    #             "Total_targeted_users": total_targeted_users,
    #             "Recurring": recurrence,
    #             "Total_selected_channels": i.get("total_channels_selected"),
    #         }
    #         result.append(data)
    #     items = return_table(result, request)
    #     return items
    #
    # @extend_schema(
    #     operation_id="active_campaign_details_export_csv",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="active campaign details of pushbroadcast in csv",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="active_campaign_details_export_csv",
    # )
    # def active_campaign_details_export_csv(self, request, *args, **kwargs):
    #     filter_data = request.data
    #     filter_data.update(**kwargs)
    #     qs = query(
    #         request, CampaignsCampaignvariant, CampaignVariantIdSerializer, "campaign"
    #     )
    #     qs1 = (
    #         qs.filter(
    #             tenant=get_current_tenant_name(),
    #             campaignscreativecontent__content_type="NOTIFICATION",
    #             status="ACTIVE",
    #         )
    #         .values(
    #             "id",
    #             "campaign__campaignscampaignvariant__name",
    #             "campaignscampaignvariantdetail__selected_users",
    #             "campaignspushbroadcasttimeline__recurrence_interval",
    #         )
    #         .annotate(
    #             total_channels_selected=Count(
    #                 "campaignscreativecontent__channel", distinct=True
    #             )
    #         )
    #     )
    #
    #     result = []
    #     for i in qs1:
    #         users_details = i["campaignscampaignvariantdetail__selected_users"]
    #         total_targeted_users = len(users_details)
    #         recurrence_interval = i.get(
    #             "campaignspushbroadcasttimeline__recurrence_interval"
    #         )
    #         if recurrence_interval > 0:
    #             recurrence = True
    #         else:
    #             recurrence = False
    #         data = {
    #             "Campaign_variant_id": i.get("id"),
    #             "Campaign_name": i.get("campaign__campaignscampaignvariant__name"),
    #             "Total_targeted_users": total_targeted_users,
    #             "Recurring": recurrence,
    #             "Total_selected_channels": i.get("total_channels_selected"),
    #         }
    #         result.append(data)
    #     items = export_csv(
    #         result,
    #         [
    #             "Campaign_variant_id",
    #             "Campaign_name",
    #             "Total_targeted_users",
    #             "Recurring",
    #             "Total_selected_channels",
    #         ],
    #         "active_campaign_details.csv",
    #     )
    #     return items
    #
    # @extend_schema(
    #     operation_id="active_campaign_details_export_pdf",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="active campaign details of pushbroadcast in pdf",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="active_campaign_details_export_pdf",
    # )
    # def active_campaign_details_export_pdf(self, request, *args, **kwargs):
    #     filter_data = request.data
    #     filter_data.update(**kwargs)
    #     qs = query(
    #         request, CampaignsCampaignvariant, CampaignVariantIdSerializer, "campaign"
    #     )
    #     qs1 = (
    #         qs.filter(
    #             tenant=get_current_tenant_name(),
    #             campaignscreativecontent__content_type="NOTIFICATION",
    #             status="ACTIVE",
    #         )
    #         .values(
    #             "id",
    #             "campaign__campaignscampaignvariant__name",
    #             "campaignscampaignvariantdetail__selected_users",
    #             "campaignspushbroadcasttimeline__recurrence_interval",
    #         )
    #         .annotate(
    #             total_channels_selected=Count(
    #                 "campaignscreativecontent__channel", distinct=True
    #             )
    #         )
    #     )
    #
    #     result = []
    #     for i in qs1:
    #         users_details = i["campaignscampaignvariantdetail__selected_users"]
    #         total_targeted_users = len(users_details)
    #         recurrence_interval = i.get(
    #             "campaignspushbroadcasttimeline__recurrence_interval"
    #         )
    #         if recurrence_interval > 0:
    #             recurrence = True
    #         else:
    #             recurrence = False
    #         data = {
    #             "Campaign_variant_id": i.get("id"),
    #             "Campaign_name": i.get("campaign__campaignscampaignvariant__name"),
    #             "Total_targeted_users": total_targeted_users,
    #             "Recurring": recurrence,
    #             "Total_selected_channels": i.get("total_channels_selected"),
    #         }
    #         result.append(data)
    #     items = export_pdf(
    #         result,
    #         [
    #             "Campaign_variant_id",
    #             "Campaign_name",
    #             "Total_targeted_users",
    #             "Recurring",
    #             "Total_selected_channels",
    #         ],
    #         "active_campaign_details.pdf",
    #         "Active Campaign Details",
    #     )
    #     return items
    #
    # @extend_schema(
    #     operation_id="channelwise_count_campaign_user",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Counts the users from different channels who selected the campaigns",
    # )
    # @action(methods=["POST"], detail=False, url_path="channelwise_count_campaign_user")
    # def channelwise_count_campaign_user(self, request, *args, **kwargs):
    #     """
    #     The channelwise_count_campaign_user function returns a table of campaign variant id, campaign name,
    #     whatsapp count, facebook count and email count for each campaign variant. The whatsapp_count is the number of users
    #     who have been selected to receive the message via whatsapp. Similarly for facebook and email.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of users selected for a campaign variant
    #     """
    #     response = channelwise_count_campaign_user_generic(request)
    #     return return_table(response, request)
    #
    # @extend_schema(
    #     operation_id="channelwise_count_campaign_user_export",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Counts the users from different channels who selected the campaigns in csv",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="channelwise_count_campaign_user_export",
    # )
    # def channelwise_count_campaign_user_export(self, request, *args, **kwargs):
    #     """
    #     The channelwise_count_campaign_user_export function is used to export the user count of a campaign variant.
    #     The function takes in a request object and returns an exported CSV file containing the following fields:
    #     campaign_variant_id, campaign_name, whatsapp, facebook and email.
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object from the view
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The count of users for each channel in a campaign
    #     """
    #     response, field_names, file_name = channelwise_count_campaign_user_generic(
    #         request
    #     )
    #     items = export_csv(response, field_names, f"{file_name}.csv")
    #     return items
    #
    # @extend_schema(
    #     operation_id="channelwise_count_campaign_user_export_pdf",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Counts the users from different channels who selected the campaigns in pdf",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="channelwise_count_campaign_user_export_pdf",
    # )
    # def channelwise_count_campaign_user_export_pdf(self, request, *args, **kwargs):
    #     """
    #     The channelwise_count_campaign_user_export_pdf function is used to export the number of users in a campaign variant
    #     by channel (email, whatsapp, facebook) as a PDF file. The function takes in the request object and returns an HTTP
    #     response containing the PDF file.
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The pdf file of the channelwise count of users
    #     """
    #     response, field_names, file_name = channelwise_count_campaign_user_generic(
    #         request
    #     )
    #     if len(response) > MAX_PDF_LIMIT:
    #         response = response[:MAX_PDF_LIMIT]
    #     items = export_pdf(response, field_names, f"{file_name}.pdf", "User Counts")
    #     return items
    #
    # @extend_schema(
    #     operation_id="total_targeted_users",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="big number of the total targeted users",
    # )
    # @action(
    #     methods=["POST"],
    #     detail=False,
    #     url_path="total_targeted_users",
    # )
    # def total_targeted_users(self, request, *args, **kwargs):
    #     filter_data = request.data
    #     filter_data.update(**kwargs)
    #     qs1 = (
    #         CampaignsCampaignvariantdetail.objects.using("campaign")
    #         .filter(
    #             campaign_variant__tenant=get_current_tenant_name(),
    #             timestamp__range=filter_data.get("timestamp__range"),
    #             campaign_variant_id__in=filter_data.get("campaign_variants"),
    #         )
    #         .filter(
    #             campaign_variant__campaignscreativecontent__content_type="NOTIFICATION"
    #         )
    #         .values("campaign_variant_id", "campaign_variant__name", "selected_users")
    #     )
    #
    #     count = sum(len(i["selected_users"]) for i in qs1)
    #     return Response(data={"count": count})
