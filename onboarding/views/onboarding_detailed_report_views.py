from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from onboarding.models import DetailedReportTableRt, DetailedReportTableSp
from onboarding.services.onboarding_detailed_report_utils import (
    onb_detailed_applications_report_generic,
    detailed_report_comments_generic
)

from main.utils.boiler_plate import (
    get_generic_response,
)


class DetailedReportViewSet(GenericViewSet):
    field_names_rt = [
        "Application_number",
        "Product_name",
        "Customer_name",
        "Phone_Number",
        "Created_by",
        "Created_timestamp",
        "Last_modified_by",
        "Last_modified_timestamp",
        "Verified_by",
        "Verified_timestamp",
        "Approved_by",
        "Approved_timestamp",
        "Account_number_1",
        "Account_number_2",
        "Created_at_branch_code",
        "Present_at_branch_code",
        "Application_stage",
        "Customer_type",
    ]

    field_names_sp = [
        "Application_number",
        "Product_name",
        "Business_name",
        "Phone_Number",
        "Created_by",
        "Created_timestamp",
        "Last_modified_by",
        "Last_modified_timestamp",
        "Verified_by",
        "Verified_timestamp",
        "Approved_by",
        "Approved_timestamp",
        "Account_number_1",
        "Account_number_2",
        "Created_at_branch_code",
        "Present_at_branch_code",
        "Application_stage",
        "Customer_type",
    ]

    @extend_schema(
        operation_id="applications_report_agent_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(Agent)",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_agent_rt")
    def applications_report_agent_rt(self, request, *args, **kwargs):
        """
        The applications_report_agent_rt function returns a table of all applications created by agents.
        The function takes in the request object and passes it to the query function, which returns a queryset.
        The queryset is then filtered for only those applications that were created by an agent, and values are selected from it.
        These values are passed to the return_table function, which converts them into a table format that can be displayed on the frontend.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableRt, "Agent", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_agent_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_agent_rt_export_csv",
    )
    def applications_report_agent_rt_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_agent_rt_export_csv function is used to export the data from the applications_report_agent_rt view into a csv file.
        The function takes in a request object and returns an items object which contains all of the data that was exported.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Agent",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_agent_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_agent_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_agent_rt_export_pdf",
    )
    def applications_report_agent_rt_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_agent_rt_export_pdf function is used to export the Agent Applications Report as a PDF file.
        The function takes in a request object and returns an items object containing the report data.


        :param self: Represent the instance of the class
        :param request: Get the data from the client side
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Agent",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_agent_rt.pdf",
                "title": "Retail Detailed Report (Agent)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_agent_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(Agent) for SP",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_agent_sp")
    def applications_report_agent_sp(self, request, *args, **kwargs):
        """
        The applications_report_agent_sp function returns a list of all applications created by agents.
        The function takes in the request object and returns a list of dictionaries containing the following keys:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last_modified_timestamp
        Approved by Approved timestamp Account number 1 Account number 2 Created at branch code Present at branch code
        Application stage Created at branch type Customer type Product name

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableSp, "Agent", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_agent_sp_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_agent_sp_export_csv",
    )
    def applications_report_agent_sp_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_agent_sp_export_csv function is used to export the data from the applications_report_agent_sp view into a csv file.
        The function takes in a request object and returns an items object which contains all of the data that was exported.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Agent",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_agent_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_agent_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_agent_sp_export_pdf",
    )
    def applications_report_agent_sp_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_agent_sp_export_pdf function is used to export the data of all applications created by agents for sole proprietors in a PDF file.
        The function takes in the request and returns a PDF file containing the data of all applications created by agents for sole proprietors.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Agent",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_agent_sp.pdf",
                "title": "Sole Proprietor Detailed Report (Agent)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # DETAILS OF REPORTS STARTED BY SELF

    @extend_schema(
        operation_id="applications_report_self_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(Self)",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_self_rt")
    def applications_report_self_rt(self, request, *args, **kwargs):
        """
        The applications_report_self_rt function returns a table of all applications created by the Self channel.
        The function takes in a request object and returns an array of objects containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last_modified timestamp
        Approved by Approved timestamp Account number 1 Account number 2 Created at branch code Present at branch code
        Application stage Created at branch type Customer type Product name

        :param self: Refer to the current object
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableRt, "Self", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_self_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_self_rt_export_csv",
    )
    def applications_report_self_rt_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_self_rt_export_csv function is used to export the data from the applications_report_self_rt view into a csv file.
        The function takes in request, *args and **kwargs as parameters.
        It returns items which is a list of dictionaries containing all the data that was exported.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Self",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_self_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_self_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Self)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_self_rt_export_pdf",
    )
    def applications_report_self_rt_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_self_rt_export_pdf function is used to export the data of all self retail applications in a PDF file.
        The function takes in request as an argument and returns the PDF file containing the data.

        :param self: Refer to the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Self",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_self_rt.pdf",
                "title": "Retail Detailed Report (Self)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_retail_comments_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(Self)",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_retail_comments_details")
    def onboarding_retail_comments_details(self, request, *args, **kwargs):
        """
        The applications_report_self_rt function returns a table of all applications created by the Self channel.
        The function takes in a request object and returns an array of objects containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last_modified timestamp
        Approved by Approved timestamp Account number 1 Account number 2 Created at branch code Present at branch code
        Application stage Created at branch type Customer type Product name

        :param self: Refer to the current object
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        # params = onb_detailed_applications_report_generic(
        #     request, DetailedReportTableRt, "Self", 2
        # )
        params = detailed_report_comments_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_retail_comments_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="onboarding_retail_comments_details_export_csv",
    )
    def onboarding_retail_comments_details_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_self_rt_export_csv function is used to export the data from the applications_report_self_rt view into a csv file.
        The function takes in request, *args and **kwargs as parameters.
        It returns items which is a list of dictionaries containing all the data that was exported.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = detailed_report_comments_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Product_name",
                    "Phone_Number",
                    "Created_by",
                    "Created_timestamp",
                    "Last_modified_by",
                    "Last_modified_timestamp",
                    "Last_action_performed_by",
                    "Last_action_perform_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                    "Account_number_1",
                    "Account_number_2",
                    "Created_at_branch_code",
                    "Present_at_branch_code",
                    "Application_stage",
                    "Customer_type",
                    "Action",
                    "Comments",
                ],
                "fileName": "detailed_report_self_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="onboarding_retail_comments_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Self)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="onboarding_retail_comments_details_export_pdf",
    )
    def onboarding_retail_comments_details_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_self_rt_export_pdf function is used to export the data of all self retail applications in a PDF file.
        The function takes in request as an argument and returns the PDF file containing the data.

        :param self: Refer to the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = detailed_report_comments_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames":
                    [
                        "Application_number",
                        "Product_name",
                        "Phone_Number",
                        "Created_by",
                        "Created_timestamp",
                        "Last_modified_by",
                        "Last_modified_timestamp",
                        "Last_action_performed_by",
                        "Last_action_performed_timestamp",
                        "Approved_by",
                        "Approved_timestamp",
                        "Account_number_1",
                        "Account_number_2",
                        "Created_at_branch_code",
                        "Present_at_branch_code",
                        "Application_stage",
                        "Customer_type",
                        "Action",
                        "Comments"
                    ],
                "fileName": "detailed_report_self_rt.pdf",
                "title": "Retail Detailed Report (Self)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_self_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(Self)",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_self_sp")
    def applications_report_self_sp(self, request, *args, **kwargs):
        """
        The applications_report_self_sp function returns a list of all applications submitted through the self-service portal.
        The function takes in a request object and returns an array of objects containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last_modified_timestamp,
        Approved by (if applicable), Approved timestamp (if applicable), Account number 1 (if applicable), Account number 2 (if applicable),
        Created at branch code , Present at branch code , Application stage ,Created at branch type  and Customer type .
        The function also filters out any data that is not relevant to the

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of all the applications submitted through self onboarding
        """

        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableSp, "Self", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_self_sp_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Agent)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_self_sp_export_csv",
    )
    def applications_report_self_sp_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_self_sp_export_csv function is used to export the applications report for self SP.
            It takes in a request and returns an item.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Self",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_self_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_self_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Self)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_self_sp_export_pdf",
    )
    def applications_report_self_sp_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_self_sp_export_pdf function is used to export a PDF report of all the applications that have been created by self onboarding channel for sole proprietor customers.
        The function takes in request as an argument and returns a PDF file containing the data from the query set.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A tuple of two items
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Self",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_self_sp.pdf",
                "title": "Sole Proprietor Detailed Report (Self)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Details of report by staff

    @extend_schema(
        operation_id="applications_report_staff_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(STAFF)",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_staff_rt")
    def applications_report_staff_rt(self, request, *args, **kwargs):
        """
        The applications_report_staff_rt function is used to generate a report of all applications created by staff.
        The function takes in the request and returns a table containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last modified timestamp
        Approved by Approved timestamp Account number 1 Account number 2 Created at branch code Present at branch code
        Application stage Created at branch type Customer type Product name

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableRt, "Staff", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_staff_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(STAFF)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_staff_rt_export_csv",
    )
    def applications_report_staff_rt_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_staff_rt_export_csv function is used to export the applications report for staff RT in CSV format.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Staff",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_staff_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_staff_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(STAFF)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_staff_rt_export_pdf",
    )
    def applications_report_staff_rt_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_staff_rt_export_pdf function is used to export the Retail Staff Applications report in PDF format.
        It takes a request object as an argument and returns a response object containing the PDF file.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableRt,
            "Staff",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_rt,
                "fileName": "detailed_report_staff_rt.pdf",
                "title": "Retail Detailed Report (Staff)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_staff_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display details of onboarding(STAFF)",
    )
    @action(methods=["POST"], detail=False, url_path="applications_report_staff_sp")
    def applications_report_staff_sp(self, request, *args, **kwargs):
        """
        The applications_report_staff_sp function is used to generate a report of all applications created by staff.
        The function takes in the request and returns a table containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Last_modified_by, Last modified timestamp
        Approved by Approved timestamp Account number 1 Account number 2 Created at branch code Present at branch code
        Application stage Created at branch type Customer type Product name

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the url
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following data:
        """
        params = onb_detailed_applications_report_generic(
            request, DetailedReportTableSp, "Staff", 2
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_staff_sp_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Staff)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_staff_sp_export_csv",
    )
    def applications_report_staff_sp_export_csv(self, request, *args, **kwargs):
        """
        The applications_report_staff_sp_export_csv function is used to export the applications report for staff SP.
            It takes in a request and returns an items object.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Staff",
            2,
            key="csv_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_staff_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_report_staff_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download details of onboarding(Staff)",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="applications_report_staff_sp_export_pdf",
    )
    def applications_report_staff_sp_export_pdf(self, request, *args, **kwargs):
        """
        The applications_report_staff_sp_export_pdf function is used to export the applications report for staff SP in PDF format.
        It takes a request as an argument and returns the response of the query set in PDF format.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the data from the query
        """
        params = onb_detailed_applications_report_generic(
            request,
            DetailedReportTableSp,
            "Staff",
            2,
            key="pdf_kwargs",
            value={
                "fieldNames": self.field_names_sp,
                "fileName": "detailed_report_staff_sp.pdf",
                "title": "Sole Proprietor Detailed Report (Staff)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
