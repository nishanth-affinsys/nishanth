from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from handoff.models import NewUserInHandoff, ReturningUserInHandoff
from handoff.services.detail_queue_report_utils import (
    chatbot_message_interactions_generic,
    total_session_time_generic,
    cust_req_for_handoff_generic,
    agent_interactions_generic,
    bot_interactions_generic,
    abandoned_users_details_generic,
    average_session_time_seconds_generic,
    customer_activity_generic,
    agent_handoff_details_generic,
    handled_ended_chats_generic,
    unhandled_chats_generic,
    user_in_handoff_generic,
    bot_interactions_export_table_generic,
    agent_interactions_export_table_generic,
)
from main.settings import MAX_PDF_LIMIT
from main.utils.export import export_csv, export_pdf


from main.utils.boiler_plate import (
    get_generic_response,
    return_table,
)


class DetailReportViewSet(GenericViewSet):  # For Queue Report
    # @extend_schema(
    #     operation_id="entered_queue",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total people who entered queue",
    # )
    # # Number of Interactions entered in queue (waiting in queue neither accepted by Agent nor rejected by agent)
    # @action(methods=["POST"], detail=False, url_path="entered-queue")
    # def entered_queue(self, request, *args, **kwargs):
    #     """
    #     The entered_queue function returns the number of times a user has entered the queue.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the tenant name from the request
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: A list of all the sessions in which a customer entered the queue
    #     """
    #     params = entered_queue_generic(request)
    #     return get_generic_response(params)

    # Number of Interactions Accepted by Agent
    # @extend_schema(
    #     operation_id="agent_accept",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total people who Agent Accepted",
    # )
    # @action(methods=["POST"], detail=False, url_path="agent-accept")
    # def agent_accept(self, request, *args, **kwargs):
    #     """
    #     The agent_accept function is a view that returns the number of times an agent has accepted a call.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the tenant name from the request
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: The number of agent-accept events for a given tenant
    #     """
    #     params = agent_accept_generic(request)
    #     return get_generic_response(params)

    # Number of chats got Abandoned (either by user cancel , or user fallout) after notification went to agent
    # @extend_schema(
    #     operation_id="abondaned_chats",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying chatd after notification went to agent but max routing exceed or user cancelled handoff",
    # )
    # @action(methods=["POST"], detail=False, url_path="abondaned-chats")
    # def abandoned_chats(self, request, *args, **kwargs):
    #     """
    #     The abondaned_chats function is used to get the number of abandoned chats.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The number of abandoned chats
    #     """
    #     params = abandoned_chats_generic(request)
    #     return get_generic_response(params)

    # Total messages from Users to Agents
    # @extend_schema(
    #     operation_id="total_message_from_user_to_agent",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total messages from Users to Agents",
    # )
    # @action(methods=["POST"], detail=False, url_path="message-user-agent")
    # def total_message_from_user_to_agent(self, request, *args, **kwargs):
    #     """
    #     The total_message_from_user_to_agent function returns the total number of messages sent from a user to an agent.
    #         ---
    #         # YAML (must be separated by `---`)
    #
    #     :param self: Represent the instance of a class
    #     :param request: Get the request object, which is used to get the tenant name
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: The total number of messages sent by users to agents
    #     """
    #     params = total_message_from_user_to_agent_generic(request)
    #     return get_generic_response(params)

    # Total messages from Agents to Users
    # @extend_schema(
    #     operation_id="total_message_from_agent_to_user",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total messages from Agents to Users",
    # )
    # @action(methods=["POST"], detail=False, url_path="message-agent-user")
    # def total_message_from_agent_to_user(self, request, *args, **kwargs):
    #     """
    #     The total_message_from_agent_to_user function returns the total number of messages sent from an agent to a user.
    #         ---
    #         # YAML (must be separated by `---`)
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: The total number of messages sent by the agent to the user
    #     """
    #     params = total_message_from_agent_to_user_generic(request)
    #     return get_generic_response(params)

    # Total messages from Users to Bot
    # @extend_schema(
    #     operation_id="total_message_from_user_to_bot",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total messages from Users to Bot",
    # )
    # @action(methods=["POST"], detail=False, url_path="message-user-bot")
    # def total_message_from_user_to_bot(self, request, *args, **kwargs):
    #     """
    #     The total_message_from_user_to_bot function is a generic function that returns the total number of messages sent from users to bots.
    #     The function takes in request, *args, and **kwargs as parameters.
    #     It then creates a dictionary called params with the following keys: &quot;request&quot;, &quot;models&quot;, &quot;db_schema&quot;,
    #     &quot;filter_kwargs&quot;, &quot;filter_args&quot;,&quot;serializers&quot;,&quot;exclude&quot;,&quot;values&quot; and count&quot;. The values for each key are as follows:
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list to a function
    #     :return: The total number of messages sent by the user to the bot
    #     """
    #     params = total_message_from_user_to_bot_generic(request)
    #     return get_generic_response(params)

    @extend_schema(
        operation_id="agent_detailed_chatbot_message_interactions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying all messages from agent to user, user to agent ,user to bot",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_chatbot_message_interactions",
    )
    def chatbot_message_interactions(self, request, *args, **kwargs):
        """
        The chatbot_message_interactions function is used to return the total number of messages sent from a user to an agent,
        the total number of messages sent from an agent to a user, and the total number of messages sent from a user directly
        to the chatbot. The function takes in two parameters: request and *args. The request parameter is used for HTTP requests
        and *args allows us to pass multiple arguments into our function.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, each containing the channel name and three message counts
        """
        response, _, _ = chatbot_message_interactions_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="agent_detailed_chatbot_message_interactions_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying all messages from agent to user, user to agent ,user to bot",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_chatbot_message_interactions_export_csv",
    )
    def chatbot_message_interactions_export(self, request, *args, **kwargs):
        """
        The chatbot_message_interactions_export function is used to export a CSV file containing the following data:
            - Channel
            - Total messages user to agent
            - Total messages agent to user
            - Total messages user to bot

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, field_names, file_name = chatbot_message_interactions_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # pdf for customer activity
    @extend_schema(
        operation_id="agent_detailed_chatbot_message_interactions_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying all messages from agent to user, user to agent ,user to bot",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_chatbot_message_interactions_export_pdf",
    )
    def chatbot_message_interactions_export_pdf(self, request, *args, **kwargs):
        """
        The chatbot_message_interactions_export_pdf function is used to export the chatbot message interactions data as a PDF file.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = chatbot_message_interactions_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Count of Messages",
            request.user.username,
        )
        return items

    # Total time spent by agents for attending the sessions in given time interval
    @extend_schema(
        operation_id="agent_detailed_total_handling_time",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total time spent by agents for attending the sessions in given time interval",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_detailed_total_handling_time"
    )
    def total_session_time(self, request, *args, **kwargs):
        """
        The total_session_time function returns the total handling time of each agent for a given date range.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The total handling time of an agent
        """
        response, _, _ = total_session_time_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_detailed_total_handling_time_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Total time spent by agents for attending the sessions in given time interval",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_total_handling_time_export_csv",
    )
    def total_session_time_export(self, request, *args, **kwargs):
        """
        The total_session_time_export function is used to export the total session time of all agents in a given date range.
        The function takes in a request object and keyword arguments, which are then added to the filter_data dictionary.
        A query set is created using the AnalyticsSocialevent model, filtering by timestamp__range (the start and end dates), channel (the social media platform), tenant (the current tenant name) and event type (&quot;agent-accept&quot;, &quot;user-end-confirm&quot;, &quot;agent-force-end&quot;, &quot;agent-end_confirm&quot; or &quot;user inactive&quot;). The values() method returns only certain fields from each record that

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following fields:
        """
        response, field_names, file_name = total_session_time_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # PDF download function for Total session time
    @extend_schema(
        operation_id="agent_detailed_total_handling_time_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Total time spent by agents for attending the sessions in given time interval",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_total_handling_time_export_pdf",
    )
    def total_session_time_export_pdf(self, request, *args, **kwargs):
        """
        The total_session_time_export_pdf function is used to export the total session time of all agents in a particular channel.
        The function takes in the following parameters:
            request - The request object that contains information about the current HTTP request.
            *args - A tuple containing positional arguments, if any were provided when calling this function.
            **kwargs - A dict containing keyword arguments, if any were provided when calling this function.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = total_session_time_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Total Handling Time",
            request.user.username,
        )
        return items

    # Customers required for handoff in particular hours of a day
    @extend_schema(
        operation_id="agent_detailed_cust_req_for_handoff",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Customers requested for handoff in particular hours of a day",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_detailed_cust_req_for_handoff"
    )
    def cust_req_for_handoff(self, request, *args, **kwargs):
        """
        The cust_req_for_handoff function is a custom request function that returns the number of handoff-initial events
        that occurred in each hour of the day. The data returned by this function is used to populate the Handoff Initials
        graph on the Analytics page.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A dictionary with the following keys:
        """
        params = cust_req_for_handoff_generic(request)
        return get_generic_response(params)

    #  Total sessions attended by agents in particular hour in a day
    @extend_schema(
        operation_id="agent_detailed_interactions_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions attended by agents in particular hour in a day",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_detailed_interactions_linechart"
    )
    def agent_interactions(self, request, *args, **kwargs):
        """
        The agent_interactions function is a view that returns the number of agent interactions per hour.
        The function takes in a request and *args, **kwargs as parameters. The tz_info variable is set to the timezone specified in settings.py (TIME_ZONE).
        The params dictionary contains all of the information needed for get_generic_response to return an appropriate response:
            - request: The HTTP request object passed into this function by Django REST Framework's generic views framework. This allows us to access any data sent with the HTTP request, such as query parameters or URL path variables (e.g., /api/v

        :param self: Represent the instance of the class
        :param request: Get the tenant name
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The following:
        """
        params = agent_interactions_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="agent_detailed_interactions_linechart_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions attended by agents in particular hour in a day",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_interactions_linechart_export_csv",
    )
    def agent_interactions_export_csv(self, request, *args, **kwargs):
        params = agent_interactions_export_table_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Date", "Hour", "count"],
                "fileName": "agent_interactions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_detailed_interactions_linechart_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions attended by agents in particular hour in a day",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_interactions_linechart_export_pdf",
    )
    def agent_interactions_export_pdf(self, request, *args, **kwargs):
        params = agent_interactions_export_table_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Date", "Hour", "count"],
                "fileName": "agent_interactions.pdf",
                "title": "Agent Interactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Total sessions happened by BOT in particular hours of a day
    @extend_schema(
        operation_id="agent_detailed_bot_interactions_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions happened by BOT in particular hours of a day",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_bot_interactions_linechart",
    )
    def bot_interactions(self, request, *args, **kwargs):
        """
        The bot_interactions function is a generic function that can be used to get the number of interactions with a bot.
        It takes in the following parameters:
            request - The HTTP request object. This is required by Django REST Framework for all viewsets.
            models - The model class that contains the data you want to query from (in this case, MessageLog). This should be imported from your app's models file (e.g., &quot;from .models import MessageLog&quot;).
            db_schema - The name of your database schema as defined in settings.py (e.g., &quot;event&quot;). If you are using multiple databases

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The following:
        """
        params = bot_interactions_generic(request)
        return Response(params)

    @extend_schema(
        operation_id="agent_detailed_bot_interactions_linechart_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions happened by BOT in particular hours of a day",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_bot_interactions_linechart_export_csv",
    )
    def bot_interactions_export_csv(self, request, *args, **kwargs):
        params = bot_interactions_export_table_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Date", "Hour", "count"],
                "fileName": "bot_interactions_by_hour.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_detailed_bot_interactions_linechart_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions happened by BOT in particular hours of a day",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_bot_interactions_linechart_export_pdf",
    )
    def bot_interactions_export_pdf(self, request, *args, **kwargs):
        params = bot_interactions_export_table_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Date", "Hour", "count"],
                "fileName": "bot_interactions_by_hour.pdf",
                "title": "Bot Interactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # New Users came for handoff in a given time interval
    @extend_schema(
        operation_id="agent_queue_new_users_handoff",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying New Users came for handoff in a given time interval",
    )
    @action(methods=["POST"], detail=False, url_path="agent_queue_new_users_handoff")
    def new_user_in_handoff(self, request, *args, **kwargs):
        """
        The new_user_in_handoff function is used to get the data for the New User in Handoff report.
        The function takes a request object and keyword arguments as parameters. The request object contains
        the filter data that will be used to query the database, while any keyword arguments are passed on
        to other functions that may need them. The function then creates a queryset of all new users in handoff
        that match the filter criteria specified by the user, and annotates it with additional fields needed for
        the report (Customer_Id, Username, Channel, Phone_Number). It then returns this queryset after applying search/sort

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The data from the newuserinhandoff model
        """
        qs, _, _ = user_in_handoff_generic(request, NewUserInHandoff, "time")
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_queue_new_users_handoff_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading New Users came for handoff in a given time in csv formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_new_users_handoff_export_csv",
    )
    def new_user_in_handoff_export(self, request, *args, **kwargs):
        """
        The new_user_in_handoff_export function is a custom function that allows the user to export data from the NewUserInHandoff model.
        The function takes in request and *args, **kwargs as parameters. The filter_data variable is set equal to request.data and then updated with kwargs using .update().
        The qs variable is set equal to a query that filters by timestamp__range (a range of timestamps) and channel (the channel name). It also filters by tenant using get_current_tenant_name() which returns the current tenant's name as a string.
        It annotates Customer Id, Username,

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names, file_name = user_in_handoff_generic(
            request, NewUserInHandoff, "time"
        )
        items = export_csv(response, field_names, "new_user_in_handoff.csv")
        return items

    @extend_schema(
        operation_id="agent_queue_new_users_handoff_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading New Users came for handoff in a given time in pdf formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_new_users_handoff_export_pdf",
    )
    def new_user_in_handoff_export_pdf(self, request, *args, **kwargs):
        """
        The new_user_in_handoff_export_pdf function is used to export a PDF file of the New Users In HandOff data.
        The function takes in a request and any number of arguments, as well as keyword arguments.
        It then creates an object called tz_info that stores the timezone information from settings.TIME_ZONE (which is set to UTC).
        Next, it creates an object called filter_data that stores all of the data from request.data (the user's inputted filters). It then updates this with any additional keyword arguments passed into the function call itself (this will be empty for now since we are not passing in anything else).

        :param self: Represent the instance of the object itself
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A pdf file
        """
        response, field_names, file_name = user_in_handoff_generic(
            request, NewUserInHandoff, "time"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "new_user_in_handoff.pdf",
            "New Users In HandOff",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_queue_returning_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Returned Users for handoff in a given time interval",
    )
    @action(methods=["POST"], detail=False, url_path="agent_queue_returning_users")
    def returning_user_in_handoff(self, request, *args, **kwargs):
        """
        The returning_user_in_handoff function is used to return a list of all returning users in handoff.
        The function takes the following parameters:
            request - The HTTP request object that contains the GET query parameters.
            *args - A variable length argument list containing any additional arguments passed into the function.
            **kwargs - An arbitrary keyword argument dictionary containing any additional arguments passed into the function.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A queryset of returninguserinhandoff objects
        """
        qs, _, _ = user_in_handoff_generic(
            request, ReturningUserInHandoff, "return_time"
        )
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_queue_returning_users_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Returned Users for handoff in a given time in csv formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_returning_users_export_csv",
    )
    def return_user_in_handoff_export(self, request, *args, **kwargs):
        """
        The return_user_in_handoff_export function is used to export a CSV file of all returning users in handoff.
        The function takes the following parameters:
            request - The HTTP request object that contains the data for filtering and sorting.
            *args - A list of arguments passed into the function, which are not used here.
            **kwargs - A dictionary of keyword arguments passed into the function, which are not used here.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A csv file with the following fields:
        """
        response, field_names, file_name = user_in_handoff_generic(
            request, ReturningUserInHandoff, "return_time"
        )
        items = export_csv(response, field_names, "returning_user_in_handoff.csv")
        return items

    @extend_schema(
        operation_id="agent_queue_returning_users_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Returned Users for handoff in a given time in pdf formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_returning_users_export_pdf",
    )
    def return_user_in_handoff_export_pdf(self, request, *args, **kwargs):
        """
        The return_user_in_handoff_export_pdf function is used to export the data from the ReturningUserInHandoff model into a PDF file.
        The function takes in request and kwargs as parameters, and returns an iterator object that contains the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: An iterator
        """
        response, field_names, file_name = user_in_handoff_generic(
            request, ReturningUserInHandoff, "return_time"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "returning_user_in_handoff.pdf",
            "Returning Users In Handoff",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_detailed_abandoned_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Abandoned Users Details",
    )
    @action(methods=["POST"], detail=False, url_path="agent_detailed_abandoned_users")
    def abandoned_users_details(self, request, *args, **kwargs):
        """
        The abandoned_users_details function is used to get the details of abandoned users.
            It takes in a request object and returns a paginated response containing the following fields:
                Customer_name, Phone_Number, Email, Channel and Session.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries that contain the following information:
        """
        qs, _, _ = abandoned_users_details_generic(request)
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_detailed_abandoned_users_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Abandoned Users in csv formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_abandoned_users_export_csv",
    )
    def abandoned_users_details_export(self, request, *args, **kwargs):
        """
        The abandoned_users_details_export function is used to export the abandoned users details.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A generator object
        """
        response, field_names, file_name = abandoned_users_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_detailed_abandoned_users_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Abandoned Users in pdf formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_abandoned_users_export_pdf",
    )
    def abandoned_users_details_export_pdf(self, request, *args, **kwargs):
        """
        The abandoned_users_details_export_pdf function is used to export the abandoned chat details in a PDF format.
        The function takes in the request and kwargs as parameters, and returns an iterator object.


        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: An iterator
        """
        response, field_names, file_name = abandoned_users_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Abandoned Chat Details",
            request.user.username,
        )
        return items

    # Average session time (in  minutes) of agents attending the session in a given time interval
    @extend_schema(
        operation_id="agent_detailed_average_handling_time",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Aversage session time (in  minutes) of agents attending the session in a given time interval",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_detailed_average_handling_time"
    )
    def average_session_time_seconds(self, request, *args, **kwargs):
        """
        The average_session_time_seconds function returns the average session time in seconds for each agent.

        :param self: Represent the instance of the class
        :param request: Get the data from the request body
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average handling time of the agent
        """
        response, _, _ = average_session_time_seconds_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_detailed_average_handling_time_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Aversage session time (in  minutes) of agents attending the session in a given time interval",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_average_handling_time_export_csv",
    )
    def average_session_time_seconds_export(self, request, *args, **kwargs):
        """
        The average_session_time_seconds_export function is used to export the average handling time of an agent in seconds.
        The function takes a request object and keyword arguments as input. The filter_data variable stores the data from the
        request object, which is then updated with any keyword arguments that are passed into it.
        A queryset (qs) is created using this filter_data variable, which filters out all AnalyticsSocialevent objects
        based on their timestamp range, channel name(s), and tenant name (which will be set to whatever tenant you're currently logged in as).
        This queryset also filters out only those events that have event names equal to &quot;agent-accept

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The average handling time in minutes
        """
        response, field_names, file_name = average_session_time_seconds_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_detailed_average_handling_time_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Aversage session time (in  minutes) of agents attending the session in a given time interval",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_average_handling_time_export_pdf",
    )
    def average_session_time_seconds_export_pdf(self, request, *args, **kwargs):
        """
        The average_session_time_seconds_export_pdf function is used to export the average handling time of an agent in minutes.
        The function takes a request object and keyword arguments as input, and returns a PDF file containing the data.


        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = average_session_time_seconds_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Average Handling Time",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_detailed_customer_activity",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer activity in handoff",
    )
    @action(methods=["POST"], detail=False, url_path="agent_detailed_customer_activity")
    def customer_activity(self, request, *args, **kwargs):
        """
        The customer_activity function is used to return a list of all the customers that have interacted with the bot.
        The function takes in a request object and kwargs, which are then added to filter_data. The timezone information is
        then retrieved from settings and stored in tz_info. A query is then performed on AnalyticsSocialevent using filter_data
        to retrieve all records where event = 'handoff-initial'. The values returned by this query are Customer (social__username),
        Skill (social__skill), Phone Number (social__phone_number), Email(social__email) Channel, Timestamp(

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries, where each dictionary contains the following keys:
        """
        result, _, _ = customer_activity_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="agent_detailed_customer_activity_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer activity in handoff",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_customer_activity_export_csv",
    )
    def customer_activity_export(self, request, *args, **kwargs):
        """
        The customer_activity_export function is used to export a CSV file containing the following data:
            - Customer (username)
            - Skill (skill name)
            - Phone Number (phone number of customer)
            - Email (email address of customer, if available)
            - Channel ('facebook', 'twitter', etc.)
        :param self: Represent the instance of the object itself
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, field_names, file_name = customer_activity_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_detailed_customer_activity_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer activity in handoff in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_customer_activity_export_pdf",
    )
    def customer_activity_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = customer_activity_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Customer Activity",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_detailed_handoff_details",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer in handoff",
    )
    @action(methods=["POST"], detail=False, url_path="agent_detailed_handoff_details")
    def agent_handoff_details(self, request, *args, **kwargs):
        """
        The agent_handoff_details function returns a list of all agent handoff details.

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries, where each dictionary is a row in the table
        """
        result, _, _ = agent_handoff_details_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="agent_detailed_handoff_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer in handoff",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_handoff_details_export_csv",
    )
    def agent_handoff_details_export(self, request, *args, **kwargs):
        """
        The agent_handoff_details_export function is used to export the agent handoff details.

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names, file_name = agent_handoff_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # pdf for agent handoff details
    @extend_schema(
        operation_id="agent_detailed_handoff_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="details of the customer in handoff",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_detailed_handoff_details_export_pdf",
    )
    def agent_handoff_details_export_pdf(self, request, *args, **kwargs):
        """
        The agent_handoff_details_export_pdf function is used to export the agent handoff details in a PDF format.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = agent_handoff_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Agent Handoff Details",
            request.user.username,
        )
        return items

    # To display all the chats the was successfully accepted by agent and then later ended due to agent or user termination
    @extend_schema(
        operation_id="agent_detailed_ended_chats",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display pie chart for ended chats",
    )
    @action(methods=["POST"], detail=False, url_path="agent_detailed_ended_chats")
    def handled_ended_chats(self, request, *args, **kwargs):
        """
        The handled_ended_chats function returns a list of the number of chats that ended in each way.
        The function takes in a request and kwargs, which are used to filter the data.
        It then creates an AnalyticsSocialevent queryset with filters for timestamp range, channel, tenant name, and event type.
        The queryset is annotated with labels based on event type and counts for each label are calculated using Count().  The resulting data is returned as a Response object.

        :param self: Represent the instance of the class
        :param request: Get the filter data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A queryset of the number of chats that were ended by an agent, a user, or automatically
        """
        qs = handled_ended_chats_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="agent_detailed_unhandled_chats",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display pie chart for ended chats",
    )
    @action(methods=["POST"], detail=False, url_path="agent_detailed_unhandled_chats")
    def unhandled_chats(self, request, *args, **kwargs):
        """
        The unhandled_chats function returns a list of unhandled chats.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A queryset of dictionaries
        """
        qs = unhandled_chats_generic(request)
        return Response(qs)
