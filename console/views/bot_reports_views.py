from __future__ import annotations
from auth.tags import AuthTags

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from console.serializers import BotReportSerializer
from console.services.bot_report_utils import (
    messages_faq_generic,
    total_message_generic,
    top_intents_generic,
    top_messages_generic,
    total_matched_intents_generic,
    total_unmatched_intents_generic,
    total_active_customers_generic,
    number_of_users_interactions_generic,
    average_session_time_generic,
    average_message_generic,
    new_user_in_bot_generic,
    conversation_generic,
    returning_user_in_bot_generic,
    user_flow_shankey_chart_generic,
    user_messages_heatmap_generic,
    top_ten_matched_intents_by_channel_generic,
)
from django.conf import settings
from main.utils.export import export_csv, export_pdf
from main.utils.boiler_plate import (
    get_generic_response,
    return_table,
)

from drf_spectacular.utils import extend_schema

import logging

logger = logging.getLogger(__name__)


class BotChartsViewSet(GenericViewSet):  # for all BOT Report
    serializer_class = BotReportSerializer

    # Number of messages coming to BOT
    @extend_schema(
        operation_id="bot_no_of_msgs_coming_to_bot",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of the messages channelwise",
    )
    @action(methods=["POST"], detail=False, url_path="bot_no_of_msgs_coming_to_bot")
    def messages_faq(self, request, *args, **kwargs):
        """
         The messages_faq function is a custom function that returns the number of messages sent by users to each channel.
         It uses the query function from utils.py, which takes in a request object and returns an appropriate queryset based on
         the parameters passed in through the request object (e.g., filters, ordering). The result variable is then assigned to
         a list of dictionaries containing information about each message log entry that matches our criteria: it must be from a user,
        , and it must belong to this tenant's database schema (i.e., event). We

         :param self: Represent the instance of the class
         :param request: Get the request object
         :param *args: Send a non-keyworded variable length argument list to the function
         :param **kwargs: Pass keyworded, variable-length argument list to a function
         :return: A list of dictionaries, where each dictionary contains the channel and count for each message
        """

        items, _, _ = messages_faq_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_no_of_msgs_coming_to_bot_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of the messages channelwise",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_no_of_msgs_coming_to_bot_export_csv",
    )
    def faq_messages_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = messages_faq_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_no_of_msgs_coming_to_bot_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total count of the messages channelwise",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_no_of_msgs_coming_to_bot_export_pdf",
    )
    def faq_messages_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = messages_faq_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Messages by Channel",
            request.user.username,
        )
        return items

    # Total Messages of BOT
    @extend_schema(
        operation_id="bot_total_messages_by_session",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying  Total messages to the BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_total_messages_by_session")
    def total_message(self, request, *args, **kwargs):
        """
        The total_message function is a generic function that returns the total number of messages sent by users.
        It takes in request, *args and **kwargs as parameters. It then creates a dictionary called params which contains
        the following keys: &quot;request&quot;, &quot;models&quot;, &quot;serializers&quot;, &quot;db_schema&quot;,
        &quot;filter_kwargs&quot;,&quot;filter_args&quot;,&quot;values&quot;,&quot;annotate&quot; and order_by&quot;. The values for these keys are as follows:
        request = request, models = MessageLog, serializers = BotReportSerializer, db_schema=&quot;event&quot;. filter kwargss= {&quot;source&quot;: user

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of messages sent by the user
        """
        items, _, _ = total_message_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_total_messages_by_session_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying  Total messages to the BOT",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_total_messages_by_session_export_csv",
    )
    def total_messages_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = total_message_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_total_messages_by_session_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying  Total messages to the BOT",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_total_messages_by_session_export_pdf",
    )
    def total_messages_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = total_message_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Messages by Session",
            request.user.username,
        )
        return items

    # Top Intents to BOT
    @extend_schema(
        operation_id="bot_top_matched_intents",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top matchedintents triggered",
    )
    @action(methods=["POST"], detail=False, url_path="bot_top_matched_intents")
    def top_intents(self, request, *args, **kwargs):
        """
        The top_intents function returns a list of the top intents that users have
            interacted with.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The top intents for the bot
        """
        items, _, _ = top_intents_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_top_matched_intents_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top intents triggered",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_top_matched_intents_export_csv"
    )
    def top_intent_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = top_intents_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_top_matched_intents_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top matched intents triggered",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_top_matched_intents_export_pdf"
    )
    def top_intent_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = top_intents_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Top Matched Intents",
            request.user.username,
        )
        return items

    # Top Messages to BOT
    @extend_schema(
        operation_id="bot_top_messages",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Highest count of the messages appeared",
    )
    @action(methods=["POST"], detail=False, url_path="bot_top_messages")
    def top_messages(self, request, *args, **kwargs):
        """
        The top_messages function returns the top messages sent by users to the bot.
            ---
            parameters:
                - name: start_date
                  description: The start date for filtering data. Format is YYYY-MM-DD HH24:MI (e.g., 2020-01-01 00:00) or YYYY/MM/DD HH24/MI (e.g., 2020/01/01 00). If no time is specified, it defaults to midnight of that day in UTC timezone (i.e., 00 hours and 00 minutes). This parameter is optional and if not provided, will default

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The top messages sent by the users
        """
        items, _, _ = top_messages_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_top_messages_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Highest count of the messages appeared",
    )
    @action(methods=["POST"], detail=False, url_path="bot_top_messages_export_csv")
    def top_messages_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = top_messages_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_top_messages_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Highest count of the messages appeared",
    )
    @action(methods=["POST"], detail=False, url_path="bot_top_messages_export_pdf")
    def top_messages_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = top_messages_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Top Messages",
            request.user.username,
        )
        return items

    # Total Matched Intents
    @extend_schema(
        operation_id="bot_total_matched_intents",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Matched Intents",
    )
    @action(methods=["POST"], detail=False, url_path="bot_total_matched_intents")
    def total_matched_intents(self, request, *args, **kwargs):
        """
        The total_matched_intents function returns the total number of matched intents for a given tenant.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of matched intents
        """
        params = total_matched_intents_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_total_matched_intents_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Matched Intents",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_total_matched_intents_export_csv"
    )
    def total_intents_matched_export_csv(self, request, *args, **kwargs):
        params = total_matched_intents_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel", "Count"],
                "fileName": "total_matched_intents.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_total_matched_intents_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Matched Intents",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_total_matched_intents_export_pdf"
    )
    def total_intents_matched_export_pdf(self, request, *args, **kwargs):
        params = total_matched_intents_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel", "Count"],
                "fileName": "total_matched_intents.pdf",
                "title": "Total Matched Intents",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Total UnMatched Intents
    @extend_schema(
        operation_id="bot_total_unmatched_intents",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Unmatched Intents",
    )
    @action(methods=["POST"], detail=False, url_path="bot_total_unmatched_intents")
    def total_unmatched_intents(self, request, *args, **kwargs):
        """
        The total_unmatched_intents function returns the total number of unmatched intents.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of unmatched intents
        """
        params = total_unmatched_intents_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_total_unmatched_intents_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Unmatched Intents",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_total_unmatched_intents_export_csv",
    )
    def total_intents_unmatched_export_csv(self, request, *args, **kwargs):
        params = total_unmatched_intents_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel", "Count"],
                "fileName": "total_unmatched_intents.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_total_unmatched_intents_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Unmatched Intents",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_total_unmatched_intents_export_pdf",
    )
    def total_intents_unmatched_export_pdf(self, request, *args, **kwargs):
        params = total_unmatched_intents_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel", "Count"],
                "fileName": "total_unmatched_intents.pdf",
                "title": "Total Unmatched Intents",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Total Active Customers
    @extend_schema(
        operation_id="bot_active_customers",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total active customers by channel",
    )
    @action(methods=["POST"], detail=False, url_path="bot_active_customers")
    def total_active_customers(self, request, *args, **kwargs):
        """
        The total_active_customers function returns the total number of active customers for a given time period.

        :param self: Represent the instance of the object itself
        :param request: Pass the request object to the function
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of active customers on a given day
        """
        items, _, _ = total_active_customers_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_active_customers_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total active customers by channel",
    )
    @action(methods=["POST"], detail=False, url_path="bot_active_customers_export_csv")
    def active_customers_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = total_active_customers_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_active_customers_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total active customers by channel",
    )
    @action(methods=["POST"], detail=False, url_path="bot_active_customers_export_pdf")
    def active_customers_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = total_active_customers_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Active Customers",
            request.user.username,
        )
        return items

    # Number of Users Interactions
    @extend_schema(
        operation_id="bot_no_of_user_sessions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Interacted Users",
    )
    @action(methods=["POST"], detail=False, url_path="bot_no_of_user_sessions")
    def number_of_users_interactions(self, request, *args, **kwargs):
        """
        The Number_of_Users_Interactions function returns the number of users who have interacted with a bot.
            This function is called by the Number_of_Users_Interactions endpoint in views.py, which is accessed via
            /api/v2/analytics/number-of-users-interactions/.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of users that have interacted with the bot
        """
        items, _, _ = number_of_users_interactions_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_no_of_user_sessions_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Interacted Users",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_no_of_user_sessions_export_csv"
    )
    def user_interactions_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = number_of_users_interactions_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_no_of_user_sessions_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Interacted Users",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_no_of_user_sessions_export_pdf"
    )
    def user_interactions_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = number_of_users_interactions_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Number of User Sessions",
            request.user.username,
        )
        return items

    # Average Session Tome in seconds
    @extend_schema(
        operation_id="bot_average_session_time",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average Session Time with the BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_average_session_time")
    def average_session_time(self, request, *args, **kwargs):
        """
        The average_session_time function takes in a request and kwargs, which are used to filter the queryset.
        The function then filters the MessageLog model by timestamp range, channel, tenant name (current), source (user), and message content.
        It then groups by session_id and channel while annotating with max time of each session_id group as well as min time of each session_id group.
        It also calculates difference between max time and min time for each session id group. The queryset is ordered by nothing so that it can be sorted later on in the function using key=itemgetter('channel').

        :param self: Represent the instance of the class
        :param request: Get the data from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average session time for each channel
        """
        items, _, _ = average_session_time_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_average_session_time_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average Session Time with the BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_average_session_time_export_csv"
    )
    def average_session_time_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = average_session_time_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_average_session_time_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average Session Time with the BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_average_session_time_export_pdf"
    )
    def average_session_time_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = average_session_time_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Average Session Time",
            request.user.username,
        )
        return items

    # Average Messages per session
    @extend_schema(
        operation_id="bot_avg_msgs_per_session",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average message count received by the BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_avg_msgs_per_session")
    def average_message(self, request, *args, **kwargs):
        """
        The average_message function returns the average number of messages per session.
            It takes in a request object and returns a Response object with the data field containing
            an integer representing the average number of messages per session.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The average number of messages per session
        """
        items, _, _ = average_message_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_avg_msgs_per_session_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average message count received by the BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_avg_msgs_per_session_export_csv"
    )
    def average_message_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = average_message_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_avg_msgs_per_session_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Average message count received by the BOT",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_avg_msgs_per_session_export_pdf"
    )
    def average_message_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = average_message_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Average Messages per Session",
            request.user.username,
        )
        return items

    # New users coming to BOT in the given time interval
    @extend_schema(
        operation_id="bot_new_user",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying New User to the BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_new_user")
    def new_user_in_bot(self, request, *args, **kwargs):  # This is created with view
        """
        The new_user_in_bot function is used to return a list of new users in the bot.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        result, _, _ = new_user_in_bot_generic(request)
        return return_table(result, request)

    # New User in BOT chart Export csv format
    @extend_schema(
        operation_id="bot_new_user_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying New User to the BOT csv export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_new_user_export_csv")
    def new_user_in_bot_export(self, request, *args, **kwargs):
        """
        The new_user_in_bot_export function is used to export a CSV file containing the following information:
            - Customer ID
            - Channel Name (e.g. Facebook, WhatsApp)
            - Time of first interaction with bot

        :param self: Represent the instance of the class
        :param request: Get the query string from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        response, field_names, file_name = new_user_in_bot_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_new_user_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying New User to the BOT pdf export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_new_user_export_pdf")
    def new_user_in_bot_export_pdf(self, request, *args, **kwargs):
        """
        The new_user_in_bot_export_pdf function is used to export a PDF file containing the new users in BOT.
            The function takes in request, *args and **kwargs as parameters.
            It then creates a tz_info variable that stores the timezone information of settings.TIME_ZONE (which is UTC).
            Next, it creates a get_qs variable that stores the query results from querying MessageLog using BotReportSerializer and db schema &quot;event&quot;.
                The query filters out all messages with &quot;agent&quot; or &quot;/&quot; in them and only selects source=&quot;user&quot;, tenant=get_current_tenant name

        :param self: Represent the instance of the class
        :param request: Get the query string from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = new_user_in_bot_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "New Users In BOT",
            request.user.username,
        )
        return items

    # Customer Conversations
    @extend_schema(
        operation_id="bot_conversations",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Details of Customer Conversations",
    )
    @action(methods=["POST"], detail=False, url_path="bot_conversations")
    def conversations(self, request, *args, **kwargs):
        """
        The Conversations function returns a list of all conversations that have occurred between the bot and users.
        The function takes in a request object, which is used to determine what data should be returned.
        The function then queries the database for all messages sent by users (source=&quot;user&quot;) and filters out any messages that are not from users.
        It then annotates each message with its channel id, session id, channel name, message text, intent name (if applicable), whether it was handled by an agent or not (&quot;handled&quot;), score (how confident the bot was in its response), source (&quot;user&quot;),

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = conversation_generic(request)
        return get_generic_response(params)

    # Conversation chart export csv format
    @extend_schema(
        operation_id="bot_conversations_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="User for downloading Customer Conversations csv export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_conversations_export_csv")
    def conversations_export(self, request, *args, **kwargs):
        """
        The conversations_export function is used to export the conversations of a customer.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = conversation_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Customer_Id",
                    "User_Session_Id",
                    "Channel",
                    "Message",
                    "Intent",
                    "Handled",
                    "Score",
                    "Source",
                    "Timestamp",
                ],
                "fileName": "conversations.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_conversations_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="User for downloading Customer Conversations pdf export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_conversations_export_pdf")
    def conversations_export_pdf(self, request, *args, **kwargs):
        """
        The conversations_export_pdf function is used to export the conversations of a customer in PDF format.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the first settings.MAX_PDF_LIMIT conversations
        """
        params = conversation_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Customer_Id",
                    "User_Session_Id",
                    "Channel",
                    "Message",
                    "Intent",
                    "Handled",
                    "Score",
                    "Source",
                    "Timestamp",
                ],
                "fileName": "conversations.pdf",
                "title": "Conversations",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_conversations_export_excel",
        tags=[AuthTags.AUTHORIZE],
        description="User for downloading Customer Conversations pdf export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_conversations_export_excel")
    def bot_conversations_export_excel(self, request, *args, **kwargs):
        """
        The conversations_export_pdf function is used to export the conversations of a customer in PDF format.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the first settings.MAX_PDF_LIMIT conversations
        """
        params = conversation_generic(
            request,
            key="excel_kwargs",
            value={"timestamp_keys": ["Timestamp"], "fileName": "conversations.xlsx"},
        )
        return get_generic_response(params)

    # Returning User in Handoff
    @extend_schema(
        operation_id="bot_returning_user",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Returning User To BOT",
    )
    @action(methods=["POST"], detail=False, url_path="bot_returning_user")
    def returning_user_in_bot(self, request, *args, **kwargs):
        """
        The Returning_user_in_bot function returns a table of returning users in the bot.
            The function takes in a request and uses it to query the MessageLog model, using
            the BotReportSerializer as its serializer. It then filters out all messages that are not from users,
            It then groups by channel_id and counts
            unique session IDs for each channel ID. Then it annotates with Channel name, Customer name (channel ID), and Time of last visit.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        result, _, _ = returning_user_in_bot_generic(request)
        return return_table(result, request)

    # Returning User in BOT chart Export csv format
    @extend_schema(
        operation_id="bot_returning_user_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="User for downloading Returning User to BOT csv export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_returning_user_export_csv")
    def return_user_in_bot_export(self, request, *args, **kwargs):
        """
        The return_user_in_bot_export function returns a CSV file containing the following information:
            - Customer (the customer's name)
            - Channel (the channel through which the customer interacted with the bot)
            - Time (the time at which this interaction occurred, in UTC format)

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file containing the customer, channel and time of a user who has visited more than once
        """
        response, field_names, file_name = returning_user_in_bot_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_returning_user_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="User for downloading Returning User to BOT pdf export",
    )
    @action(methods=["POST"], detail=False, url_path="bot_returning_user_export_pdf")
    def return_user_in_bot_export_pdf(self, request, *args, **kwargs):
        """
        The return_user_in_bot_export_pdf function returns a PDF file containing the following information:
            - Customer (the customer's name)
            - Channel (the channel through which the customer contacted you)
            - Time (when they last contacted you)

        :param self: Allow an instance of a class to access its own attributes and methods
        :param request: Get the query string from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file of the top settings.MAX_PDF_LIMIT returning users in bot
        """
        response, field_names, file_name = returning_user_in_bot_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Returning Users In BOT",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_user_flow_sankey_chart",
        tags=[AuthTags.AUTHORIZE],
        description="User for the flow of the user",
    )
    @action(methods=["POST"], detail=False, url_path="bot_user_flow_sankey_chart")
    def user_flow_shankey_chart(self, request, *args, **kwargs):
        """
        The user_flow_shankey_chart function is a viewset that returns the data for the user flow sankey chart.
        The function takes in a request and returns a response containing two lists of dictionaries: values and links.
        The values list contains dictionaries with keys 'Target' and 'value'. The Target key has as its value
        a string concatenation of target, rank, and space (e.g., &quot;target 1&quot;). The value key has as its value an integer count
        of how many times that particular Target appears in the database table UserFlow.

        :param self: Represent the instance of a class
        :param request: Get the query string from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A response that is a dictionary with two keys: values and links
        """
        response = user_flow_shankey_chart_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="bot_daily_user_messages_heatmap",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying heatmap",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_user_messages_heatmap")
    def user_messages_heatmap(self, request, *args, **kwargs):
        response = user_messages_heatmap_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="bot_top_ten_matched_intents_by_channel",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top 10 intents triggered by channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_top_ten_matched_intents_by_channel",
    )
    def top_ten_matched_intents_by_channel(self, request, *args, **kwargs):
        items, _, _ = top_ten_matched_intents_by_channel_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_top_ten_matched_intents_by_channel_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top 10 intents triggered by channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_top_ten_matched_intents_by_channel_export_csv",
    )
    def top_ten_matched_intents_by_channel_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = top_ten_matched_intents_by_channel_generic(
            request
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_top_ten_matched_intents_by_channel_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top 10 intents triggered by channel",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_top_ten_matched_intents_by_channel_export_pdf",
    )
    def top_ten_matched_intents_by_channel_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = top_ten_matched_intents_by_channel_generic(
            request
        )
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Top 10 matched Intents by Channel",
            request.user.username,
        )
        return items
