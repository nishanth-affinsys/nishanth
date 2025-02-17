from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from handoff.services.agent_productivity_utils import (
    agent_routing_generic,
    agent_login_status_generic,
    agent_availability_generic,
)
from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import return_table
from handoff.serializers import AgentReportSerializer

from main.utils.export import export_csv, export_pdf


class AgentProductivityViewSet(GenericViewSet):
    serializer_class = AgentReportSerializer

    @extend_schema(
        operation_id="agent_report_agent_routing_details",
        tags=[AuthTags.AUTHORIZE],
        description="detailed report of agent routing",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_agent_routing_details"
    )
    def agent_routing(self, request, *args, **kwargs):
        """
        The agent_routing function is used to return a list of all agent routing data.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A queryset
        """
        items, _, _ = agent_routing_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="agent_report_agent_routing_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent routing",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_routing_details_export_csv",
    )
    def agent_routing_export(self, request, *args, **kwargs):
        """
        The agent_routing_export function is used to export the agent routing data in a csv file.
        The function takes in the request and kwargs as parameters. The filter_data variable stores
        the request data and updates it with kwargs. The values dictionary contains two key-value pairs,
        one for accepted time(Seconds) and one for initialized time. The qs variable stores all of the
        queryset information that will be exported into a csv file using export_csv(). It filters by channel,
        initial time range, tenant name (using get_current_tenant()), username, agent routed

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: An iterator
        """
        response, field_names, file_name = agent_routing_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_report_agent_routing_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent routing",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_routing_details_export_pdf",
    )
    def agent_routing_export_pdf(self, request, *args, **kwargs):
        """
        The agent_routing_export_pdf function is used to export the agent routing data in a PDF format.
        The function takes in the request and kwargs as parameters, and returns an iterator object.


        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: An iterator
        """
        response, field_names, file_name = agent_routing_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Agent Routing",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_report_agent_login_status",
        tags=[AuthTags.AUTHORIZE],
        description="detailed report agent login status",
    )
    @action(methods=["POST"], detail=False, url_path="agent_report_agent_login_status")
    def agent_login_status(self, request, *args, **kwargs):
        """
        The agent_login_status function is used to return a table of agent login status.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A table with the agent name, status and timestamp
        """
        items, _, _ = agent_login_status_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="agent_report_agent_login_status_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent login status report",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_login_status_export_csv",
    )
    def agent_login_status_export(self, request, *args, **kwargs):
        """
        The agent_login_status_export function is used to export the agent login status data.

        :param self: Represent the instance of the class
        :param request: Get the request data from the user
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The agent_login_status
        """
        response, field_names, file_name = agent_login_status_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_report_agent_login_status_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent login status report",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_login_status_export_pdf",
    )
    def agent_login_status_export_pdf(self, request, *args, **kwargs):
        """
        The agent_login_status_export_pdf function is used to export the agent login status data in a PDF format.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        response, field_names, file_name = agent_login_status_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Agent Login Status",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_report_agent_availability",
        tags=[AuthTags.AUTHORIZE],
        description="detailed report agent online status",
    )
    @action(methods=["POST"], detail=False, url_path="agent_report_agent_availability")
    def agent_availability(self, request, *args, **kwargs):
        """
        The agent_availability function is used to return a table of agent availability data.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A table of agents and their availability
        """
        items, _, _ = agent_availability_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="agent_report_agent_availability_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent availability status report",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_availability_export_csv",
    )
    def agent_availability_export(self, request, *args, **kwargs):
        """
        The agent_availability_export function is used to export the agent availability status.
            The function takes in a request and *args, **kwargs as parameters.
            It then filters the data based on timestamp range and changes that contain 'is_ready'.
            It then annotates the query set with a Timestamp field which is casted to CharField().
            The values are filtered by object_id, object_repr, changes and Timestamp.

        :param self: Represent the instance of a class
        :param request: Get the request data from the user
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A generator object
        """
        response, field_names, file_name = agent_availability_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_report_agent_availability_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="downloading detailed report of agent availability status report",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_agent_availability_export_pdf",
    )
    def agent_availability_export_pdf(self, request, *args, **kwargs):
        """
        The agent_availability_export_pdf function is used to export the agent availability status in a PDF format.
            The function takes in the request and kwargs as parameters, and returns an iterator object that can be used to
            stream data from a database or other source. The function first filters out all of the log entries that contain
            changes related to whether or not an agent is ready for work, then it annotates each entry with its timestamp
            truncated down to seconds (to avoid having multiple entries for every second). It then creates a list of dictionaries,
            where each dictionary contains information about one log entry:

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: An iterator
        """
        response, field_names, file_name = agent_availability_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Agent Availability Status",
            request.user.username,
        )
        return items
