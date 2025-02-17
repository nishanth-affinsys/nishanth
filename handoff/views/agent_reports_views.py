from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from handoff.services.agent_reports_utils import (
    interaction_arrived_bar_generic,
    interaction_accepted_channelwise_generic,
    agent_average_session_time_by_channel_generic,
    entered_accepted_generic,
    messages_in_each_interactions_generic,
    handoff_flow_shankey_chart_generic,
    interactions_arrived_or_accepted_generic,
)
from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import return_table


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from main.utils.export import export_csv, export_pdf


class AgentReportViewSet(GenericViewSet):  # For Agent Report
    # Total Interactions Arrived per channel
    @extend_schema(
        operation_id="agent_report_interaction_arrived_bar",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Interactions Arrived per channel",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_interaction_arrived_bar"
    )
    def agent_report_interaction_arrived_bar(self, request, *args, **kwargs):
        """
        The interaction_arrived_bigNumber function is a custom function that returns the number of interactions
        that have arrived in each channel. The data returned by this function is used to populate the big numbers on
        the dashboard.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of sessions for each channel
        """
        qs = interaction_arrived_bar_generic(request)
        return Response(qs)

    # Number of Interactions Arrived per Agent
    @extend_schema(
        operation_id="agent_report_interaction_arrived_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Interaction Arrived",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_arrived_details",
    )
    def interaction_arrived(self, request, *args, **kwargs):
        """
        The interaction_arrived function is used to get the number of interactions arrived for each agent.
        The function takes in a request object and kwargs, which are then added to filter_data.
        A query set is created that gets all agents from the SocialconversationAgenttenant table where
        the tenant name matches the current tenant's name. The values() method is called on this query set,
        which returns a dictionary with keys &quot;agent__username&quot; and &quot;agent__id&quot;. The annotate() method is then called on this qs, which adds two new fields: username and id (these are aliases for agent__

        :param self: Represent the instance of the class
        :param request: Get the request object, which contains information about the current request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries, each dictionary containing the agent name, date, channel and number of interactions arrived
        """
        response, _, _ = interactions_arrived_or_accepted_generic(
            request, "handoff-notification"
        )
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_report_interaction_arrived_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of Interaction Arrived",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_arrived_details_export_csv",
    )
    def interaction_arrived_export(self, request, *args, **kwargs):
        """
        The interaction_arrived_export function is used to export the interactions arrived data.
            The function takes in a request and *args, **kwargs as parameters.
            It then filters the data based on the timestamp range and channel provided by the user.
            It then creates an empty dictionary called res which will be used to store all of our queryset results for each agent that we loop through in our next step.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A csv file with the following columns:
        """
        response, field_names, file_name = interactions_arrived_or_accepted_generic(
            request, "handoff-notification"
        )
        items = export_csv(response, field_names, "interactions_arrived.pdf")
        return items

    # interactions arrived pdf

    @extend_schema(
        operation_id="agent_report_interaction_arrived_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of Interaction Arrived in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_arrived_details_export_pdf",
    )
    def interaction_arrived_details_export_pdf(self, request, *args, **kwargs):
        """
        The interaction_arrived_details_export_pdf function is used to export the Interactions Arrived Details report as a PDF.
        The function takes in the request and kwargs, which are then added to filter_data. The qs variable is set equal to a query that gets all of the SocialconversationAgenttenant objects with tenant names matching get_current_tenant_name(), values for agent username and id, annotates those values with username=F(&quot;agent__username&quot;) and id=F(&quot;agent__id&quot;), then returns only those two fields. res is an empty dictionary that will be filled by looping through each user in qs (

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = interactions_arrived_or_accepted_generic(
            request, "handoff-notification"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "interactions_arrived.pdf",
            "Interactions Arrived",
            request.user.username,
        )
        return items

    # Total Interactions Accepted per channel(not a big number)
    @extend_schema(
        operation_id="agent_report_interaction_accepted_bar",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Interactions Accepted per channel(not a bignumber)",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_interaction_accepted_bar"
    )
    def interaction_accepted_channelwise(self, request, *args, **kwargs):
        """
        The interaction_accepted_bigNumber function is a custom API endpoint that returns the number of accepted interactions for each channel.
        The function takes in a request and *args, **kwargs as parameters. The filter_data variable is set to the data contained within the request object.
        The filter_data variable then updates itself with any additional keyword arguments passed into it (**kwargs). The qs variable is set to an AnalyticsSocialevent queryset filtered by tenant name, timestamp range, and channel(s) specified in the request object's data field.
        This queryset also filters out all events except for agent-accept events (i.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of accepted interactions per channel
        """
        qs = interaction_accepted_channelwise_generic(request)
        return Response(qs)

    # Number of Interactions Accepted per Agent
    @extend_schema(
        operation_id="agent_report_interaction_accepted_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Interactions Accepted",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_accepted_details",
    )
    def interaction_accepted(self, request, *args, **kwargs):
        """
        The interaction_accepted function is used to get the number of interactions accepted by each agent.
            The function takes in a request object and returns a paginated response containing the following fields:
                - Agent Name: The name of the agent who accepted an interaction.
                - Date: The date on which an interaction was accepted by an agent.
                - Channel: The channel through which an interaction was received (e.g., Facebook, Twitter).
                - Interactions Accepted: Number of interactions that were accepted by agents.

        :param self: Represent the instance of the class
        :param request: Get the request object, which contains all the information about the current http request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of interactions accepted by each agent on a particular day
        """
        response, _, _ = interactions_arrived_or_accepted_generic(
            request, "agent-accept"
        )
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_report_interaction_accepted_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of Interactions Accepted",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_accepted_details_export_csv",
    )
    def interaction_accepted_export(self, request, *args, **kwargs):
        """
        The interaction_accepted_export function is used to export the data for the Interactions Accepted chart.
        It takes in a request object and any number of keyword arguments, which are then added to a filter_data dictionary.
        The function then creates an empty response list, which will be populated with dictionaries containing the data that we want to export.
        Next, it queries SocialconversationAgenttenant objects using values() and annotate() methods so that we can get all of our agents' usernames and ids into one queryset (qs). Then it loops through each user in qs (which contains username/id pairs)

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A csv file containing the following columns:
        """
        response, field_names, file_name = interactions_arrived_or_accepted_generic(
            request, "agent-accept"
        )
        items = export_csv(response, field_names, "interactions_accepted.csv")
        return items

    # pdf for interactions accepted details
    @extend_schema(
        operation_id="agent_report_interaction_accepted_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of Interactions Accepted in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_interaction_accepted_details_export_pdf",
    )
    def interaction_accepted_export_pdf(self, request, *args, **kwargs):
        """
        The interaction_accepted_export_pdf function is used to export the data from the Interactions Accepted report into a PDF file.
        The function takes in a request object and any number of keyword arguments, which are then stored in filter_data.
        A query set is created that contains all of the agents for this tenant, and their usernames and IDs are extracted from it.
        An empty dictionary called res is created to store each agent's username as keys, with values being another query set containing
        the channel name, date (cast as DateField), count of interactions accepted per day per channel for that agent on those dates.  The response list stores

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response, field_names, file_name = interactions_arrived_or_accepted_generic(
            request, "agent-accept"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "interactions_accepted.pdf",
            "Agent Interactions Accepted",
            request.user.username,
        )
        return items

    # Average session time in minutes per Agent
    @extend_schema(
        operation_id="agent_report_average_session_time",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Average Session Time",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_average_session_time"
    )
    def average_session_time(self, request, *args, **kwargs):
        """
        The average_session_time function returns the average session time for each agent on a given day.
        The function takes in a request object and keyword arguments, which are used to filter the data.
        The function then queries AnalyticsSocialevent objects that have an event of 'agent-accept', 'user-end-confirm',
        'agent-force-end', 'agent-end_confirm' or 'user_inactive'. The query is filtered by timestamp range, channel and tenant name.
        It also filters out any duplicate sessions using distinct(). The query is then ordered by date descendingly.
        A response list is created to

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The average handling time of the agent per day
        """
        response, _, _ = agent_average_session_time_by_channel_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_report_average_session_time_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Average Session Time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_average_session_time_export_csv",
    )
    def average_session_time_export(self, request, *args, **kwargs):
        """
        The average_session_time_export function is used to export the average session time of each agent for a given date range.
        The function takes in a request object and keyword arguments, which are then added to the filter_data dictionary.
        A query set is created using the AnalyticsSocialevent model, filtering by timestamp__range (the start and end dates), channel (the social media platform),
        and tenant (the current tenant). The event field is filtered by four different events: agent-accept, user-end-confirm, agent-force-end,
        agent-end_confirm and user inactive. The values() method returns all of

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        (
            response,
            field_names,
            file_name,
        ) = agent_average_session_time_by_channel_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # average session time pdf
    @extend_schema(
        operation_id="agent_report_average_session_time_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Average Session Time in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_average_session_time_export_pdf",
    )
    def average_session_time_export_pdf(self, request, *args, **kwargs):
        """
        The average_session_time_export_pdf function is used to export the average session time data in a PDF format.
        The function takes in the request and kwargs as parameters, and returns a PDF file containing the average session time data.


        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        (
            response,
            field_names,
            file_name,
        ) = agent_average_session_time_by_channel_generic(request)
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

    # Aggregate for handoff flow entered, handled unhandled, abandoned
    @extend_schema(
        operation_id="agent_queue_report_aggregate_analysis",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Chats in Queue, Accepted by agents,Unhandled and Abandoned chats.",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_queue_report_aggregate_analysis"
    )
    def entered_accepted(self, request, *args, **kwargs):
        """
        The entered_accepted function is used to calculate the number of chats that were entered into a queue, accepted by an agent, unhandled by an agent and abandoned.
        The function takes in a request object and keyword arguments. The filter_data variable is set equal to the data contained within the request object.
        The filter_data variable then updates itself with any keyword arguments passed into it (in this case there are none).
        A queryset is created using AnalyticsSocialevent objects that have a timestamp range between two dates specified in the timestamp__range key of filter_data, as well as having one of several channels specified in channel key of filter

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of chats that are entered in queue, accepted by agent, unhandled and abandoned
        """
        response, _, _ = entered_accepted_generic(request)
        return return_table(response, request)

    # Entered and Accepted Report export csv format
    @extend_schema(
        operation_id="agent_queue_report_aggregate_analysis_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Chats in Queue, Accepted by agents,Unhandled and Abandoned chats in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_report_aggregate_analysis_export_csv",
    )
    def entered_accepted_export(self, request, *args, **kwargs):
        """
        The entered_accepted_export function is used to export the data from the entered_accepted function.
        It takes in a request and kwargs, which are then added to filter_data. The items variable is set equal
        to an AnalyticsSocialevent query that filters by timestamp range and channel, as well as adding a tenant
        filter for security purposes. The values() method returns only the channel field of each item in items, while
        the annotate() method adds additional fields based on calculations performed on other fields (in this case,
        Entered_in_Queue = Count(&quot;session&quot;, distinct=True, filter=Q(

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: An object that is a generator
        """
        response, field_names, file_name = entered_accepted_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # previous name :entered_accepted_export_pdf
    @extend_schema(
        operation_id="agent_queue_report_aggregate_analysis_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Chats in Queue, Accepted by agents,Unhandled and Abandoned chats in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_queue_report_aggregate_analysis_export_pdf",
    )
    def entered_accepted_pdf_download(self, request, *args, **kwargs):
        """
        The entered_accepted_pdf_download function is used to generate a PDF report of the number of chats that entered the queue, were accepted by an agent, and were unhandled or abandoned.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """

        response, field_names, file_name = entered_accepted_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Aggregate Agent Report",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_report_messages_in_interactions",
        tags=[AuthTags.AUTHORIZE],
        description="details of no of messages in each user interactions",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_messages_in_interactions"
    )
    def messages_in_each_interactions(self, request, *args, **kwargs):
        """
        The messages_in_each_interactions function returns a table of the number of messages sent by each agent in each interaction.
        The function takes in a request object and kwargs, which are used to filter the data. The timestamp__range is used to filter
        the data based on date range, while channel filters the data based on channel type (e.g., Facebook). The result variable uses
        a Django ORM query to return all rows from AnalyticsSocialevent that have an event value equal to &quot;social-message&quot; or &quot;chat-message&quot;.
        The values() method is then called on this queryset, which allows us to specify what

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of messages in each interaction
        """
        result, _, _ = messages_in_each_interactions_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="agent_report_messages_in_interactions_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="details of no of messages in each user interactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_messages_in_interactions_export_csv",
    )
    def messages_in_interactions_export(self, request, *args, **kwargs):
        """
        The messages_in_interactions_export function is used to export a CSV file containing the following data:
            - Agent Name
            - Customer Name
            - Session ID (unique identifier for each session)
            - Channel (Facebook, Twitter, etc.)
            - Timestamp of message sent/received in UTC timezone.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The result of the export_csv function
        """
        response, field_names, file_name = messages_in_each_interactions_generic(
            request
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # messages in interactions downloading in pdf
    @extend_schema(
        operation_id="agent_report_messages_in_interactions_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="details of no of messages in each user interactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_messages_in_interactions_export_pdf",
    )
    def messages_in_interactions_export_pdf(self, request, *args, **kwargs):
        """
        The messages_in_interactions_export_pdf function is used to export the messages in each interaction data as a PDF file.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = messages_in_each_interactions_generic(
            request
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Messages in Each interactions",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="handoff_flow_shankey_chart",
        tags=[AuthTags.AUTHORIZE],
        description="flow of a user when triggers handoff is shown here",
    )
    @action(methods=["POST"], detail=False, url_path="handoff_flow_shankey_chart")
    def handoff_flow_shankey_chart(self, request, *args, **kwargs):
        """
        The handoff_flow_shankey_chart function is used to generate a Sankey chart for the handoff flow.
        The function takes in a request and returns a response containing values and links.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A dictionary with two keys, values and links
        """
        response = handoff_flow_shankey_chart_generic(request)
        return Response(response)
