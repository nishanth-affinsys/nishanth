from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from console.services.transaction_reports_utils import (
    successful_transaction_generic,
    successful_transaction_goal_completed_generic,
    successful_transaction_goal_not_completed_generic,
    failed_transaction_generic,
    system_aborted_generic,
    user_aborted_generic,
    transactions_linechart_generic,
    transaction_partition_generic,
    all_transaction_breakdown_generic,
    transaction_report_details_generic,
)

from main.utils.boiler_plate import get_generic_response


# constants
goal_completed = "Goal Completed"
goal_not_completed = "Goal Not Completed"
user_aborted = "User Aborted"
system_aborted = "System Aborted"


class TransactionChartsViewSet(GenericViewSet):  # for Transaction Report
    # Total Successful Transactions
    @extend_schema(
        operation_id="transaction_successful",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_successful")
    def successful_transaction(self, request, *args, **kwargs):
        """
        The Successful_transaction function is used to get the count of successful transactions.
            Args:
                request (object): The request object contains all the information about the HTTP Request.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The total number of transactions
        """
        add = successful_transaction_generic(request)
        return Response(data={"count": add})

    @extend_schema(
        operation_id="transaction_successful_goal_completed",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions Goal Completed",
    )
    @action(
        methods=["POST"], detail=False, url_path="transaction_successful_goal_completed"
    )
    def successful_transaction_goal_completed(self, request, *args, **kwargs):
        """
        The Successful_transaction_goal_completed function returns the number of successful transactions that have completed their goal.
            ---
            # YAML (must be separated by `---`)

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of transactions that completed the goal successfully
        """
        params = successful_transaction_goal_completed_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="transaction_successful_goal_not_completed",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Successful Transactions Goal Not Completed",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_successful_goal_not_completed",
    )
    def successful_transaction_goal_not_completed(self, request, *args, **kwargs):
        """
        The Successful_transaction_goal_not_completed function returns the number of successful transactions where the goal was not completed.
            ---
            parameters:
                - name: request_id
                  description: The ID of a specific transaction to retrieve. If no ID is provided, all transactions will be returned.  This parameter is optional and can be omitted if you want to return all transactions in the database.  To specify multiple IDs, separate them with commas (e.g., 1,2).  Note that this parameter cannot be used in conjunction with any other parameters; it must stand alone or not at all.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of transactions with a final response of goal not completed
        """
        params = successful_transaction_goal_not_completed_generic(request)
        return get_generic_response(params)

    # Total Failed Transactions
    @extend_schema(
        operation_id="transaction_failed",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Failed Transactions",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_failed")
    def failed_transaction(self, request, *args, **kwargs):
        """
        The Failed_transaction function is used to get the count of failed transactions.
            It takes in a request and returns a response with the count of failed transactions.

        :param self: Represent the instance of the object itself
        :param request: Get the request object, which contains all the information about the current request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The count of failed transactions
        """
        add = failed_transaction_generic(request)
        return Response(data={"count": add})

    @extend_schema(
        operation_id="transaction_system_aborted",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Failed Transactions System Aborted",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_system_aborted")
    def system_aborted(self, request, *args, **kwargs):
        """
        The System_aborted function returns the number of times a transaction was aborted by the system.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of transactions that were aborted by the system
        """
        params = system_aborted_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="transaction_user_aborted",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Total Failed Transactions User Aborted",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_user_aborted")
    def user_aborted(self, request, *args, **kwargs):
        """
        The User_aborted function returns the number of transactions that were aborted by the user.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of transactions that have been aborted by the user

        """
        params = user_aborted_generic(request)
        return get_generic_response(params)

    # Total API Calls (FAQs)
    # @extend_schema(
    #     operation_id="total_API_calls_FAQ",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total API Calls (FAQs)",
    # )
    # @action(methods=["POST"], detail=False, url_path="api-faq")
    # def total_api_calls_faq(self, request, *args, **kwargs):
    #     """
    #     The total_API_calls_FAQ function is a custom API endpoint that returns the total number of FAQs in the database.
    #     It uses a generic function called get_generic_response to accomplish this task. The get_generic_response function takes
    #     a dictionary as an argument, and it uses those parameters to query the database for information about all of the FAQs.
    #
    #     :param self: Represent the instance of the class
    #     :param request: Get the request object
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The total number of api calls for a given tenant
    #     """
    #     params = total_api_calls_faq_generic(request)
    #     return get_generic_response(params)
    #
    # # Total API Calls (Trans)
    # @extend_schema(
    #     operation_id="total_API_calls_Trans",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Used for displaying Total API Calls (Trans)",
    # )
    # @action(methods=["POST"], detail=False, url_path="api-trans")
    # def total_api_calls_trans(self, request, *args, **kwargs):
    #     """
    #     The total_API_calls_Trans function is a generic function that returns the total number of API calls made by all transactions in the database.
    #     It takes no arguments, and returns an integer value.
    #
    #     :param self: Represent the instance of the object itself
    #     :param request: Pass the request object to the get_generic_response function
    #     :param *args: Send a non-keyworded variable length argument list to the function
    #     :param **kwargs: Pass keyworded, variable-length argument list
    #     :return: The total number of api calls made
    #     """
    #     params = total_api_calls_trans_generic(request)
    #     return get_generic_response(params)

    # Detailed report for successful transactions
    @extend_schema(
        operation_id="transaction_successful_transaction_rpt",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Detailed report for Successful Transactions",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_successful_transaction_rpt",
    )
    def successful_transaction_rpt(self, request, *args, **kwargs):
        """
        The Successful_transaction_rpt function is used to get the successful transactions report.
            Args:
                request (object): The request object contains details of the incoming HTTP request.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of all transactions that have completed the final stage
        """
        params = transaction_report_details_generic(
            request, goal_completed, goal_not_completed
        )
        return get_generic_response(params)

    # Successful Transactions chart export csv format
    @extend_schema(
        operation_id="transaction_successful_transaction_rpt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Detailed report for Successful Transactions in csv formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_successful_transaction_rpt_export_csv",
    )
    def successful_transaction_export(self, request, *args, **kwargs):
        """
        The Successful_transaction_export function is used to export a CSV file containing all the successful transactions.
        The function takes in a request object and returns an iterator that can be used to generate the CSV file.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The successful transactions in a csv file
        """
        params = transaction_report_details_generic(
            request,
            goal_completed,
            goal_not_completed,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Customer_id",
                    "Transaction_id",
                    "Transaction_intent",
                    "Stage",
                    "Stage_result",
                    "Channel",
                    "Details",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "successful_transactions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="transaction_successful_transaction_rpt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Detailed report for Successful Transactions in pdf formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_successful_transaction_rpt_export_pdf",
    )
    def successful_transaction_export_pdf(self, request, *args, **kwargs):
        """
        The Successful_transaction_export_pdf function is used to export a pdf file of all the successful transactions.
            The function takes in a request and returns an exported pdf file.

        :param self: Represent the instance of the class
        :param request: Get the request object, which contains all the information about the current http request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the details of all successful transactions
        """
        params = transaction_report_details_generic(
            request,
            goal_completed,
            goal_not_completed,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Customer_id",
                    "Transaction_id",
                    "Transaction_intent",
                    "Stage",
                    "Stage_result",
                    "Channel",
                    "Details",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "successful_transactions.pdf",
                "title": "Successful Transactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Detailed report for failed transactions
    @extend_schema(
        operation_id="transaction_report_failed_rpt",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Detailed report for failed transactions",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_report_failed_rpt")
    def failed_transaction_rpt(self, request, *args, **kwargs):
        """
        The Failed_transaction_rpt function is used to get the failed transactions report.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of failed transactions
        """
        params = transaction_report_details_generic(
            request, user_aborted, system_aborted
        )
        return get_generic_response(params)

    # Failed Transactions chart export csv format
    @extend_schema(
        operation_id="transaction_report_failed_rpt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Detailed report for Failed Transactions in csv formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_report_failed_rpt_export_csv",
    )
    def failed_transaction_export(self, request, *args, **kwargs):
        """
        The Failed_transaction_export function is used to export a CSV file containing all failed transactions.
        The function takes in the request and returns a response object with the following fields:
            - Customer_id: The customer ID of the user who initiated this transaction.
            - Transaction_id: The unique ID of this transaction.
            - Transaction_intent: The intent that was being executed when this transaction failed
            - Stage: The stage at which this transaction failed (e.g., &quot;Final Response&quot;).
            - Stage_result: A description of why/how it failed, e.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        :doc-author: Trelent
        """
        params = transaction_report_details_generic(
            request,
            user_aborted,
            system_aborted,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Customer_id",
                    "Transaction_id",
                    "Transaction_intent",
                    "Stage",
                    "Stage_result",
                    "Channel",
                    "Details",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "failed_transactions.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="transaction_report_failed_rpt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading Detailed report for Failed Transactions in pdf formate",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="transaction_report_failed_rpt_export_pdf",
    )
    def failed_transaction_export_pdf(self, request, *args, **kwargs):
        """
        The Failed_transaction_export_pdf function is used to export a pdf file of all the failed transactions.
        It takes in a request and returns an exported pdf file.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the failed transactions
        """
        params = transaction_report_details_generic(
            request,
            user_aborted,
            system_aborted,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Customer_id",
                    "Transaction_id",
                    "Transaction_intent",
                    "Stage",
                    "Stage_result",
                    "Remarks",
                    "Channel",
                    "Details",
                    "Remarks",
                    "Timestamp",
                ],
                "fileName": "failed_transactions.pdf",
                "title": "Failed Transactions",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="transactions_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="User for displaying Linechart of transactions",
    )
    @action(methods=["POST"], detail=False, url_path="transactions_linechart")
    def transactions_linechart(self, request, *args, **kwargs):
        """
        The transactions_linechart function is a viewset that returns the number of successful and failed transactions
        for each day in the past week. The data returned by this function is used to populate a line chart on the dashboard.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A response object
        """
        items = transactions_linechart_generic(request)
        return Response(items)

    # Sunburst chart used to show successful and failure transaction breakdown

    @extend_schema(
        operation_id="transaction_successful_partition",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying breakdown graph on Successful Transaction",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_successful_partition")
    def successful_transaction_partition(self, request, *args, **kwargs):
        items = transaction_partition_generic(
            request, "Goal Completed", "Goal Not Completed"
        )
        return Response(items)

    @extend_schema(
        operation_id="transaction_failed_partition",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying partition graph on Failed Transaction",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_failed_partition")
    def failed_transaction_partition(self, request, *args, **kwargs):
        items = transaction_partition_generic(request, "User Aborted", "System Aborted")
        return Response(items)

    @extend_schema(
        operation_id="transaction_breakdown_sunburst",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the complete breakdown of all transaction",
    )
    @action(methods=["POST"], detail=False, url_path="transaction_breakdown_sunburst")
    def all_transaction_breakdown_sunburst(self, request, *args, **kwargs):
        items = all_transaction_breakdown_generic(request)
        return Response(items)
