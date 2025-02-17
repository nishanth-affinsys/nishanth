from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from console.services.report_at_glance_utils import (
    active_customer_generic,
    session_per_day_generic,
    session_per_user_generic,
    message_per_session_generic,
    average_session_time_linechart_generic,
)
from main.utils.export import export_csv, export_pdf
from django.conf import settings


class ReportsAtGlanceViewSet(GenericViewSet):  # For Reports at a Glance
    # All line chart ordered by date is ascending order
    @extend_schema(
        operation_id="bot_report_active_customers_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Active Customers",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_report_active_customers_linechart"
    )
    def active_customer(self, request, *args, **kwargs):
        """
        The active_customer function returns a list of active customers for the given date range.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of active customers per day
        """
        qs, _, _ = active_customer_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="bot_report_active_customers_linechart_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Active Customers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_active_customers_linechart_export_csv",
    )
    def active_customer_linechart_export_csv(self, request, *args, **kwargs):
        qs, field_names, file_name = active_customer_generic(request)
        items = export_csv(qs, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_report_active_customers_linechart_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Active Customers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_active_customers_linechart_export_pdf",
    )
    def active_customer_linechart_export_pdf(self, request, *args, **kwargs):
        qs, field_names, file_name = active_customer_generic(request)
        if len(qs) > settings.MAX_PDF_LIMIT:
            qs = qs[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            qs,
            field_names,
            f"{file_name}.pdf",
            "Active Customers",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_report_no_of_sessions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per Day",
    )
    @action(methods=["POST"], detail=False, url_path="bot_report_no_of_sessions")
    def session_per_day(self, request, *args, **kwargs):
        """
        The session_per_day function returns a list of dictionaries containing the date and total number of sessions per day.
        The function takes in a request object, which is used to get the filter data from the frontend. The filter data contains
        the timestamp range and channel(s) that are selected by the user on the frontend. The query set filters out any messages
        that contain &quot;agent_&quot; or &quot;/&quot;, as these are not actual customer messages, but rather agent responses or system generated
        messages (such as when an agent joins/leaves a chat). It also filters out any message logs that do not belong to this tenant

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries with the date and total number of sessions for that day
        """
        qs, _, _ = session_per_day_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="bot_report_no_of_sessions_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per Day",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_report_no_of_sessions_export_csv"
    )
    def session_per_day_export_csv(self, request, *args, **kwargs):
        qs, field_names, file_name = session_per_day_generic(request)
        items = export_csv(qs, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_report_no_of_sessions_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per Day",
    )
    @action(
        methods=["POST"], detail=False, url_path="bot_report_no_of_sessions_export_pdf"
    )
    def session_per_day_export_pdf(self, request, *args, **kwargs):
        qs, field_names, file_name = session_per_day_generic(request)
        if len(qs) > settings.MAX_PDF_LIMIT:
            qs = qs[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            qs,
            field_names,
            f"{file_name}.pdf",
            "Number of Sessions",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_report_session_per_user",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per User",
    )
    @action(methods=["POST"], detail=False, url_path="bot_report_session_per_user")
    def session_per_user(self, request, *args, **kwargs):
        """
        The session_per_user function is a custom function that returns the average number of sessions per user for each day in the specified date range.

        :param self: Refer to the current instance of a class
        :param request: Get the data from the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A query set that contains the number of sessions per user
        """
        qs, _, _ = session_per_user_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="bot_report_session_per_user_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per User",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_session_per_user_export_csv",
    )
    def session_per_user_export_csv(self, request, *args, **kwargs):
        qs, field_names, file_name = session_per_user_generic(request)
        items = export_csv(qs, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_report_session_per_user_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Sessions per User",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_session_per_user_export_pdf",
    )
    def session_per_user_export_pdf(self, request, *args, **kwargs):
        qs, field_names, file_name = session_per_user_generic(request)
        if len(qs) > settings.MAX_PDF_LIMIT:
            qs = qs[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            qs,
            field_names,
            f"{file_name}.pdf",
            "Sessions per User",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_report_message_per_session_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Messages per Session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_message_per_session_linechart",
    )
    def message_per_session(self, request, *args, **kwargs):
        """
        The message_per_session function returns the average number of messages per session for a given time period.
        The function takes in two parameters: start_date and end_date, which are both strings formatted as YYYY-MM-DD.
        It then filters the MessageLog table by those dates, and counts the number of messages divided by
        the number of unique sessions to get an average.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average number of messages per session
        """
        qs, _, _ = message_per_session_generic(request)
        return Response(qs)

    @extend_schema(
        operation_id="bot_report_message_per_session_linechart_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Messages per Session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_message_per_session_linechart_export_csv",
    )
    def message_per_session_export_csv(self, request, *args, **kwargs):
        qs, field_names, file_name = message_per_session_generic(request)
        items = export_csv(qs, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_report_message_per_session_linechart_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Total Messages per Session",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_message_per_session_linechart_export_pdf",
    )
    def message_per_session_export_pdf(self, request, *args, **kwargs):
        qs, field_names, file_name = message_per_session_generic(request)
        if len(qs) > settings.MAX_PDF_LIMIT:
            qs = qs[: settings.MAX_PDF_LIMIT]
        items = export_pdf(
            qs,
            field_names,
            f"{file_name}.pdf",
            "Messages per Session",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="bot_report_average_session_time_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Average Session time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_average_session_time_linechart",
    )
    def average_session_time_linechart(self, request, *args, **kwargs):
        """
        The average_session_time_linechart function is used to calculate the average session time for each day in a given date range.
        The function takes in a request object and keyword arguments, which are then added to the filter_data dictionary.
        A query set is created using MessageLog objects from the event database, filtered by timestamp__range and channel values passed into
        the function via kwargs. The query set also filters out messages that contain &quot;agent_&quot; or &quot;/&quot;. The tenant name of the current user
        is also added as a filter value. Values are selected from this queryset based on session id and date (timestamp casted as

        :param self: Represent the instance of the class
        :param request: Get the request data from the frontend
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The average session time for each day in the specified date range
        """
        response, _, _, _ = average_session_time_linechart_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="bot_report_average_session_time_linechart_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Average Session time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_average_session_time_linechart_export_csv",
    )
    def average_session_time_linechart_export_csv(self, request, *args, **kwargs):
        _, response, field_names, file_name = average_session_time_linechart_generic(
            request
        )
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="bot_report_average_session_time_linechart_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Average Session time",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="bot_report_average_session_time_linechart_export_pdf",
    )
    def average_session_time_linechart_export_pdf(self, request, *args, **kwargs):
        _, response, field_names, file_name = average_session_time_linechart_generic(
            request
        )
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
