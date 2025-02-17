from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from handoff.services.live_report_utils import (
    online_agents_generic,
    message_agent_and_user_generic,
    chats_in_queue_generic,
    chats_in_queue_detail_generic,
    handoff_called_today_generic,
    online_detail_generic,
    online_customers_agent_generic,
    online_customers_bot_generic,
    handoff_duration_generic,
    agent_last_activity_time_generic,
    ended_chats_generic,
    agent_skill_generic,
    ongoing_max_chats_generic,
    current_loggedin_skills_generic,
    abandoned_users_details_live_generic,
    conversations_live_generic,
    top_messages_live_generic,
    interaction_live_generic,
)

from main.utils.boiler_plate import return_table


class LiveDataViewSet(GenericViewSet):  # For Live Report
    @extend_schema(
        operation_id="agent_live_online_agents",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Online Agents",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_online_agents")
    def online_agents(self, request, *args, **kwargs):
        """
        The online_agents function is a viewset that returns the number of agents online.
            It takes in a request and filters the data based on tenant name, then counts how many agents are online.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The count of online agents
        """
        qs = online_agents_generic()
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_messages_agents_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying messages between Agent and User",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_messages_agents_users")
    def message_agent_and_user(self, request, *args, **kwargs):  # add
        """
        The message_agent_and_user function is a custom function that returns the number of messages sent by agents and users in the last 3 minutes.
        The function takes in a request object, which contains information about the HTTP request made to this endpoint.
        It also takes in *args and **kwargs, which are used to pass additional arguments into functions when you don't know how many there will be ahead of time.

        :param self: Represent the instance of the class
        :param request: Get the data from the request body
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of chat and social messages sent by the user in the last three minutes
        """
        qs = message_agent_and_user_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_chats_in_queue",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying chats which are currently in queue",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_chats_in_queue")
    def chats_in_queue(self, request, *args, **kwargs):  # add
        """
        The chats_in_queue function is used to return the number of chats in queue for a given channel.
            The function takes in a request object and kwargs, which are then added to filter_data.
            today is set as 3 minutes ago from now, and tomorrow is set as now.
            qs filters SocialconversationTempsocialuser objects using the handoff database with channel values from filter_data's get method on 'channel'.  It also filters by tenant name (get_current_tenant_name()), last activity greater than or equal to today but less than or equal to tomorrow, and where it

        :param self: Represent the instance of the object itself
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of chats in the queue
        """
        qs = chats_in_queue_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_chats_in_queue_detail",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of chats which are currently in queue",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_chats_in_queue_detail")
    def chats_in_queue_detail(self, request, *args, **kwargs):  # add
        """
        The chats_in_queue_detail function is used to retrieve the number of chats in queue for a given channel.
            The function takes in a request and *args, **kwargs as parameters.
            It then filters the data based on the channel provided by kwargs and returns it as an object.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The username and timestamp of the user who is currently in queue
        """
        qs = chats_in_queue_detail_generic(request)
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_live_handoff_called_today",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total number of HandOff called Today",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_handoff_called_today")
    def handoff_called_today(self, request, *args, **kwargs):  # add
        """
        The handoff_called_today function is a custom function that returns the number of handoffs called today.
        It takes in a request object and kwargs, which are used to filter the data returned from the AnalyticsSocialevent model.
        The query filters by channel, tenant name (which is retrieved using get_current_tenant_name()), timestamp (today's date), and event type (&quot;handoff-initial&quot;).
        The count of all objects matching these criteria is then returned as JSON.

        :param seld: Access the serializer class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of handoffs called today
        """
        qs = handoff_called_today_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_agent_status",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Details of Agents who are online",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_agent_status")
    def online_detail(self, request, *args, **kwargs):
        """
        The online_detail function is used to get the list of agents who are online and ready for a conversation.
        The function takes in the request object, which contains information about the current HTTP request.
        It also takes in *args and **kwargs, which are used to pass additional arguments into a view function or method.
        The filter_data variable is set equal to all of the data contained within the request object (request.data).  The update() method then adds any additional keyword arguments that were passed into this view (**kwargs) onto filter_data as key-value pairs.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of agents that are online and their status
        """
        qs = online_detail_generic()
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_live_online_customers_agent",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Count of Agents who are online with Customer",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_live_online_customers_agent"
    )
    def online_customers_agent(self, request, *args, **kwargs):
        """
        The online_customers_agent function returns the number of customers currently online.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of online customers
        """
        qs = online_customers_agent_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_online_customers_bot",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Count of bots which are online with Customer",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_online_customers_bot")
    def online_customers_bot(self, request, *args, **kwargs):
        """
        The online_customers_bot function returns the number of unique users who have sent a message to the bot in the last minute.

        :param self: Access the class attributes and methods
        :param request: Get the data from the request
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A response object with a count of the number of unique channel_id values in messagelog objects that have a source value equal to &quot;user&quot; and are more recent than one minute ago
        """
        qs = online_customers_bot_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="agent_live_handoff_duration",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Time taken for handoff",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_live_handoff_duration"
    )  # Handoff Duration in Minutes
    def handoff_duration(self, request, *args, **kwargs):  # add
        """
        The handoff_duration function is a view that returns the total duration of handoffs for each user.
        The function takes in a request and *args, **kwargs as parameters. The filter_data variable is set to the data from the request object.
        The today variable is set to datetime now minus 3 minutes, and tomorrow is set to datetime now. The qs variable queries Handoffduration objects using
        the handoff database with a tenant equal to get_current_tenant_name(), where timestamp greater than or equal today and less than or equal tomorrow,
        and values username annotated by summing up all minutes

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total duration of handoff for each user
        """
        response = handoff_duration_generic()
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_live_last_activity_time",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Agents last Activity details",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_last_activity_time")
    def agent_last_activity_time(self, request, *args, **kwargs):  # add
        """
        The agent_last_activity_time function returns the last activity time of an agent.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The last activity time for all agents
        """
        response = agent_last_activity_time_generic()
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_live_ended_chats",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying chats which are closed by Agent Or User",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_ended_chats")
    def ended_chats(self, request, *args, **kwargs):  # add
        """
        The ended_chats function returns a list of all the chats that have ended in the last 3 minutes.
        The function takes in a request and *args, **kwargs as parameters. The filter_data variable is set to
        the data from the request object. The today variable is set to datetime now minus 3 minutes, and tomorrow
        is set to datetime now. A query string (qs) is created using AnalyticsSocialevent objects from handoff database,
        and filters are applied for channel(s), tenant name, timestamp between today and tomorrow variables (3 minute window),
        and event type(s). An annotation

        :param self: Represent the instance of the object itself
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries that contain the event name and the number of times it occurred
        """
        response = ended_chats_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="agent_live_skill",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition graph of each Agents Skills",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_skill")
    def agent_skill(self, request, *args, **kwargs):
        """
        The agent_skill function returns a list of agents and their skills.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The following:
        """
        response = agent_skill_generic()
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_live_ongoing_max_chats",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total number of chats Currently Online",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_ongoing_max_chats")
    def ongoing_max_chats(self, request, *args, **kwargs):
        """
        The ongoing_max_chats function returns a list of agents and their current number of ongoing chats.

        :param self: Allow an instance of a class to access its attributes and methods
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A table of agents and their current chats, max concurrent chats, and the difference between them
        """
        response = ongoing_max_chats_generic()
        return return_table(response, request)

    @extend_schema(
        operation_id="agent_live_current_loggedin_skills",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition graph of each Agents Skills who are currently Online",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_live_current_loggedin_skills"
    )
    def current_loggedin_skills(self, request, *args, **kwargs):
        """
        The current_loggedin_skills function returns a list of all the skills that are currently logged in.
        It also returns the number of agents who are currently logged into each skill.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of dicts, each containing the skill name and count
        """
        qs = current_loggedin_skills_generic()
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_live_abandoned_users_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of Users who were in user_fallout and canceled handoff after initiating",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_live_abandoned_users_details"
    )
    def abandoned_users_details_live(self, request, *args, **kwargs):
        """
        The abandoned_users_details_live function is used to get the abandoned users details.
            It takes in a request and returns a paginated response of the queryset.


        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of abandoned users
        """
        qs = abandoned_users_details_live_generic(request)
        return return_table(qs, request)

    # Number of Interactions Arrived per Agent
    @extend_schema(
        operation_id="agent_live_interaction_arrived",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Number of Interactions Arrived per Agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_interaction_arrived")
    def interaction_arrived_live(self, request, *args, **kwargs):
        """
        The interaction_arrived_live function is used to get the number of interactions that arrived for each agent in a given time period.
        The function takes in a request object and keyword arguments, which are then added to the filter_data dictionary.
        A datetime object is created using today's date minus 3 minutes, and another datetime object is created using today's date.
        A queryset (qs) is created by filtering SocialconversationAgenttenant objects on tenant name equal to the current tenant name,
        and values are annotated with username and id from Agent objects associated with those SocialconversationAgenttenant objects.  The

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries
        """
        items = interaction_live_generic(request, "handoff-notification")
        return return_table(items, request)

    # Number of Interactions Accepted per Agent
    @extend_schema(
        operation_id="agent_live_interaction_accepted",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Number of Interactions Accepted per Agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_interaction_accepted")
    def interaction_accepted_live(self, request, *args, **kwargs):
        """
        The interaction_accepted_live function is used to get the number of interactions accepted by an agent in a given time period.
        The function takes in a request object and keyword arguments, which are then added to the filter_data dictionary.
        A datetime object is created for today's date and tomorrow's date, which will be used as filters for our query set.
        We create a query set that gets all agents associated with the current tenant (which we get from our helper function).  We annotate this queryset so that it contains only two fields: username and id (the id field will be used later on).  We then convert this quer

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        items = interaction_live_generic(request, "agent-accept")
        return return_table(items, request)

    # Customer Conversations
    @extend_schema(
        operation_id="agent_live_conversations",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Customer Conversations Details",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_conversations")
    def conversations_live(self, request, *args, **kwargs):
        """
        The Conversations_live function is used to return a list of all conversations that have occurred in the last 3 minutes.
            It takes in a request object and returns an item object.

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries, where each dictionary represents a message
        """
        items = conversations_live_generic(request)
        return return_table(items, request)

    # Top 5 Recent Messages to BOT
    @extend_schema(
        operation_id="agent_live_topMessage",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Top 5 Recent Messages to BOT",
    )
    @action(methods=["POST"], detail=False, url_path="agent_live_topMessage")
    def top_messages_live(self, request, *args, **kwargs):
        """
        The top_messages_live function is a custom function that returns the top 5 messages sent by users in the last 3 minutes.
        It takes in a request object and kwargs, which are used to filter data based on channel and tenant.
        The result variable stores the query results from MessageLog objects filtered by channel, tenant, source (user), timestamp range (last 3 minutes),
        and message.
        The values() method is used to return only specific fields from each record.
        The annotate() method adds an additional

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of the top 5 messages that have been sent in the last 3 minutes
        """
        items = top_messages_live_generic(request)
        return return_table(items, request)
