from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from onboarding.models import SingleCifRetailData, SingleCifSpData
from main.utils.boiler_plate import get_generic_response
from onboarding.services.onboarding_transaction_report_utils import (
    successful_transaction_generic,
    failed_transaction_generic,
    exception_transaction_generic,
    successful_transaction_report_generic,
    rejected_transactions_report_generic,
    discarded_or_exceptions_transaction_rt_generic,
    onboarding_remediated_pass_generic
)


class TransactionReportViewSet(GenericViewSet):
    # these big numbers are irrespective of the onboarding channel
    @extend_schema(
        operation_id="successful_transaction_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="successful_transaction_rt")
    def successful_transaction_rt(self, request, *args, **kwargs):
        """
        The successful_transaction_rt function is a viewset that returns the number of successful transactions for a given tenant.
        It takes in the request, *args and **kwargs as parameters. It then creates a dictionary called params which contains all
        the necessary information to make this function work. The params dictionary has keys such as &quot;request&quot;, &quot;models&quot;,
        &quot;serializers&quot;, etc... Each key has its own value which is used by get_generic_response() to return the desired result.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of successful transactions
        """
        params = successful_transaction_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Successful transactions for Sole Proprietary",
    )
    @action(methods=["POST"], detail=False, url_path="successful_transaction_sp")
    def successful_transaction_sp(self, request, *args, **kwargs):
        """
        The successful_transaction_sp function is used to get the number of successful transactions for a specific service provider.
            It takes in a request object and returns the number of successful transactions for that service provider.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of successful transactions for a given tenant
        """
        params = successful_transaction_generic(request, SingleCifSpData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="failed_transaction_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Failed Transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="failed_transaction_rt")
    def failed_transaction_rt(self, request, *args, **kwargs):
        """
        The failed_transaction_rt function is used to get the number of failed transactions for a given tenant.
            It takes in a request object and returns the number of failed transactions as an integer.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A count of the number of failed transactions
        """
        params = failed_transaction_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="failed_transaction_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Failed Transactions for SP",
    )
    @action(methods=["POST"], detail=False, url_path="failed_transaction_sp")
    def failed_transaction_sp(self, request, *args, **kwargs):
        """
        The failed_transaction_sp function is a viewset that returns the number of failed transactions for a given tenant.
        It takes in an HTTP request and returns the number of failed transactions as JSON data.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of distinct external references in the qreject queue
        """
        params = failed_transaction_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # Transactions big number for  exceptions
    @extend_schema(
        operation_id="exception_transaction_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of all Exception transactions for retail",
    )
    @action(methods=["POST"], detail=False, url_path="exception_transaction_rt")
    def exception_transaction_rt(self, request, *args, **kwargs):
        """
        The exception_transaction_rt function is used to get the number of exceptions in a queue.
            It takes in a request and returns the number of exceptions for that tenant.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of distinct external references
        """
        params = exception_transaction_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Successful transactions details",
    )
    @action(methods=["POST"], detail=False, url_path="successful_transaction_report_rt")
    def successful_transaction_report_rt(self, request, *args, **kwargs):
        """
        The successful_transaction_report_rt function is used to generate a report of all successful transactions.
            The function takes in the request object and returns a table containing the following fields:
                Customer_name, Account_number_2, Created_at_branch, Customer type, Application number and Approved by.

        :param self: Represent the instance of the class
        :param request: Get the request object, which is used to get the query string parameters
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = successful_transaction_report_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Successful transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_transaction_report_rt_export_csv",
    )
    def successful_transaction_report_rt_export_csv(self, request, *args, **kwargs):
        """
        The successful_transaction_report_rt_export_csv function is used to export a CSV file containing the following fields:
            - Customer_name
            - Account_number_2
            - Created_at_branch
            - Customer type (Individual or Corporate)
            - Application number (external reference)
            - Approved by (submit by)

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file that contains the following fields:
        """
        params = successful_transaction_report_generic(
            request,
            SingleCifRetailData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "successful_transaction_report_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Successful transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_transaction_report_rt_export_pdf",
    )
    def successful_transaction_report_rt_export_pdf(self, request, *args, **kwargs):
        """
        The successful_transaction_report_rt_export_pdf function is used to export a PDF file of the successful_transaction_report_rt view.
        The function takes in a request object and returns an HttpResponse object containing the PDF file.
        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_transaction_report_generic(
            request,
            SingleCifRetailData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "successful_transaction_report_rt.pdf",
                "title": "Retail Successful Transaction Report",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Successful transactions details",
    )
    @action(methods=["POST"], detail=False, url_path="successful_transaction_report_sp")
    def successful_transaction_report_sp(self, request, *args, **kwargs):
        """
        The successful_transaction_report_sp function is used to generate a report of all successful transactions.
            It takes in the request object and returns a table containing the following fields:
                Customer_name, Account_number_2, Created_at_branch, Customer type, Application number, Approved by and Approved timestamp.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of data
        """
        params = successful_transaction_report_generic(request, SingleCifSpData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_sp_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Successful transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_transaction_report_sp_export_csv",
    )
    def successful_transaction_report_sp_export_csv(self, request, *args, **kwargs):
        """
        The successful_transaction_report_sp_export_csv function is used to export a CSV file containing the following fields:
            Customer_name, Account_number_2, Created_at_branch, Customer type, Application number and Approved by.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following fields:
        """
        params = successful_transaction_report_generic(
            request,
            SingleCifSpData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "successful_transaction_report_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="successful_transaction_report_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Successful transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="successful_transaction_report_sp_export_pdf",
    )
    def successful_transaction_report_sp_export_pdf(self, request, *args, **kwargs):
        """
        The successful_transaction_report_sp_export_pdf function is used to export a PDF file of the successful transaction report for sole proprietors.
        The function takes in a request object and returns an HttpResponse object containing the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file of the successful transactions report for sole proprietors

        """
        params = successful_transaction_report_generic(
            request,
            SingleCifSpData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "successful_transaction_report_sp.pdf",
                "title": "Sole Proprietor Successful Transaction Report",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Rejected applications retail
    @extend_schema(
        operation_id="rejected_transactions_report_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Reject transactions details for retail",
    )
    @action(methods=["POST"], detail=False, url_path="rejected_transactions_report_rt")
    def rejected_transactions_report_rt(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_rt function returns a list of rejected transactions.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = rejected_transactions_report_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="rejected_transactions_report_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all rejected transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="rejected_transactions_report_rt_export",
    )
    def rejected_transactions_report_rt_export(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_rt_export function is used to export the rejected transactions report for retail customers.
        It takes in a request object and returns an exported csv file containing the following fields:
        Customer_name, Created_at_branch, Customer_type, Application number, Rejected by and Rejected timestamp.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = rejected_transactions_report_generic(
            request,
            SingleCifRetailData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "rejected_transaction_report_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="rejected_transactions_report_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all rejected transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="rejected_transactions_report_rt_export_pdf",
    )
    def rejected_transactions_report_rt_export_pdf(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_rt_export_pdf function is used to export a PDF report of rejected transactions for the Retail channel.
        The function takes in a request object and returns an HTTP response containing the PDF file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = rejected_transactions_report_generic(
            request,
            SingleCifRetailData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "rejected_transaction_report_rt.pdf",
                "title": "Retail Rejected Transaction Report",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # REJECTED for sp reports
    @extend_schema(
        operation_id="rejected_transactions_report_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Reject transactions details for sp",
    )
    @action(methods=["POST"], detail=False, url_path="rejected_transactions_report_sp")
    def rejected_transactions_report_sp(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_sp function returns a list of rejected transactions for the current tenant.
        The function takes in a request object and returns an items object containing the data to be displayed on the page.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The following:
        """
        params = rejected_transactions_report_generic(request, SingleCifSpData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="rejected_transactions_report_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all rejected transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="rejected_transactions_report_sp_export",
    )
    def rejected_transactions_report_sp_export(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_sp_export function is used to export the rejected transactions report for SP.
        It takes in a request and returns an exported CSV file containing the following fields:
        Customer_name, Created_at_branch, Customer_type, Application number, Rejected by, Rejected timestamp and Mode.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = rejected_transactions_report_generic(
            request,
            SingleCifSpData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "rejected_transaction_report_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="rejected_transactions_report_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all rejected transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="rejected_transactions_report_sp_export_pdf",
    )
    def rejected_transactions_report_sp_export_pdf(self, request, *args, **kwargs):
        """
        The rejected_transactions_report_sp_export_pdf function is used to generate a PDF report of rejected transactions for sole proprietors.
        The function takes in the request object, and returns a PDF file containing the requested data.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the url
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = rejected_transactions_report_generic(
            request,
            SingleCifSpData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "rejected_transaction_report_sp.pdf",
                "title": "Sole Proprietor Rejected Transaction Report",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # DISCARDED transactions retail
    @extend_schema(
        operation_id="discarded_transaction_report_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Failed transactions details for retail",
    )
    @action(methods=["POST"], detail=False, url_path="discarded_transaction_report_rt")
    def discarded_transaction_report_rt(self, request, *args, **kwargs):
        """
        The discarded_transaction_report_rt function is used to generate a report of all transactions that have been discarded.
        The function takes in the request object and returns a table containing the following fields:
        Customer_name, Created_at_branch, Customer_type, Application number, Abandoned by and Abandoned timestamp.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = discarded_or_exceptions_transaction_rt_generic(request, "QDISCARD")
        return get_generic_response(params)

    @extend_schema(
        operation_id="discarded_transaction_report_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all rejected transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="discarded_transaction_report_rt_export_csv",
    )
    def discarded_transaction_report_rt_export_csv(self, request, *args, **kwargs):
        """
        The discarded_transaction_report_rt_export_csv function is used to export the discarded transaction report in CSV format.
        It takes a request object as an argument and returns a response object containing the exported data.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = discarded_or_exceptions_transaction_rt_generic(
            request,
            "QDISCARD",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "abandoned_transaction_report_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="discarded_transaction_report_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Failed transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="discarded_transaction_report_rt_export_pdf",
    )
    def discarded_transaction_report_rt_export_pdf(self, request, *args, **kwargs):
        """
        The discarded_transaction_report_rt_export_pdf function is used to export a PDF report of all the discarded transactions in the Retail queue.
        The function takes in a request object and returns an exported PDF file containing information about all the discarded transactions.

        :param self: Represent the instance of the object
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = discarded_or_exceptions_transaction_rt_generic(
            request,
            "QDISCARD",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "abandoned_transaction_report_rt.pdf",
                "title": "Retail Abandoned Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # exception applications for retail - when face match fails
    @extend_schema(
        operation_id="exception_transaction_report_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display all Failed transactions details for retail",
    )
    @action(methods=["POST"], detail=False, url_path="exception_transaction_report_rt")
    def exception_transaction_report_rt(self, request, *args, **kwargs):
        """
        The exception_transaction_report_rt function is used to generate a report of all the transactions that are in the exception queue.
        The function takes in a request object and returns an items object which contains data about each transaction that is currently in the exception queue.


        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = discarded_or_exceptions_transaction_rt_generic(request, "QEXCEPTION")
        return get_generic_response(params)

    @extend_schema(
        operation_id="exception_transaction_report_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Failed transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="exception_transaction_report_rt_export_csv",
    )
    def exception_transaction_report_rt_export_csv(self, request, *args, **kwargs):
        """
        The exception_transaction_report_rt_export_csv function is used to export the Exception Transaction Report for Retail Customers in CSV format.

        :param self: Represent the instance of the object itself
        :param request: Get the query string from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = discarded_or_exceptions_transaction_rt_generic(
            request,
            "QEXCEPTION",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                ],
                "fileName": "exception_transaction_report_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="exception_transaction_report_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download all Failed transactions details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="exception_transaction_report_rt_export_pdf",
    )
    def exception_transaction_report_rt_export_pdf(self, request, *args, **kwargs):
        """
        The exception_transaction_report_rt_export_pdf function is used to export a PDF file of the Retail Exception Transaction Report.
        The function takes in a request object and returns an HTTP response with the PDF file attached.


        :param self: Represent the instance of the object
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = discarded_or_exceptions_transaction_rt_generic(
            request,
            "QEXCEPTION",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Branch_code",
                    "Customer_type",
                    "Mode",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                ],
                "fileName": "exception_transaction_report_rt.pdf",
                "title": "Retail Exception Transaction Report",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_remediated_pass",
        tags=[AuthTags.AUTHORIZE],
        description="Shows  second-day report of failed, remediated pass, and passed applications",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_remediated_pass")
    def onboarding_remediated_pass(self, request):
        params = onboarding_remediated_pass_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_remediated_pass_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Shows  second-day report of failed, remediated pass, and passed applications",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_remediated_pass_export_csv"
    )
    def onboarding_remediated_pass_export_csv(self, request):
        params = onboarding_remediated_pass_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_Reference_Number",
                    "Application_Status",
                    "Primary_Contact_Number",
                    "Primary_Email_Address",
                    "Account_Number_1",
                    "Account_Number_2",
                    "Last_action_perform_timestamp"
                ],
                "fileName": "Remediation_Report.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_remediated_pass_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Shows  second-day report of failed, remediated pass, and passed applications",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_remediated_pass_export_pdf"
    )
    def onboarding_remediated_pass_export_pdf(self, request):
        params = onboarding_remediated_pass_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_Reference_Number",
                    "Application_Status",
                    "Primary_Contact_Number",
                    "Primary_Email_Address",
                    "Account_Number_1",
                    "Account_Number_2",
                    "Last_action_perform_timestamp"
                ],
                "fileName": "Remediation_Report.pdf",
                "title": "Second Day Failed, Remediated, Failed Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
