from auth.tags import AuthTags
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from console.services.daily_traffic_utils import (
    total_users_periodic_generic,
    total_users_generic,
    total_sessions_periodic_generic,
    total_sessions_generic,
    sessions_per_users_periodic_generic,
    sessions_per_user_generic,
    message_per_session_periodic_generic,
    message_per_session_generic,
    total_session_time_periodic_generic,
    total_session_time_generic,
    handled_or_not_generic,
    handled_message_generic,
    unhandled_message_generic,
)

from main.utils.boiler_plate import get_generic_response, return_table
from main.utils.export import export_csv, export_pdf


class DailyTrafficViewSet(GenericViewSet):  # For Daily Traffic Report
    @extend_schema(
        operation_id="bot_daily_total_users_periodic",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_total_users_periodic")
    def total_users_periodic(self, request, *args, **kwargs):
        """
        The total_users_periodic function returns the total number of users that have interacted with a bot in a given time period.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of distinct users who have interacted with the bot
        """
        params = total_users_periodic_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_users_periodic_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_users_periodic_export_csv",
    )
    def total_users_periodic_export_csv(self, request, *args, **kwargs):
        params = total_users_periodic_generic(request)
        response = get_generic_response(params)
        items = export_csv([response.data], ["count"], "total_users_periodic.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_total_users_periodic_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_users_periodic_export_pdf",
    )
    def total_users_periodic_export_pdf(self, request, *args, **kwargs):
        params = total_users_periodic_generic(request)
        response = get_generic_response(params)
        items = export_pdf(
            [response.data],
            ["count"],
            "total_users_periodic.pdf",
            "Total Users(Periodic)",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_total_users_daily",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users compared to previous days",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_total_users_daily")
    def total_users(self, request, *args, **kwargs):
        """
        The total_users function returns the total number of users that have interacted with the bot.

        :param self: Represent the instance of a class
        :param request: Pass the request object to the function
        :param *args: Pass a variable number of arguments to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of users that have interacted with the bot
        """
        params = total_users_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_users_daily_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_users_daily_export_csv",
    )
    def total_users_export_csv(self, request, *args, **kwargs):
        params = total_users_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "total_users.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_users_daily_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total users compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_users_daily_export_pdf",
    )
    def total_users_export_pdf(self, request, *args, **kwargs):
        params = total_users_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "total_users.pdf",
                "title": "Total Users Daily",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_sessions_periodic",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_daily_total_sessions_periodic"
    )
    def total_sessions_periodic(self, request, *args, **kwargs):
        """
        The total_sessions_periodic function returns the total number of sessions for a given time period.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of sessions that have occurred in the last 24 hours
        """
        params = total_sessions_periodic_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_sessions_periodic_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_sessions_periodic_export_csv",
    )
    def total_sessions_periodic_export_csv(self, request, *args, **kwargs):
        params = total_sessions_periodic_generic(request)
        response = get_generic_response(params)
        items = export_csv([response.data], ["count"], "total_sessions_periodic.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_total_sessions_periodic_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_sessions_periodic_export_pdf",
    )
    def total_sessions_periodic_export_pdf(self, request, *args, **kwargs):
        params = total_sessions_periodic_generic(request)
        response = get_generic_response(params)
        items = export_pdf(
            [response.data],
            ["count"],
            "total_sessions_periodic.pdf",
            "Total Sessions(Periodic)",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_total_sessions_daily",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions compared to previous days",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_total_sessions_daily")
    def total_sessions(self, request, *args, **kwargs):
        """
        The total_sessions function returns the total number of sessions for a given date range.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of sessions in a given time period
        """
        params = total_sessions_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_sessions_daily_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_sessions_daily_export_csv",
    )
    def total_sessions_export_csv(self, request, *args, **kwargs):
        params = total_sessions_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "total_sessions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_total_sessions_daily_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total sessions compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_sessions_daily_export_pdf",
    )
    def total_sessions_export_pdf(self, request, *args, **kwargs):
        params = total_sessions_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "total_sessions.pdf",
                "title": "Total Sessions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_sessions_per_users_periodic",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_daily_sessions_per_users_periodic"
    )
    def sessions_per_users_periodic(self, request, *args, **kwargs):
        """
        The sessions_per_users_periodic function is a custom function that returns the average number of sessions per user for a given time period.

        :param self: Represent the instance of a class
        :param request: Get the tenant name from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average number of sessions per user
        """
        try:
            params = sessions_per_users_periodic_generic(request)
            return Response(get_generic_response(params))
        except Exception:
            return Response(data={"count": 0})

    @extend_schema(
        operation_id="bot_daily_sessions_per_users_periodic_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_sessions_per_users_periodic_export_csv",
    )
    def sessions_per_users_periodic_export_csv(self, request, *args, **kwargs):
        try:
            params = sessions_per_users_periodic_generic(request)
            response = Response(get_generic_response(params))
        except Exception:
            response = Response(data={"count": 0})
        items = export_csv(
            [response.data], ["count"], "sessions_per_users_periodic.csv"
        )
        return items

    @extend_schema(
        operation_id="bot_daily_sessions_per_users_periodic_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_sessions_per_users_periodic_export_pdf",
    )
    def sessions_per_users_periodic_export_pdf(self, request, *args, **kwargs):
        try:
            params = sessions_per_users_periodic_generic(request)
            response = Response(get_generic_response(params))
        except Exception:
            response = Response(data={"count": 0})
        items = export_pdf(
            [response.data],
            ["count"],
            "sessions_per_users_periodic.pdf",
            "Sessions per User(Periodic)",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_sessions_per_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user compared to previous days",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_sessions_per_users")
    def sessions_per_user(self, request, *args, **kwargs):
        """
        The sessions_per_user function returns the number of sessions per user.

        :param self: Refer to the class itself
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average number of sessions per user
        """
        params = sessions_per_user_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_sessions_per_users_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_sessions_per_users_export_csv",
    )
    def sessions_per_user_export_csv(self, request, *args, **kwargs):
        params = sessions_per_user_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "sessions_per_user.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_sessions_per_users_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of sessions per user compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_sessions_per_users_export_pdf",
    )
    def sessions_per_user_export_pdf(self, request, *args, **kwargs):
        params = sessions_per_user_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Date", "count"],
                "fileName": "sessions_per_user.pdf",
                "title": "Sessions per User",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_message_per_session_periodic",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_message_per_session_periodic",
    )
    def message_per_session_periodic(self, request, *args, **kwargs):
        """
        The message_per_session_periodic function is a custom function that returns the average number of messages per session.
        It takes in a request object and uses it to get the current tenant name, which is used to filter out data from other tenants.
        The function then creates a dictionary called params, which contains all of the information needed for get_generic_response()
        to return an appropriate response. The params dictionary contains:

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average number of messages per session
        """
        res = message_per_session_periodic_generic(request)
        return Response(data={"count": res})

    @extend_schema(
        operation_id="bot_daily_message_per_session_periodic_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_message_per_session_periodic_export_csv",
    )
    def message_per_session_periodic_export_csv(self, request, *args, **kwargs):
        res = message_per_session_periodic_generic(request)
        response = Response(data={"count": res})
        items = export_csv(
            [response.data], ["count"], "sessions_per_users_periodic.csv"
        )
        return items

    @extend_schema(
        operation_id="bot_daily_message_per_session_periodic_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_message_per_session_periodic_export_pdf",
    )
    def message_per_session_periodic_export_pdf(self, request, *args, **kwargs):
        res = message_per_session_periodic_generic(request)
        response = Response(data={"count": res})
        items = export_pdf(
            [response.data],
            ["count"],
            "messages_per_users_periodic.pdf",
            "Messages per Session(Periodic)",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_message_per_session",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session compared to previous days",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_message_per_session")
    def message_per_session(self, request, *args, **kwargs):
        """
        The message_per_session function is a generic function that returns the average number of messages per session.
        It takes in a request object and uses it to get the current tenant name, which is used to filter out all other tenants' data.
        The params dictionary contains all of the parameters needed for this function:
            - The request parameter allows us to use Django's built-in authentication system, which we need in order to get
                information about our current user (i.e., their tenant name). This parameter will be passed into every generic
                function as well as any custom functions that are called by them.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average number of messages per session
        """
        try:
            res, _, _ = message_per_session_generic(request)
            return Response(res)
        except Exception as e:
            return []

    @extend_schema(
        operation_id="bot_daily_message_per_session_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_message_per_session_export_csv",
    )
    def message_per_session_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = message_per_session_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_message_per_session_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying number of messages per session compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_message_per_session_export_pdf",
    )
    def message_per_session_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = message_per_session_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Messages per Session",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_total_session_time_periodic",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_daily_total_session_time_periodic"
    )
    def total_session_time_periodic(self, request, *args, **kwargs):
        """
        The total_session_time_periodic function is a custom function that calculates the total session time for all users in minutes.
            It takes in a request object and returns the total session time as an integer value.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total session time in minutes
        """
        display_total_time, int_total_time = total_session_time_periodic_generic(
            request
        )
        return Response(data={"count": int_total_time, "display": display_total_time})

    @extend_schema(
        operation_id="bot_daily_total_session_time_periodic_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_session_time_periodic_export_csv",
    )
    def total_session_time_periodic_export_csv(self, request, *args, **kwargs):
        total_time, _ = total_session_time_periodic_generic(request)
        response = Response(data={"count": total_time})
        items = export_csv(
            [response.data], ["count"], "total_session_time_periodic.csv"
        )
        return items

    @extend_schema(
        operation_id="bot_daily_total_session_time_periodic_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_session_time_periodic_export_pdf",
    )
    def total_session_time_periodic_export_pdf(self, request, *args, **kwargs):
        total_time, _ = total_session_time_periodic_generic(request)
        response = Response(data={"count": total_time})
        items = export_pdf(
            [response.data],
            ["count"],
            "total_session_time_periodic.pdf",
            "Total Session Time(Periodic)",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_total_session_time",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time compared to previous days",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_total_session_time")
    def total_session_time(self, request, *args, **kwargs):
        """
        The total_session_time function returns the total session time in minutes for each day.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The total time spent by the user on the website
        """
        result, _, _, _ = total_session_time_generic(request)
        return Response(result)

    @extend_schema(
        operation_id="bot_daily_total_session_time_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_session_time_export_csv",
    )
    def total_session_time_export_csv(self, request, *args, **kwargs):
        _, result, field_names, file_name = total_session_time_generic(request)
        items = export_csv(result, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_total_session_time_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total session time compared to previous days",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_total_session_time_export_pdf",
    )
    def total_session_time_export_pdf(self, request, *args, **kwargs):
        _, result, field_names, file_name = total_session_time_generic(request)
        if len(result) > settings.MAX_PDF_LIMIT:
            result = result[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            result,
            field_names,
            f"{file_name}.pdf",
            "Total Session Time Daily",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_handled_or_not",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying pie chart of handled and not handled",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_handled_or_not")
    def handled_or_not(self, request, *args, **kwargs):
        """
        The handled_or_not function is a viewset that returns the number of messages
        that were handled by an agent and the number of messages that were not handled.
        It does this by querying the MessageLog table for all user-generated messages,
        and then counting how many are marked as &quot;handled&quot; or &quot;not_handled&quot;. It then
        returns these counts in a JSON object.

        :param self: Refer to the object itself
        :param request: Get the query string from the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A queryset of the number of messages that were handled and not handled
        """
        params = handled_or_not_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="bot_daily_top5_handled_msg",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying top 5 handled data",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_top5_handled_msg")
    def handled_message(self, request, *args, **kwargs):
        """
        The handled_message function returns a table of the top 5 most frequently handled messages.
        The function takes in a request object and uses it to get the queryset from which we will pull our data.
        We then filter that queryset by source, tenant, and whether or not the message was handled (Y). We also exclude any messages; or &quot;/&quot;. This is because these are system-generated messages used for routing purposes only.
        Next we use values() to return an array of dictionaries containing just the message field and count field (the number of times each message has been sent). We then order this

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A table with the top 5 messages that have been handled
        """
        items, _, _ = handled_message_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_daily_top5_handled_msg_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying top 5 handled data",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_daily_top5_handled_msg_export_csv"
    )
    def handled_msg_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = handled_message_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_top5_handled_msg_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying top 5 handled data",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_daily_top5_handled_msg_export_pdf"
    )
    def handled_msg_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = handled_message_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Handled Messages",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_daily_top5_unhandled_msg",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition chart for unhandled data",
    )
    @action(methods=["POST"], detail=False, url_path="bot_daily_top5_unhandled_msg")
    def unhandled_message(self, request, *args, **kwargs):
        """
        The unhandled_message function returns a table of the top 5 unhandled messages from users.
            The function takes in a request object and uses it to get the queryset for MessageLogs.
            It then filters out all handled messages, and any message containing '/'.
            This is done because these are not user-generated messages.  Then it counts how many times each message appears in the logs, orders them by count descendingly, and returns only the top 5.

        :param self: Refer to the class itself
        :param request: Get the request object that is sent to the server
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A table of the top 5 unhandled messages
        """
        items, _, _ = unhandled_message_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="bot_daily_top5_unhandled_msg_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition chart for unhandled data",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_top5_unhandled_msg_export_csv",
    )
    def unhandled_msg_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = unhandled_message_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_daily_top5_unhandled_msg_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition chart for unhandled data",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_daily_top5_unhandled_msg_export_pdf",
    )
    def unhandled_msg_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = unhandled_message_generic(request)
        if len(response) > settings.MAX_PDF_LIMIT:
            response = response[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Unhandled Messages",
            request.user.username,
        )
        return items
