from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from handoff.services.agent_transfer_utils import (
    total_transfer_initiated_bigno_generic,
    total_successful_transfer_bigno_generic,
    total_failed_transfer_bigno_generic,
    transfers_initiated_linechart_generic,
    transfers_accepted_linechart_generic,
    transfers_failed_linechart_generic,
    agent_initiated_transfers_generic,
    transfer_details_generic,
    only_transfer_details_generic,
)

from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import (
    return_table,
    get_generic_response,
)

from main.utils.export import export_csv, export_pdf


class AgentTransferViewSet(GenericViewSet):
    # Total transfer initiated agent transfers
    @extend_schema(
        operation_id="agent_transfer_total_transfer_initiated",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of transfers initiated",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_transfer_total_transfer_initiated",
    )
    def total_transfer_initiated_bigno(self, request, *args, **kwargs):
        """
        The total_transfer_initiated_bigNo function returns the total number of transfers initiated by agents.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of transfers initiated by agents
        """
        params = total_transfer_initiated_bigno_generic(request)
        return get_generic_response(params)

    # Total successful agent transfers
    @extend_schema(
        operation_id="agent_transfer_total_successful",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of successful transfers",
    )
    @action(methods=["POST"], detail=False, url_path="agent_transfer_total_successful")
    def total_successful_transfer_bigno(self, request, *args, **kwargs):
        """
        The total_successful_transfer_bigNo function returns the total number of successful agent transfers.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of failed agent transfers
        """
        params = total_successful_transfer_bigno_generic(request)
        return get_generic_response(params)

    # Total failed agent transfers
    @extend_schema(
        operation_id="agent_transfer_total_failed",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of failed transfers",
    )
    @action(methods=["POST"], detail=False, url_path="agent_transfer_total_failed")
    def total_failed_transfer_bigno(self, request, *args, **kwargs):
        """
        The total_failed_transfer_bigNo function returns the total number of failed transfers for a given tenant.
            ---
            # YAML (must be separated by `---`)

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of failed transfers
        """
        params = total_failed_transfer_bigno_generic(request)
        return get_generic_response(params)

    # transfer initiated linechart by date
    @extend_schema(
        operation_id="agent_transfer_initiated_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of transfers initiated ",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_transfer_initiated_linechart"
    )
    def transfers_initiated_linechart(self, request, *args, **kwargs):
        """
        The transfers_initiated_linechart function returns a linechart of the number of transfers initiated by date.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A linechart of the number of transfers initiated by date
        """
        params = transfers_initiated_linechart_generic(request)
        return get_generic_response(params)

    # transfer accepted linechart by date
    @extend_schema(
        operation_id="agent_transfer_successful_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of transfers initiated ",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_transfer_successful_linechart"
    )
    def transfers_accepted_linechart(self, request, *args, **kwargs):
        """
        The transfers_accepted_linechart function is a viewset that returns the number of transfers accepted by agents on a given day.
        The function takes in an HTTP request and returns an HTTP response containing the data requested.


        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of transfers accepted by an agent
        """
        params = transfers_accepted_linechart_generic(request)
        return get_generic_response(params)

    # transfer failed linechart by date
    @extend_schema(
        operation_id="agent_transfer_failed_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Total number of transfers initiated ",
    )
    @action(methods=["POST"], detail=False, url_path="agent_transfer_failed_linechart")
    def transfers_failed_linechart(self, request, *args, **kwargs):
        """
        The transfers_failed_linechart function is used to generate a line chart of the number of failed transfers per day.
        The function takes in a request object and returns an HTTP response containing the data for the line chart.


        :param self: Represent the instance of a class
        :param request: Get the current request
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A line chart of the number of failed transfers per day
        """
        params = transfers_failed_linechart_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_transfer_initiated_transfer",
        tags=[AuthTags.AUTHORIZE],
        description="Total number transfer the agent has initiated",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_transfer_initiated_transfer"
    )
    def agent_initiated_transfers(self, request, *args, **kwargs):
        """
        The agent_initiated_transfers function is a viewset that returns the number of times an agent has initiated a transfer.
        The function takes in request data and kwargs, which are used to filter the query set. The query set is then filtered by tenant name, event type (handoff-transfer-from), and parent session id (to exclude any sessions that were not transferred).
        The values() method filters out all columns except for Agent_Name and count. The annotate() method counts how many times each agent's name appears in the table.

        :param self: Allow an instance of a class to access its own attributes and methods
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries
        """
        items = agent_initiated_transfers_generic(request)
        return Response(items)

    @extend_schema(
        operation_id="agent_report_handoff_transfer_details",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_report_handoff_transfer_details"
    )
    def transfer_details(self, request, *args, **kwargs):
        """
        The transfer_details function is used to return a list of all transfers that have occurred within the specified time range.
        The function takes in a request object and kwargs, which are then added to filter_data. The values dictionary contains the
        fields we want returned from our query, along with their aliases (the keys). We use Cast() to convert the datetime fields into
        strings so they can be displayed properly in our table. The qs variable holds our queryset, which filters on channel and timestamp__range
        (which is passed as part of kwargs), excludes any records where initial_agent contains &quot;{

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries
        """
        qs, _, _ = transfer_details_generic(request)
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_report_handoff_transfer_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_handoff_transfer_details_export_csv",
    )
    def transfer_details_export(self, request, *args, **kwargs):
        """
        The transfer_details_export function is used to export the data from the AgentTransfer model.
        The function takes in a request and *args, **kwargs as parameters. The filter_data variable is set equal to
        the request data and then updated with kwargs. The values dictionary contains two keys: Initialized_time and Total_session_time, which are both set equal to Cast objects that take in Trunc objects as their first parameter (Trunc object for Initialized time also takes in tzinfo=tzinfo).
        The qs variable is set equal to an AgentTransfer queryset that filters on channel__in

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A csv file
        """
        response, field_names, file_name = transfer_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_report_handoff_transfer_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_report_handoff_transfer_details_export_pdf",
    )
    def transfer_details_export_pdf(self, request, *args, **kwargs):
        """
        The transfer_details_export_pdf function is used to export the agent transfer details in a PDF format.
        The function takes in the request and kwargs as parameters, and returns an item.


        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A tuple of two items
        """
        response, field_names, file_name = transfer_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Handoff Duration",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="agent_transfer_details_only",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer",
    )
    @action(methods=["POST"], detail=False, url_path="agent_transfer_details_only")
    def only_transfer_details(self, request, *args, **kwargs):
        """
        The only_transfer_details function is used to return a list of all transfers that have occurred
            within the specified time range. The function takes in a request object and kwargs, which are
            then added to the filter_data dictionary. The values dictionary contains several fields that are
            truncated and casted into strings for easier display on the front end. A query set is created using
            these values, filtering by channel and timestamp__range (which comes from kwargs). This query set is then passed through
            return_table() which returns an items object containing data about each transfer.

        :param self: Represent the instance of the class
        :param request: Get the data from the frontend
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass in keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        qs, _, _ = only_transfer_details_generic(request)
        return return_table(qs, request)

    @extend_schema(
        operation_id="agent_transfer_details_only_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_transfer_details_only_export_csv",
    )
    def only_transfer_details_export(self, request, *args, **kwargs):
        """
        The only_transfer_details_export function is used to export the agent transfer details.

        :param self: Represent the instance of the class
        :param request: Get the data from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names, file_name = only_transfer_details_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="agent_transfer_details_only_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Details of the agent transfer",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_transfer_details_only_export_pdf",
    )
    def only_transfer_details_export_pdf(self, request, *args, **kwargs):
        """
        The only_transfer_details_export_pdf function is used to export the data from the AgentTransfer model into a PDF file.
        The function takes in request and kwargs as parameters, and returns items. The function first creates a tz_info variable that stores
        the timezone information for the current tenant's timezone setting. It then creates a filter_data variable that stores all of
        the data passed in through request, which includes channel and timestamp__range values (which are used to filter out specific rows).
        It then creates an empty dictionary called values, which will be populated with key-value pairs later on in this function. Next it uses

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The items that are exported in the pdf
        """
        response, field_names, file_name = only_transfer_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Agent Transfer Details",
            request.user.username,
        )
        return items
