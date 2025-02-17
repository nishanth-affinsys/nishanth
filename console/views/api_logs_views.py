from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from console.services.api_logs_utils import (
    api_calls_generic,
    api_details_generic,
    api_exceptions_generic,
    api_stage_details_generic,
)

from main.utils.boiler_plate import get_generic_response


class ApiLogsChartsViewSet(GenericViewSet):  # For ApiLog Report
    # Total Calls for particular API and their count
    @extend_schema(
        operation_id="api_calls",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Calls for particular API",
    )
    @action(methods=["POST"], detail=False, url_path="api_calls")
    def api_calls(self, request, *args, **kwargs):
        """
        The api_calls function returns a list of the most frequently called APIs.

        :param self: Represent the instance of the class
        :param request: Get the request object, which is used to get the query parameters from it
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of the api calls made by the user
        """
        params = api_calls_generic(request)
        return get_generic_response(params)

    # API Calls export csv format
    @extend_schema(
        operation_id="api_calls_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Total Calls for particular API in csv formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_calls_export_csv")
    def api_calls_export(self, request, *args, **kwargs):
        """
        The api_calls_export function is a view that returns the total number of API calls made by each API.
        It takes in a request, and then uses query to get all ApiLog objects from the database.
        It filters out any ApiLogs that are not associated with the current tenant, and then groups them by their api
        field (which is an F expression). Then it counts how many times each api appears in this group, and orders them
        by descending count, finally it exports these items as a csv file.

        :param self: Represent the instance of the object itself
        :param request: Get the query parameters from the request
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A generator object
        """
        params = api_calls_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["API", "count"],
                "fileName": "total_api_calls.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_calls_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Total Calls for particular API in pdf formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_calls_export_pdf")
    def api_calls_export_pdf(self, request, *args, **kwargs):
        """
        The api_calls_export_pdf function is used to export the total number of API calls made by a tenant.
        The function takes in a request object and returns an iterator that can be used to generate the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The export_pdf function
        """
        params = api_calls_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["API", "count"],
                "fileName": "total_api_calls.pdf",
                "title": "Total API Calls",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # API Details
    @extend_schema(
        operation_id="api_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of APIs",
    )
    @action(methods=["POST"], detail=False, url_path="api_details")
    def api_details(self, request, *args, **kwargs):
        """
        The api_details function is a view that returns the API logs for the current tenant.
        The function takes in a request object and uses it to get query parameters from the URL.
        It then uses these query parameters to filter down an ApiLogsSerializer queryset, which is
        then used to create a table of data using return_table(). The table of data is returned by
        the function.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The api details in the form of a table
        """
        params = api_details_generic(request)
        return get_generic_response(params)

    # API Details export csv format
    @extend_schema(
        operation_id="api_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of APIs in csv formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_details_export_csv")
    def api_details_export(self, request, *args, **kwargs):
        """
        The api_details_export function is used to export the api_details table as a csv file.
        The function takes in a request object and returns an iterator that can be used to create the csv file.


        :param self: Represent the instance of the class
        :param request: Get the query parameters from the url
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following fields:
        """
        params = api_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Stage",
                    "Status",
                    "Endpoint",
                    "Channel",
                    "Timestamp",
                ],
                "fileName": "api_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of APIs in pdf formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_details_export_pdf")
    def api_details_export_pdf(self, request, *args, **kwargs):
        """
        The api_details_export_pdf function is used to export the api_details table as a PDF file.
        The function takes in a request object and returns an iterator that can be used to download the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = api_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Stage",
                    "Status",
                    "Endpoint",
                    "Channel",
                    "Timestamp",
                ],
                "fileName": "api_details.pdf",
                "title": "API Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # API Exceptions
    @extend_schema(
        operation_id="api_exceptions",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of API exceptions",
    )
    @action(methods=["POST"], detail=False, url_path="api_exceptions")
    def api_exceptions(self, request, *args, **kwargs):
        """
        The api_exceptions function is a view that returns the API logs with exceptions.
        It takes in a request and returns an HTML table of the API logs with exceptions.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of all the exceptions that have occured in the api
        """
        params = api_exceptions_generic(request)
        return get_generic_response(params)

    # API Exceptions export csv format
    @extend_schema(
        operation_id="api_exceptions_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API exceptions in csv formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_exceptions_export_csv")
    def api_exceptions_export(self, request, *args, **kwargs):
        """
        The api_exceptions_export function is used to export the api exceptions data from the database.
        The function takes in a request object and returns an iterator of csv rows.


        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = api_exceptions_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Stage",
                    "Status",
                    "Exception",
                    "Details",
                    "Channel",
                    "Timestamp",
                ],
                "fileName": "api_exceptions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_exceptions_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API exceptions in pdf formate",
    )
    @action(methods=["POST"], detail=False, url_path="api_exceptions_export_pdf")
    def api_exceptions_export_pdf(self, request, *args, **kwargs):
        """
        The api_exceptions_export_pdf function is used to export the API Exceptions table as a PDF file.
        The function takes in a request object and returns an iterator that can be used to download the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the query string from the request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the api exceptions
        """
        params = api_exceptions_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Stage",
                    "Status",
                    "Exception",
                    # "Details",
                    "Channel",
                    "Timestamp",
                ],
                "fileName": "api_exceptions.pdf",
                "title": "API Exceptions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_response_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of API response details",
    )
    @action(methods=["POST"], detail=False, url_path="api_response_details")
    def api_response_details(self, request, *args, **kwargs):
        params = api_stage_details_generic(request, "Response")
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_response_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API response in csv format",
    )
    @action(methods=["POST"], detail=False, url_path="api_response_details_export_csv")
    def api_response_details_export_csv(self, request, *args, **kwargs):
        params = api_stage_details_generic(
            request,
            "Response",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Endpoint",
                    "Status",
                    "Details",
                    "Request_Id",
                    "Session_Id",
                    "Channel_Id",
                    "Channel",
                    "Exception",
                    "External_reference",
                    "Timestamp",
                ],
                "fileName": "api_response_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_response_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API response in pdf format",
    )
    @action(methods=["POST"], detail=False, url_path="api_response_details_export_pdf")
    def api_response_details_export_pdf(self, request, *args, **kwargs):
        params = api_stage_details_generic(
            request,
            "Response",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Endpoint",
                    "Status",
                    "Details",
                    "Request_Id",
                    "Session_Id",
                    "Channel_Id",
                    "Channel",
                    "Exception",
                    "External_reference",
                    "Timestamp",
                ],
                "fileName": "api_response_details.pdf",
                "title": "API Response Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # request details
    @extend_schema(
        operation_id="api_request_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of API response details",
    )
    @action(methods=["POST"], detail=False, url_path="api_request_details")
    def api_request_details(self, request, *args, **kwargs):
        params = api_stage_details_generic(request, "Request")
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_request_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API request in csv format",
    )
    @action(methods=["POST"], detail=False, url_path="api_request_details_export_csv")
    def api_request_details_export_csv(self, request, *args, **kwargs):
        params = api_stage_details_generic(
            request,
            "Request",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Endpoint",
                    "Status",
                    "Details",
                    "Request_Id",
                    "Session_Id",
                    "Channel_Id",
                    "Channel",
                    "External_reference",
                    "Timestamp",
                ],
                "fileName": "api_request_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="api_request_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API request in pdf format",
    )
    @action(methods=["POST"], detail=False, url_path="api_request_details_export_pdf")
    def api_request_details_export_pdf(self, request, *args, **kwargs):
        params = api_stage_details_generic(
            request,
            "Request",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Internal_reference",
                    "API",
                    "Endpoint",
                    "Status",
                    "Details",
                    "Request_Id",
                    "Session_Id",
                    "Channel_Id",
                    "Channel",
                    "External_reference",
                    "Timestamp",
                ],
                "fileName": "api_request_details.pdf",
                "title": "API Response Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
