from __future__ import annotations
from auth.tags import AuthTags
from django.conf import settings

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from console.services.user_behaviour_utils import (
    top_10_message_generic,
    top_10_intents_generic,
    message_wordcloud_generic,
    channels_reaction_generic,
)
from main.utils.boiler_plate import get_generic_response, return_table, query
from main.utils.export import export_csv, export_pdf


class UserBehaviourChartsViewSet(GenericViewSet):  # for all BOT Report
    # Top Messages to BOT
    @extend_schema(
        operation_id="bot_user_top_ten_messages",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Messages to BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_user_top_ten_messages")
    def top_10_message(self, request, *args, **kwargs):
        """
        The top_10_message function returns the top 10 messages sent by users to a bot.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The top 10 messages that the user has sent to the bot
        """
        items, _, _ = top_10_message_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_user_top_ten_messages_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Messages to BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_top_ten_messages_export_csv"
    )
    def top_ten_message_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = top_10_message_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_user_top_ten_messages_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Messages to BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_top_ten_messages_export_pdf"
    )
    def top_ten_message_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = top_10_message_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Top 10 Messages",
            request.user.username,
        )
        return items

    # Top Intents of BOT
    @extend_schema(
        operation_id="bot_user_top_ten_intents",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Intents to BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_user_top_ten_intents")
    def top_10_intents(self, request, *args, **kwargs):
        """
        The total_10_intents function returns the top 10 intents that have been used by users.
            ---
            parameters:
                - name: request_type
                  description: The type of request being made (GET, POST, PUT, DELETE)
                  required: true

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The top 10 intents from the database
        """
        items, _, _ = top_10_intents_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_user_top_ten_intents_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Intents to BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_top_ten_intents_export_csv"
    )
    def top_ten_intents_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = top_10_intents_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_user_top_ten_intents_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top Intents to BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_top_ten_intents_export_pdf"
    )
    def top_ten_intents_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = top_10_intents_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Top 10 Intents",
            request.user.username,
        )
        return items

    # Word Cloud
    @extend_schema(
        operation_id="bot_user_messages_wordcloud",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying WordCloud",
    )
    @action(methods=["POST"], detail=False, url_path="bot_user_messages_wordcloud")
    def message_wordcloud(self, request, *args, **kwargs):
        """
        The top_10_message_wordCloud function is used to generate a word cloud of the top 10 most frequently used words in user messages.
        The function takes in a request object and returns a response object containing the data for generating the word cloud.


        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The top 10 messages sent by the users to the bot
        """
        items = message_wordcloud_generic(request)
        return Response(items)

    # @extend_schema(
    #     operation_id="channels_reaction",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying the reaction messages of the user to a particular post",
    # )
    # @action(methods=["POST"], detail=False, url_path="channels_reaction")
    # def channels_reaction(self, request, *args, **kwargs):
    #     params = channels_reaction_generic(request)
    #     return get_generic_response(params)

    # @extend_schema(
    #     operation_id="channels_reaction_export_csv",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying the reaction messages of the user to a particular post in csv",
    # )
    # @action(methods=["POST"], detail=False, url_path="channels_reaction_export_csv")
    # def channels_reaction_export_csv(self, request, *args, **kwargs):
    #     params = channels_reaction_generic(
    #         request,
    #         key="csv_kwargs",
    #         value={
    #             "fieldNames": [
    #                 "Username",
    #                 "Page_Id",
    #                 "Post_Id",
    #                 "Action_Type",
    #                 "Remarks",
    #                 "Timestamp",
    #             ],
    #             "fileName": "channels_reactions.csv",
    #         },
    #     )
    #     return get_generic_response(params)

    # @extend_schema(
    #     operation_id="channels_reaction_export_pdf",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying the reaction messages of the user to a particular post in pdf",
    # )
    # @action(methods=["POST"], detail=False, url_path="channels_reaction_export_pdf")
    # def channels_reaction_export_pdf(self, request, *args, **kwargs):
    #     params = channels_reaction_generic(
    #         request,
    #         key="pdf_kwargs",
    #         value={
    #             "fieldNames": [
    #                 "Username",
    #                 "Page_Id",
    #                 "Post_Id",
    #                 "Action_Type",
    #                 "Remarks",
    #                 "Timestamp",
    #             ],
    #             "fileName": "channels_reactions.pdf",
    #             "title": "User Actions",
    #              "user":request.user.username
    #         },
    #     )
    #     return get_generic_response(params)

    @extend_schema(
        operation_id="bot_user_channels_reaction",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the reaction messages of the user to a particular post",
    )
    @action(methods=["POST"], detail=False, url_path="bot_user_channels_reaction")
    def channels_reaction(self, request, *args, **kwargs):
        params = channels_reaction_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_user_channels_reaction_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the reaction messages of the user to a particular post in csv",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_channels_reaction_export_csv"
    )
    def channels_reaction_export_csv(self, request, *args, **kwargs):
        params = channels_reaction_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Username",
                    "User_Id",
                    "Page_Id",
                    "Post_Id",
                    "Action_Type",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "user_actions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_user_channels_reaction_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the reaction messages of the user to a particular post in pdf",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_user_channels_reaction_export_pdf"
    )
    def channels_reaction_export_pdf(self, request, *args, **kwargs):
        params = channels_reaction_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Username",
                    "User_Id",
                    "Page_Id",
                    "Post_Id",
                    "Action_Type",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "user_actions.pdf",
                "title": "User Actions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_user_channels_reaction_export_excel",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the reaction messages of the user to a particular post in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_user_channels_reaction_export_excel",
    )
    def bot_user_channels_reaction_export_excel(self, request, *args, **kwargs):
        params = channels_reaction_generic(
            request,
            key="excel_kwargs",
            value={"timestamp_keys": ["Timestamp"], "fileName": "user_actions.xlsx"},
        )
        return get_generic_response(params)
