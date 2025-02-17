from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from onboarding.models import SingleCifRetailData, SingleCifSpData
from main.utils.boiler_plate import query, get_generic_response, return_table
from onboarding.services.onboarding_stage_report_utils import (
    started_flow_generic,
    cif_created_generic,
    cif_failed_generic,
    self_discarded_generic,
    started_flow_self_rt_generic,
    started_flow_self_sp_generic,
    staff_started_flow_rt_generic,
    staff_started_flow_sp_generic,
    applications_with_maker_bigno_generic,
    applications_with_verifier_bigno_generic,
    applications_with_approvers_bigno_generic,
    applications_processed_bigno_generic,
    applications_exceptions_bigno_generic,
    overall_application_stages_sp_stacked_generic,
    applications_rejected_bigno_generic,
    overall_application_stages_rt_stacked_generic,
    queuecodes_pie_rt_generic,
    self_queuecodes_pie_rt_generic,
    queuecodes_pie_sp_generic,
    self_queuecodes_pie_sp_generic,
    successful_cif_details_generic,
    failed_cif_details_generic,
    self_discarded_details_generic,
    kyc_account_opening_details_generic
)


class StageReportViewSet(GenericViewSet):
    # Same reports from old dashboard(superset)
    # Agent stage report for retail
    @extend_schema(
        operation_id="agent_started_flow_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_started_flow_retail")
    def agent_started_flow_retail(self, request, *args, **kwargs):
        """
        The agent_started_flow_retail function is used to get the number of retail customers that have started the onboarding process.
        The function takes in a request object and returns a response object containing the count of retail customers that have started
        the onboarding process.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of records
        """
        params = started_flow_generic(request, SingleCifRetailData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_cif_created_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_cif_created_retail")
    def agent_cif_created_retail(self, request, *args, **kwargs):
        """
        The agent_cif_created_retail function is used to get the number of CIFs created by agents in retail.
            It takes in a request object and returns a response object containing the count of CIFs created by agents in retail.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of cifs created by the agent
        """
        params = cif_created_generic(request, SingleCifRetailData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_cif_failed_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_cif_failed_retail")
    def agent_cif_failed_retail(self, request, *args, **kwargs):
        """
        The agent_cif_failed_retail function is used to get the number of failed retail CIFs for a given agent.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of failed retail cifs
        """
        params = cif_failed_generic(request, SingleCifRetailData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_successful_cif_details_rt")
    def agent_successful_cif_details_rt(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_rt function is used to return a table of all the successful CIFs created by agents.
        The function takes in a request object and returns an items object which contains the data for the table.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of cifs that are successfully onboarded by agents
        """
        params = successful_cif_details_generic(request, SingleCifRetailData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_successful_cif_details_rt_export",
    )
    def agent_successful_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_rt_export function is used to export the data of all successful CIFs created by agents in the Retail channel.
        The function takes a request object as an argument and returns a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp, Account number 1 and 2 (if applicable), Customer type.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Agent",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "agent_successful_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_successful_cif_details_rt_export_pdf",
    )
    def agent_successful_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_rt_export_pdf function is used to export the agent_successful_cif_details_rt data as a PDF file.
        The function takes in the request, *args and **kwargs parameters.
        It then creates a tzinfo variable that stores the timezone information for settings.TIMEZONE (which is set to UTC).
        A qs variable is created which queries all of the SingleCifRetailData objects with tenant equal to get_current_tenant() and onboarding channel equal to &quot;Agent&quot; and queue code equal to &quot;QSUCCESS&quot;. The values are filtered by Customer name, Application number, Created

        :param self: Represent the instance of the object itself
        :param request: Get the data from the url
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Agent",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "agent_successful_cif_details_rt.pdf",
                "title": "Retail Successful Agent Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_failed_cif_details_rt")
    def agent_failed_cif_details_rt(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_rt function returns a table of all the failed CIFs for Retail customers.
        The function takes in a request object and uses it to query the SingleCifRetailData model, which is then serialized using OnboardingSerializer.
        The queryset is filtered by tenant name, onboarding channel (Agent), queue code (QREJECT), and values are selected from the following fields: Customer_name, Application_number, Created_by, Created_timestamp, Rejected_by ,Rejected_timestamp ,Customer type. The items are returned as a table.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following fields:
        """
        params = failed_cif_details_generic(request, SingleCifRetailData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_failed_cif_details_rt_export"
    )
    def agent_failed_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_rt_export function is used to export the data of all the failed CIFs in Retail.
        The function takes a request as an argument and returns a CSV file containing details of all failed CIFs in Retail.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following data:
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Agent",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "agent_failed_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_failed_cif_details_rt_export_pdf",
    )
    def agent_failed_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_rt_export_pdf function is used to export the agent_failed_cif_details_rt data as a PDF file.
        The function takes in the request, *args and **kwargs parameters. The request parameter is used to get all of the
        agent failed cif details rt data from the database using query(request, SingleCifRetailData, OnboardingSerializer,&quot;onboarding&quot;).
        The qs variable stores this queryset. The qs variable then filters out all of the tenant names that are not equal to
        the current tenant name (get_current_tenant()). It also filters

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Agent",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "agent_failed_cif_details_rt.pdf",
                "title": "Retail Failed Agent Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # AGENT stage reports  for SOLE PROPRIETARY
    @extend_schema(
        operation_id="agent_started_flow_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_started_flow_sp")
    def agent_started_flow_sp(self, request, *args, **kwargs):
        """
        The agent_started_flow_sp function is used to get the number of flows started by agents for a specific tenant.
        The function takes in a request object and returns the number of flows started by agents for that tenant.

        :param self: Represent the instance of a class
        :param request: Get the user id from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = started_flow_generic(request, SingleCifSpData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_cif_created_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by agent in SP",
    )
    @action(methods=["POST"], detail=False, url_path="agent_cif_created_sp")
    def agent_cif_created_sp(self, request, *args, **kwargs):
        """
        The agent_cif_created_sp function is used to get the number of CIFs created by agents.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of unique cifs created by the agent in a given period
        """
        params = cif_created_generic(request, SingleCifSpData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_cif_failed_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_cif_failed_sp")
    def agent_cif_failed_sp(self, request, *args, **kwargs):
        """
        The agent_cif_failed_sp function is used to get the number of failed CIFs for a specific agent.
        The function takes in a request and returns the number of failed CIFs for that agent.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of failed cifs for the agent
        """
        params = cif_failed_generic(request, SingleCifSpData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_successful_cif_details_sp")
    def agent_successful_cif_details_sp(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_sp function returns a list of all the successful CIFs created by agents.
        The function takes in a request object and returns an array of objects containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following data:
        """
        params = successful_cif_details_generic(request, SingleCifSpData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_successful_cif_details_sp_export",
    )
    def agent_successful_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_sp_export function is used to export a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp. Account number 1 and 2 and Customer type.
        The function filters for the tenant name of the current user (get current tenant name), onboarding channel of Agent and queue code QSUCCESS.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of the following fields:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Agent",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "agent_successful_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_successful_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_successful_cif_details_sp_export_pdf",
    )
    def agent_successful_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The agent_successful_cif_details_sp_export_pdf function is used to export the agent_successful_cif_details_sp data in a pdf format.
            Args:
                request (HttpRequest): The HttpRequest object that contains the query parameters for filtering and sorting.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Agent",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "agent_successful_cif_details_sp.pdf",
                "title": "Sole Proprietor Agent Successful Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="agent_failed_cif_details_sp")
    def agent_failed_cif_details_sp(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_sp function returns a table of all the failed CIFs for agents.
            The function takes in a request object and uses it to query the SingleCifSpData model, which is then serialized using OnboardingSerializer.
            The queryset is filtered by tenant name, onboarding channel (Agent), and queue code (QREJECT).
            Values are selected from the queryset based on their field names: Customer_name, Application_number, Created_by, Created_timestamp, Rejected_by ,Rejected_timestamp ,Customer type .
            These values are returned

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The data for the agent failed cif details
        """
        params = failed_cif_details_generic(request, SingleCifSpData, "Agent")
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent for downloading",
    )
    @action(
        methods=["POST"], detail=False, url_path="agent_failed_cif_details_sp_export"
    )
    def agent_failed_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_sp_export function is used to export the data of all the failed CIFs created by agents.
        The function takes in a request object and returns an exported CSV file containing details of all failed CIFs created by agents.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Agent",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "agent_failed_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="agent_failed_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent for downloading",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="agent_failed_cif_details_sp_export_pdf",
    )
    def agent_failed_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The agent_failed_cif_details_sp_export_pdf function is used to export the agent_failed_cif_details_sp data as a PDF file.
        The function takes in the request, *args and **kwargs parameters.
        It then creates a tzinfo variable that stores the timezone information of settings.TIMEZONE (which is set to UTC).
        A qs variable is created which queries all SingleCifSpData objects with an onboarding channel of &quot;Agent&quot; and queue code of &quot;QREJECT&quot;. The values() method filters out only certain fields from this queryset: Customer name, Application number, Created by, Created timestamp, Re

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Agent",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "agent_failed_cif_details_sp.pdf",
                "title": "Sole Proprietor Agent Failed Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # -----------------------------------------------------------------------------------------------------------------------
    # Self initiated services for retail

    @extend_schema(
        operation_id="self_started_flow_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_started_flow_retail")
    def self_started_flow_retail(self, request, *args, **kwargs):
        """
        The self_started_flow_retail function is used to get the number of self-started flows for retail customers.

        :param self: Refer to the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of distinct external_reference values in the singlecifretaildata table
        """
        params = started_flow_self_rt_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_cif_created_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_cif_created_retail")
    def self_cif_created_retail(self, request, *args, **kwargs):
        """
        The self_cif_created_retail function is used to get the number of self onboarded retail customers.


        :param self: Refer to the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of distinct external_reference values in the onboarding
        """
        params = cif_created_generic(request, SingleCifRetailData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_cif_failed_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_cif_failed_retail")
    def self_cif_failed_retail(self, request, *args, **kwargs):
        """
        The self_cif_failed_retail function is used to get the number of failed retail CIFs for a given tenant.
        The function takes in a request object and returns the number of failed retail CIFs as an integer.

        :param self: Refer to the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of failed self onboarding retail customers
        """
        params = cif_failed_generic(request, SingleCifRetailData, "Self")
        return get_generic_response(params)

    # BIG NUMBER abandoned (discarded) applications self
    @extend_schema(
        operation_id="self_discarded_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_retail")
    def self_discarded_retail(self, request, *args, **kwargs):
        """
        The self_discarded_retail function is used to get the number of self discarded retail records.

        :param self: Refer to the class itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of self-discarded retail onboarding requests
        :doc-author: Trelent
        """
        params = self_discarded_generic(request, SingleCifRetailData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="self_successful_cif_details_rt")
    def self_successful_cif_details_rt(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_rt function returns a table of all the self onboarding customers who have been approved.
        The function takes in a request object and uses it to query the SingleCifRetailData model for all records that match the following criteria:
            - The tenant name matches that of the current user's tenant name.
            - The onboarding channel is &quot;Self&quot;.
            - The queue code is &quot;QSUCCESS&quot;.  This means that these are customers who have been approved by an approver.  If they were not yet approved, their queue code would be something else (e.g., QPENDING).

        :param self: Pass the instance of the class to which this method belongs
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = successful_cif_details_generic(request, SingleCifRetailData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_successful_cif_details_rt_export"
    )
    def self_successful_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_rt_export function is used to export a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp. Account number 1 and 2 and Customer type.
        The data in this CSV file is filtered by tenant name (the current tenant), onboarding channel (Self) and queue code (QSUCCESS).


        :param self: Refer to the current object
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following fields:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Self",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "self_successful_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="self_successful_cif_details_rt_export_pdf",
    )
    def self_successful_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_rt_export_pdf function is used to export a PDF file containing the details of all self onboarding retail customers who have successfully completed their onboarding process.
        The function takes in the request object and returns a PDF file containing the details of all self onboarding retail customers who have successfully completed their onboarding process.

        :param self: Pass the instance of the class to which this method belongs
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Self",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "self_successful_cif_details_rt.pdf",
                "title": "Retail Self Successful Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="self_failed_cif_details_rt")
    def self_failed_cif_details_rt(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_rt function returns a table of all the failed CIFs for Retail customers.
        The function takes in a request object and returns an items object containing the data to be displayed on the page.

        :param self: Access the class attributes and methods
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of failed cifs for the self onboarding channel
        """
        params = failed_cif_details_generic(request, SingleCifRetailData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_failed_cif_details_rt_export"
    )
    def self_failed_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_rt_export function is used to export the self failed cif details rt data.
            Args:
                request (HttpRequest): The HttpRequest object that contains the query parameters for filtering and sorting.

        :param self: Pass the instance of the class to which this function belongs
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following data
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Self",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "self_failed_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_failed_cif_details_rt_export_pdf"
    )
    def self_failed_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_rt_export_pdf function is used to export the data from the self_failed_cif_details_rt view into a PDF file.
        The function takes in three parameters: request, *args and **kwargs. The request parameter is used to get information about the current web request that has triggered this view.
        The *args and **kwargs are not required for this particular function but they are included as a general rule of thumb when writing Django views.

        :param self: Pass the instance of a class to the function
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Self",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "self_failed_cif_details_rt.pdf",
                "title": "Retail Self Applications Failed",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Self abandoned(discarded) Applications details
    @extend_schema(
        operation_id="self_discarded_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_details_rt")
    def self_discarded_details_rt(self, request, *args, **kwargs):
        """
        The self_discarded_details_rt function returns a table of all the self-discarded retail applications.
        The function takes in a request object and returns an items object which is used to render the table.

        :param self: Access the class attributes
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of all the self-discarded applications
        """
        params = self_discarded_details_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_discarded_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_details_rt_export")
    def self_discarded_details_rt_export(self, request, *args, **kwargs):
        """
        The self_discarded_details_rt_export function is used to export the self discarded details report.
            It takes in a request and returns an exported csv file of the self discarded details report.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following fields:
        """
        params = self_discarded_details_generic(
            request,
            SingleCifRetailData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "self_abandoned_applications.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_discarded_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_discarded_details_rt_export_pdf"
    )
    def self_discarded_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The self_discarded_details_rt_export_pdf function is used to export the self discarded details in pdf format.
            Args:
                request (object): The request object contains all the information about the current HTTP request.

        :param self: Access the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The self_abandoned_applications
        """
        params = self_discarded_details_generic(
            request,
            SingleCifRetailData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "self_abandoned_applications.pdf",
                "title": "Self Abandoned Applications details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # SELF stage reports  for SOLE PROPRIETARY
    @extend_schema(
        operation_id="self_started_flow_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_started_flow_sp")
    def self_started_flow_sp(self, request, *args, **kwargs):
        """
        The self_started_flow_sp function is used to get the number of self-started flows for a given tenant.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A dictionary with the following keys:
        """
        params = started_flow_self_sp_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_cif_created_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by self in SP",
    )
    @action(methods=["POST"], detail=False, url_path="self_cif_created_sp")
    def self_cif_created_sp(self, request, *args, **kwargs):
        """
        The self_cif_created_sp function is used to get the number of self onboarded CIFs that have been created in a given time period.
        The function takes in a request object and returns the number of self onboarded CIFs that have been created.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of cifs created by the user
        """
        params = cif_created_generic(request, SingleCifSpData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_cif_failed_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_cif_failed_sp")
    def self_cif_failed_sp(self, request, *args, **kwargs):
        """
        The self_cif_failed_sp function returns the number of abandoned (discarded) applications for self onboarding channel.
            Args:
                request (object): The request object contains information about the user making this call, including authentication information.

        :param self: Pass the instance of the class to which this method belongs
        :param request: Get the request object
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to functions
        :return: The number of abandoned (discarded) applications self
        """
        params = cif_failed_generic(request, SingleCifSpData, "Self")
        return get_generic_response(params)

    # BIG NUMBER abandoned (discarded) applications self

    @extend_schema(
        operation_id="self_discarded_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_sp")
    def self_discarded_sp(self, request, *args, **kwargs):
        """
        The self_discarded_sp function returns the number of self-discarded SPs.

        :param self: Pass the instance of the class to which this function belongs
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of discarded records by the user
        """
        params = self_discarded_generic(request, SingleCifSpData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_successful_cif_details_sp")
    def self_successful_cif_details_sp(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_sp function returns a list of all the self onboarding customers who have been successfully onboarded.
        The function takes in a request object and uses it to query the SingleCifSpData table for all records that match the following criteria:
            - The tenant name is equal to get_current_tenant_name() (the current tenant)
            - The onboarding channel is equal to &quot;Self&quot; (self-onboarding)
            - The queue code is equal to &quot;QSUCCESS&quot; (successful queue)

        :param self: Pass the instance of the class to the function
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of all the successful cifs created by self onboarding
        """
        params = successful_cif_details_generic(request, SingleCifSpData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_successful_cif_details_sp_export"
    )
    def self_successful_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_sp_export function is used to export a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp. Account number 1 and 2 and Customer type.
        The function filters for records that have been created by the Self onboarding channel and are in the QSUCCESS queue code.

        :param self: Pass the current object to the function
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Self",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "self_successful_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_successful_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="self_successful_cif_details_sp_export_pdf",
    )
    def self_successful_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The self_successful_cif_details_sp_export_pdf function is used to export a PDF file containing the details of all successful self onboarding applications for sole proprietors.
        The function takes in the request object and returns a PDF file containing the details of all successful self onboarding applications for sole proprietors.

        :param self: Represent the instance of the class
        :param request: Get the data from the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Self",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "self_successful_cif_details_sp.pdf",
                "title": "Sole Proprietor Self Successful Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed in self initiated",
    )
    @action(methods=["POST"], detail=False, url_path="self_failed_cif_details_sp")
    def self_failed_cif_details_sp(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_sp function returns a table of all the failed CIFs for the Self channel.
            The function takes in a request object and returns an items object containing the data to be displayed on the page.


        :param self: Pass the instance of the class to which this function belongs
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = failed_cif_details_generic(request, SingleCifSpData, "Self")
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent for downloading",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_failed_cif_details_sp_export"
    )
    def self_failed_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_sp_export function is used to export the self failed cif details sp data.

        :param self: Represent the instance of the class
        :param request: Get the query parameters from the url
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Self",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "self_failed_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_failed_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent for downloading",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_failed_cif_details_sp_export_pdf"
    )
    def self_failed_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The self_failed_cif_details_sp_export_pdf function is used to export the self failed cif details sp data in pdf format.
            Args:
                request (HttpRequest): The HttpRequest object that contains the query parameters for filtering and sorting.

        :param self: Pass the instance of a class to its method
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Self",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "self_failed_cif_details_sp.pdf",
                "title": "Self Applications Failed",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # Self abandoned(discarded) Applications details
    @extend_schema(
        operation_id="self_discarded_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by self",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_details_sp")
    def self_discarded_details_sp(self, request, *args, **kwargs):
        """
        The self_discarded_details_sp function returns a table of all the self-discarded applications for SP.
            The function takes in a request object and returns an items object containing the data to be displayed on the page.

        :param self: Identify the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following data:
        """
        params = self_discarded_details_generic(request, SingleCifSpData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_discarded_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="self_discarded_details_sp_export")
    def self_discarded_details_sp_export(self, request, *args, **kwargs):
        """
        The self_discarded_details_sp_export function is used to export the data of all self-discarded applications in a CSV file.
        The function takes in the request and *args, **kwargs as parameters.
        It then creates a timezone object using pytz library and stores it in tz_info variable.
        Next, it calls query() function from utils module to get queryset for SingleCifSpData model with OnboardingSerializer serializer class applied on it and stores this queryset into qs variable.
        Then, we filter this queryset by tenant name (current tenant), onboarding channel (Self) and

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = self_discarded_details_generic(
            request,
            SingleCifSpData,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "self_abandoned_applications_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="self_discarded_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(
        methods=["POST"], detail=False, url_path="self_discarded_details_sp_export_pdf"
    )
    def self_discarded_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The self_discarded_details_sp_export_pdf function is used to export the self discarded details of a single cif sp data object in pdf format.
            Args:
                request (object): The request object contains information about the current HTTP request.

        :param self: Identify the class that is calling this function
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = self_discarded_details_generic(
            request,
            SingleCifSpData,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Abandoned_by",
                    "Abandoned_timestamp",
                ],
                "fileName": "self_abandoned_applications_sp.pdf",
                "title": "Self Abandoned Applications details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # -----------------------------------------------------------------------------------------------------------------------
    # STAFF inititiated applications for RT and SP

    @extend_schema(
        operation_id="staff_started_flow_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by staff",
    )
    @action(methods=["POST"], detail=False, url_path="staff_started_flow_retail")
    def staff_started_flow_retail(self, request, *args, **kwargs):
        """
        The staff_started_flow_retail function is used to get the number of retail applications that have been started by staff.
        The function takes in a request object and returns a response object containing the count of retail applications that have been started by staff.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A count of the number of distinct external_reference values in the singlecifretaildata table for a given tenant, where queue_code is one of qamend, qverify, qapprove, qsuccess,
        """
        params = staff_started_flow_rt_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_cif_created_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by staff",
    )
    @action(methods=["POST"], detail=False, url_path="staff_cif_created_retail")
    def staff_cif_created_retail(self, request, *args, **kwargs):
        """
        The staff_cif_created_retail function is used to get the number of CIFs created by staff for retail customers.
        The function takes in a request object and returns a response object containing the count of CIFs created by staff for retail customers.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of unique cifs created by staff
        """
        params = cif_created_generic(request, SingleCifRetailData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_cif_failed_retail",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff",
    )
    @action(methods=["POST"], detail=False, url_path="staff_cif_failed_retail")
    def staff_cif_failed_retail(self, request, *args, **kwargs):
        """
        The staff_cif_failed_retail function is used to get the number of failed retail CIFs for a staff user.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of distinct external_reference values for the singlecifretaildata model in the onboarding database schema, where tenant is equal to get_current_tenant_name(), queue code is equal to qreject and onboarding channel is equal to staff
        """
        params = cif_failed_generic(request, SingleCifRetailData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by staff",
    )
    @action(methods=["POST"], detail=False, url_path="staff_successful_cif_details_rt")
    def staff_successful_cif_details_rt(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_rt function is used to return a table of all the successful CIFs created by staff.
        The function takes in a request object and returns an items object which contains the data for the table.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        params = successful_cif_details_generic(request, SingleCifRetailData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_successful_cif_details_rt_export",
    )
    def staff_successful_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_rt_export function is used to export a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp. Account number 1 and 2 and Customer type.
        The function filters for all records in the SingleCifRetailData table that have an onboarding channel of &quot;Staff&quot; and a queue code of &quot;QSUCCESS&quot;.
        It then returns these filtered records as a CSV file.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Staff",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "staff_successful_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_successful_cif_details_rt_export_pdf",
    )
    def staff_successful_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_rt_export_pdf function is used to export a PDF file containing the details of all successful retail staff applications.
        The function takes in a request object and returns an HTTP response object with the PDF file attached.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = successful_cif_details_generic(
            request,
            SingleCifRetailData,
            "Staff",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "staff_successful_cif_details_rt.pdf",
                "title": "Retail Staff Successful Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff",
    )
    @action(methods=["POST"], detail=False, url_path="staff_failed_cif_details_rt")
    def staff_failed_cif_details_rt(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_rt function returns a table of failed CIFs for the staff onboarding channel.
        The function takes in a request object and uses it to query the SingleCifRetailData model, using the OnboardingSerializer serializer.
        It then filters by tenant name, onboarding channel (Staff), queue code (QREJECT), and values for Customer_name, Application_number, Created_by, Created_timestamp, Rejected_by ,Rejected timestamp ,Customer type . It then returns items as a table.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = failed_cif_details_generic(request, SingleCifRetailData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_rt_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff",
    )
    @action(
        methods=["POST"], detail=False, url_path="staff_failed_cif_details_rt_export"
    )
    def staff_failed_cif_details_rt_export(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_rt_export function is used to export the staff failed cif details report.
            It takes in a request and returns a response containing the exported file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Staff",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "staff_failed_cif_details_rt.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_failed_cif_details_rt_export_pdf",
    )
    def staff_failed_cif_details_rt_export_pdf(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_rt_export_pdf function is used to export the staff failed cif details retail data in a pdf format.
        The function takes in request, *args and **kwargs as parameters.
        It returns items.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifRetailData,
            "Staff",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Customer_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "staff_failed_cif_details_rt.pdf",
                "title": "Retail Staff Applications Failed",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # STAFF stage reports  for SOLE PROPRIETARY
    @extend_schema(
        operation_id="staff_started_flow_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="staff_started_flow_sp")
    def staff_started_flow_sp(self, request, *args, **kwargs):
        """
        The staff_started_flow_sp function is used to get the number of flows started by staff for Single CIF SP.
            It takes in a request object and returns a response object containing the count of flows started by staff for Single CIF SP.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The count of distinct external_reference values in the onboarding database,
        """
        params = staff_started_flow_sp_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_cif_created_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications successfully completed by staff in SP",
    )
    @action(methods=["POST"], detail=False, url_path="staff_cif_created_sp")
    def staff_cif_created_sp(self, request, *args, **kwargs):
        """
        The staff_cif_created_sp function is used to get the number of CIFs created by staff.
            ---
            # YAML (must be separated by `---`)

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of distinct external references
        """
        params = cif_created_generic(request, SingleCifSpData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_cif_failed_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="staff_cif_failed_sp")
    def staff_cif_failed_sp(self, request, *args, **kwargs):
        """
        The staff_cif_failed_sp function is used to get the number of failed CIFs for staff onboarding.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of failed cifs
        :doc-author: Trelent
        """
        params = cif_failed_generic(request, SingleCifSpData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications started by agent",
    )
    @action(methods=["POST"], detail=False, url_path="staff_successful_cif_details_sp")
    def staff_successful_cif_details_sp(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_sp function is used to return a table of all the successful CIFs created by staff.
        The function takes in a request object and returns an items object which contains the data for the table.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        params = successful_cif_details_generic(request, SingleCifSpData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_successful_cif_details_sp_export",
    )
    def staff_successful_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_sp_export function is used to export a CSV file containing the following fields:
        Customer_name, Application_number, Created_by, Created_timestamp, Approved_by, Approved_timestamp. Account number 1 and 2 are also included in this function.


        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of successful cif details for the staff channel
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Staff",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "staff_successful_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_successful_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications details by agent for downloading in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_successful_cif_details_sp_export_pdf",
    )
    def staff_successful_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The staff_successful_cif_details_sp_export_pdf function is used to export a PDF file containing the details of all successful applications for sole proprietorships submitted by staff.
        The function takes in a request object and returns an HttpResponse object with the PDF file attached.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file with the following fields:
        """
        params = successful_cif_details_generic(
            request,
            SingleCifSpData,
            "Staff",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Account_number_1",
                    "Account_number_2",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Approved_by",
                    "Approved_timestamp",
                ],
                "fileName": "staff_successful_cif_details_sp.pdf",
                "title": "Sole Proprietor Staff Successful Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by agent",
    )
    @action(methods=["POST"], detail=False, url_path="staff_failed_cif_details_sp")
    def staff_failed_cif_details_sp(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_sp function returns a table of all the failed CIFs for the Staff channel.
            The function takes in a request object and uses it to query the SingleCifSpData model, which is then serialized using OnboardingSerializer.
            The queryset is filtered by tenant name, onboarding channel (Staff), and queue code (QREJECT).
            Values are selected from this queryset based on their field names: Customer_name, Application_number, Created_by, Created_timestamp, Rejected_by ,Rejected_timestamp ,Customer type .
            These values

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following fields:
        """
        params = failed_cif_details_generic(request, SingleCifSpData, "Staff")
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_sp_export",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff for downloading",
    )
    @action(
        methods=["POST"], detail=False, url_path="staff_failed_cif_details_sp_export"
    )
    def staff_failed_cif_details_sp_export(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_sp_export function is used to export the staff failed cif details sp data.
            Args:
                request (HttpRequest): The HttpRequest object that contains the query parameters for filtering and sorting.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Staff",
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "staff_failed_cif_details_sp.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="staff_failed_cif_details_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications failed by staff for downloading",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="staff_failed_cif_details_sp_export_pdf",
    )
    def staff_failed_cif_details_sp_export_pdf(self, request, *args, **kwargs):
        """
        The staff_failed_cif_details_sp_export_pdf function is used to export the staff failed cif details sp data in pdf format.
            Args:
                request (HttpRequest): The HttpRequest object that contains the query parameters for filtering and sorting.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        params = failed_cif_details_generic(
            request,
            SingleCifSpData,
            "Staff",
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Application_number",
                    "Business_name",
                    "Customer_type",
                    "Created_by",
                    "Created_timestamp",
                    "Rejected_by",
                    "Rejected_timestamp",
                ],
                "fileName": "staff_failed_cif_details_sp.pdf",
                "title": "Sole Proprietor Staff Failed Applications",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # -----------------------------------------------------------------------------------------------------------------------
    # OVERALL  Application stage report

    @extend_schema(
        operation_id="applications_with_maker_bigNo_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with makers",
    )
    @action(methods=["POST"], detail=False, url_path="applications_with_maker_bigNo_rt")
    def applications_with_maker_bigNo_rt(self, request, *args, **kwargs):
        """
        The applications_with_maker_bigNo_rt function returns the number of applications with maker bigNo_rt.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of applications with maker and bigno in the queue qamend or qtemp
        """
        params = applications_with_maker_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_with_maker_bigNo_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with makers",
    )
    @action(methods=["POST"], detail=False, url_path="applications_with_maker_bigNo_sp")
    def applications_with_maker_bigNo_sp(self, request, *args, **kwargs):
        """
        The applications_with_maker_bigNo_sp function returns the number of applications with maker bigNo_sp.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications that are in the queue_code qamend or qtemp
        """
        params = applications_with_maker_bigno_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # applications with verifiers
    @extend_schema(
        operation_id="applications_with_verifier_bigNo_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with vierifier",
    )
    @action(
        methods=["POST"], detail=False, url_path="applications_with_verifier_bigNo_rt"
    )
    def applications_with_verifier_bigNo_rt(self, request, *args, **kwargs):
        """
        The applications_with_verifier_bigNo_rt function returns the number of applications with verifier bigNo.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications with the verifier bigno_rt
        """
        params = applications_with_verifier_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_with_verifier_bigNo_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with verifier",
    )
    @action(
        methods=["POST"], detail=False, url_path="applications_with_verifier_bigNo_sp"
    )
    def applications_with_verifier_bigNo_sp(self, request, *args, **kwargs):
        """
        The applications_with_verifier_bigNo_sp function returns the number of applications with verifier bigNo_sp.

        :param self: Represent the instance of a class
        :param request: Get the tenant name from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications in the qverify queue
        """
        params = applications_with_verifier_bigno_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # applications with approvers
    @extend_schema(
        operation_id="applications_with_approvers_bigno_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="applications_with_approvers_bigno_rt"
    )
    def applications_with_approvers_bigno_rt(self, request, *args, **kwargs):
        """
        The applications_with_approvers_bigno_rt function returns the number of applications with approvers for a given tenant.

        :param self: Represent the instance of a class
        :param request: Get the tenant name from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications that are in the qapprove queue
        """
        params = applications_with_approvers_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_with_approvers_bigno_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications with approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="applications_with_approvers_bigno_sp"
    )
    def applications_with_approvers_bigno_sp(self, request, *args, **kwargs):
        """
        The applications_with_approvers_bigno_sp function returns the number of applications with approvers for a given tenant.

        :param self: Represent the instance of a class
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications that have been approved
        """
        params = applications_with_approvers_bigno_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # applications processed that is completed successfully

    @extend_schema(
        operation_id="applications_processed_bigNo_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of  applications processed",
    )
    @action(methods=["POST"], detail=False, url_path="applications_processed_bigNo_rt")
    def applications_processed_bigNo_rt(self, request, *args, **kwargs):
        """
        The applications_processed_bigNo_rt function returns the number of applications processed by the system.
            ---
            # YAML (must be separated by `---`)

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications processed
        """
        params = applications_processed_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_processed_bigNo_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications processed.",
    )
    @action(methods=["POST"], detail=False, url_path="applications_processed_bigNo_sp")
    def applications_processed_bigNo_sp(self, request, *args, **kwargs):
        """
        The applications_processed_bigNo_sp function returns the number of applications processed by BigNo.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications processed by the tenant
        """
        params = applications_processed_bigno_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # applications rejected overall

    @extend_schema(
        operation_id="applications_rejected_bigNo_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications rejected",
    )
    @action(methods=["POST"], detail=False, url_path="applications_rejected_bigNo_rt")
    def applications_rejected_bigNo_rt(self, request, *args, **kwargs):
        """
        The applications_rejected_bigNo_rt function returns the number of rejected applications for a given tenant.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications rejected
        """
        params = applications_rejected_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    @extend_schema(
        operation_id="applications_rejected_bigNo_sp",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications rejected.",
    )
    @action(methods=["POST"], detail=False, url_path="applications_rejected_bigNo_sp")
    def applications_rejected_bigNo_sp(self, request, *args, **kwargs):
        """
        The applications_rejected_bigNo_sp function returns the number of rejected applications for a given tenant.
            ---
            # YAML (must be separated by `---`)

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications that were rejected by the bank
        """
        params = applications_rejected_bigno_generic(request, SingleCifSpData)
        return get_generic_response(params)

    # applications  that were in exception are only for retail

    @extend_schema(
        operation_id="applications_exceptions_bigNo_rt",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications exceptions.",
    )
    @action(methods=["POST"], detail=False, url_path="applications_exceptions_bigNo_rt")
    def applications_exceptions_bigNo_rt(self, request, *args, **kwargs):
        """
        The applications_exceptions_bigNo_rt function returns the number of applications in the exceptions queue with a big no.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of applications that have a queue_code of qexception
        """
        params = applications_exceptions_bigno_generic(request, SingleCifRetailData)
        return get_generic_response(params)

    # ---------------------------------------------------------------------------------------------------------------
    # Stacked bar charts for all 3 onboarding channel for SP
    @extend_schema(
        operation_id="overall_application_stages_sp_stacked",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications at each stage of processing for all 3 channels",
    )
    @action(
        methods=["POST"], detail=False, url_path="overall_application_stages_sp_stacked"
    )
    def overall_application_stages_sp_stacked(self, request, *args, **kwargs):
        """
        The overall_application_stages_sp_stacked function is used to return a list of dictionaries containing the number of applications in each stage for each channel.
        The function takes in a request object and returns a Response object with the data.


        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response = overall_application_stages_sp_stacked_generic(request)
        return Response(response)

    # Stacked bar charts for all 3 onboarding channel for RT

    @extend_schema(
        operation_id="overall_application_stages_rt_stacked",
        tags=[AuthTags.AUTHORIZE],
        description="The number of applications at each stage of processing for all 3 channels",
    )
    @action(
        methods=["POST"], detail=False, url_path="overall_application_stages_rt_stacked"
    )
    def overall_application_stages_rt_stacked(self, request, *args, **kwargs):
        """
        The overall_application_stages_rt_stacked function is used to return the number of applications in each stage for each channel.
        The function takes a request object as an argument and returns a response object containing the data required by the frontend.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries as shown below
        """
        response = overall_application_stages_rt_stacked_generic(request)
        return Response(response)

    # PIE charts for RT
    @extend_schema(
        operation_id="agent_queuecodes_pie_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in RT of agents application",
    )
    @action(methods=["POST"], detail=False, url_path="agent_queuecodes_pie_rt")
    def agent_queuecodes_pie_rt(self, request, *args, **kwargs):
        """
        The agent_queuecodes_pie_rt function is used to generate a pie chart that shows the number of onboarding records in each queue code for Retail customers.
        The function takes in a request object and returns a Response object containing the data needed to render the pie chart.

        :param self: Represent the instance of the class
        :param request: Get the current request
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        response = queuecodes_pie_rt_generic(request, "Agent")
        return Response(response)

    # RT for staff
    @extend_schema(
        operation_id="staff_queuecodes_pie_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in RT of staff application",
    )
    @action(methods=["POST"], detail=False, url_path="staff_queuecodes_pie_rt")
    def staff_queuecodes_pie_rt(self, request, *args, **kwargs):
        """
        The staff_queuecodes_pie_rt function is used to generate a pie chart of the number of onboarding records in each queue code for staff-originated onboarding records.
        The function takes in a request object and returns a Response object containing the data needed to render the pie chart.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries with the following keys:
        """
        response = queuecodes_pie_rt_generic(request, "Staff")
        return Response(response)

    # RT for self
    @extend_schema(
        operation_id="self_queuecodes_pie_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in RT of self application",
    )
    @action(methods=["POST"], detail=False, url_path="self_queuecodes_pie_rt")
    def self_queuecodes_pie_rt(self, request, *args, **kwargs):
        """
        The self_queuecodes_pie_rt function is used to generate a pie chart of the number of onboarding records in each queue code for self-service retail customers.
        The function takes in a request object and returns a Response object containing the data needed to render the pie chart.

        :param self: Refer to the current object
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A queryset of onboarding data
        """
        response = self_queuecodes_pie_rt_generic(request)
        return Response(response)

    # Pie charts for SP (no exceptions (for all 3) and discarded for agent and staff)

    @extend_schema(
        operation_id="agent_queuecodes_pie_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in RT of agents application",
    )
    @action(methods=["POST"], detail=False, url_path="agent_queuecodes_pie_sp")
    def agent_queuecodes_pie_sp(self, request, *args, **kwargs):
        """
        The agent_queuecodes_pie_sp function is used to generate a pie chart of the number of Single CIFs in each queue code.
        The function takes in a request and returns a response containing the data for the pie chart.

        :param self: Represent the instance of the class
        :param request: Get the request object, which contains all the information about the current request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries with the following keys:
        """
        response = queuecodes_pie_sp_generic(request, "Agent")
        return Response(response)

    # RT for staff
    @extend_schema(
        operation_id="staff_queuecodes_pie_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in sp of staff application",
    )
    @action(methods=["POST"], detail=False, url_path="staff_queuecodes_pie_sp")
    def staff_queuecodes_pie_sp(self, request, *args, **kwargs):
        """
        The staff_queuecodes_pie_sp function is used to generate a pie chart of the number of Single CIFs in each queue code.
        The function takes in a request and returns a Response object containing the data for the pie chart.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries with the following structure:
        """
        response = queuecodes_pie_sp_generic(request, "Staff")
        return Response(response)

    # SP for self
    @extend_schema(
        operation_id="self_queuecodes_pie_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display count of number quecodes in each category in sp of self application",
    )
    @action(methods=["POST"], detail=False, url_path="self_queuecodes_pie_sp")
    def self_queuecodes_pie_sp(self, request, *args, **kwargs):
        """
        The self_queuecodes_pie_sp function is used to generate a pie chart of the number of onboarding records in each queue code for self-service onboarding.
        The function takes in a request, and returns a response containing the data needed to create the pie chart.

        :param self: Refer to the current instance of the class
        :param request: Get the current tenant name
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries with the following keys:
        """
        response = self_queuecodes_pie_sp_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="kyc_account_opening_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display the details for kyc vs account opening details"
    )
    @action(methods=["POST"], detail=False, url_path="kyc_account_opening_details")
    def kyc_account_opening_details(self, request, *args, **kwargs):
        response = kyc_account_opening_details_generic(request)
        return get_generic_response(response)

    @extend_schema(
        operation_id="kyc_account_opening_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display the details for kyc vs account opening details"
    )
    @action(methods=["POST"], detail=False, url_path="kyc_account_opening_details_export_csv")
    def kyc_account_opening_details_export_csv(self, request, *args, **kwargs):
        response = kyc_account_opening_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames":
                    [
                        "Kyc_reference",
                        "Application_Reference_Number",
                        "Mobile_Number",
                        "Email",
                        "First_Name",
                        "Last_Name",
                        "Kyc_state",
                        "Account_opening_status",
                        "Create_timestamp",
                        "Last_modified_timestamp"
                    ],
                "fileName": "Kyc_Account_Opening_Details.csv"
            }
        )
        return get_generic_response(response)

    @extend_schema(
        operation_id="kyc_account_opening_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display the details for kyc vs account opening details"
    )
    @action(methods=["POST"], detail=False, url_path="kyc_account_opening_details_export_pdf")
    def kyc_account_opening_details_export_pdf(self, request, *args, **kwargs):
        response = kyc_account_opening_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Kyc_reference",
                    "Application_Reference_Number",
                    "Mobile_Number",
                    "Email",
                    "First_Name",
                    "Last_Name",
                    "Kyc_state",
                    "Account_opening_status",
                    "Create_timestamp",
                    "Last_modified_timestamp"
                ],
                "fileName": "Kyc_Account_Opening_Details.pdf",
                "title": "KYC vs Account Opening Details",
                "user": request.user.username,
            }
        )
        return get_generic_response(response)
