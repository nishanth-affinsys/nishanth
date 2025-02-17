from auth.tags import AuthTags

from drf_spectacular.utils import extend_schema

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action


from main.settings import MAX_PDF_LIMIT
from onboarding.models import SingleCifRetailData, SingleCifSpData
from main.utils.export import export_csv, export_pdf
from main.utils.boiler_plate import (
    return_table,
)

from onboarding.services.onboarding_ageing_report_utils import (
    application_ageing_report_rt_generic,
    application_ageing_report_sp_generic,
    scheduled_ageing_report_agent_generic,
    scheduled_ageing_report_generic,
)

# constants for RT
app_type_ntb_rt = "Retail New"
app_type_etb_rt = "Retail Secondary"
cust_type_ntb_rt = "RT-NEW"
cust_type_etb_rt = "RT-EXT"

# constants for SP
app_type_ntb_sp = "SP New"
app_type_etb_sp = "SP Secondary"
cust_type_ntb_sp = "SP-NEW"
cust_type_etb_sp = "SP-EXT"

channel_staff = "Staff"
app_source_staff = "STAFF-ASSISTED"

channel_self = "Self"
app_source_self = "SELF-SERVICE"


class AgeingReportViewSet(GenericViewSet):
    @extend_schema(
        operation_id="application_ageing_report_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display overall ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="application_ageing_report_rt")
    def application_ageing_report_rt(self, request, *args, **kwargs):
        """
        The application_ageing_report_rt function returns a table of all the applications in the retail onboarding process.
        The columns are: Customer_name, Application_number, Stage, Ageing (in days), Mode and Created_timestamp.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, _, _ = application_ageing_report_rt_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="application_ageing_report_rt_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download overall ageing for Retail as a csv ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="application_ageing_report_rt_export_csv",
    )
    def application_ageing_report_rt_export_csv(self, request, *args, **kwargs):
        """
        The application_ageing_report_rt_export_csv function is used to export the application ageing report for retail customers in CSV format.
        The function takes a request object as an argument and returns a response object containing the exported CSV file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names, file_name = application_ageing_report_rt_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # pdf for retail ageing
    @extend_schema(
        operation_id="application_ageing_report_rt_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download overall ageing for Retail as a pdf ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="application_ageing_report_rt_export_pdf",
    )
    def application_ageing_report_rt_export_pdf(self, request, *args, **kwargs):
        """
        The application_ageing_report_rt_export_pdf function is used to export the retail ageing report as a PDF file.
        It takes in a request object and returns an items object which contains the data that will be exported as a PDF file.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A response object with the following attributes:
        """
        response, field_names, file_name = application_ageing_report_rt_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Retail Ageing Report",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="application_ageing_report_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display overall ageing for SP ",
    )
    @action(methods=["POST"], detail=False, url_path="application_ageing_report_sp")
    def application_ageing_report_sp(self, request, *args, **kwargs):
        """
        The application_ageing_report_sp function returns a list of dictionaries containing the following keys:
            Business_name, Application_number, Stage,  Ageing (in days), Mode and Created_timestamp.
            The values for these keys are obtained from the SingleCifSpData table in the database.


        :param self: Represent the instance of the class
        :param request: Get the query parameters from the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, _, _ = application_ageing_report_sp_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="application_ageing_report_sp_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download overall ageing for SP ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="application_ageing_report_sp_export_csv",
    )
    def application_ageing_report_sp_export_csv(self, request, *args, **kwargs):
        """
        The application_ageing_report_sp_export_csv function is used to export the application ageing report for single premium products.
        It takes in a request object and returns an exported csv file containing the data from the application ageing report for single premium products.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file
        """
        response, field_names, file_name = application_ageing_report_sp_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    # pdf for ageing reports sp
    @extend_schema(
        operation_id="application_ageing_report_sp_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to download overall ageing for SP ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="application_ageing_report_sp_export_pdf",
    )
    def application_ageing_report_sp_export_pdf(self, request, *args, **kwargs):
        """
        The application_ageing_report_sp_export_pdf function is used to export the application ageing report for sole proprietors in PDF format.
        The function takes a request object as an argument and returns a response object containing the exported data.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A file that is downloaded
        """
        response, field_names, file_name = application_ageing_report_sp_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Retail Ageing Report",
            request.user.username,
        )
        return items

    # QUERIES for scheduled report for RT
    # Query for agent retail

    @extend_schema(
        operation_id="scheduled_ageing_report_agent_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_rt")
    def scheduled_ageing_report_agent_rt(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_agent_rt function is used to generate a report of all the applications that are in
        the Agent assisted channel and have been created by an agent. The report will contain the following fields:
        Application_number, Application_type, Application_source, Application_status, Agent Email Address (Agent ID),
        Application Create Date (Date when application was created), Ageing (in days) from creation date till now.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries containing the data to be displayed in the table
        """
        result, _ = scheduled_ageing_report_agent_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
        )
        return return_table(result, request)

    # csv for agent retail
    @extend_schema(
        operation_id="scheduled_ageing_report_agent_rt_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_rt_csv"
    )
    def scheduled_ageing_report_agent_rt_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_agent_rt_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status, Agent Email Address (Agent ID),
        Application Create Date (YYYY-MM-DD), Ageing in Days (Ageing = Current Date - Create Timestamp), Branch Code of Originator
        (Branch Code of User who created the application), CIF Number 1 and 2. The function filters for applications that are either
        pending for verification or approval or have been Pending for review by an agent. It also filters out any applications that were not created by an agent.&quot;

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names = scheduled_ageing_report_agent_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
        )
        items = export_csv(response, field_names, "ageing_retail_agent_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_agent_rt_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_rt_pdf"
    )
    def scheduled_ageing_report_agent_rt_pdf(self, request, *args, **kwargs):
        response, field_names = scheduled_ageing_report_agent_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "ageing_retail_agent_reports.pdf",
            "Ageing Report Retail (Agent)",
            request.user.username,
        )
        return items

    # For Staff assisted retail
    @extend_schema(
        operation_id="scheduled_ageing_report_staff_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_rt")
    def scheduled_ageing_report_staff_rt(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_rt function is used to generate a report of all the retail applications that are
        pending for verification, pending for approval and Pending for review. The report also shows the ageing of each application in days.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, _ = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_staff,
            app_source_staff,
        )
        return return_table(result, request)

    # csv for staff retail
    @extend_schema(
        operation_id="scheduled_ageing_report_staff_rt_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_rt_csv"
    )
    def scheduled_ageing_report_staff_rt_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_rt_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status,
        Application_create_date, Ageing (in days), Branch code of creation branch , CIF number of customer ,
        Account number 1 and 2 (if any) and Customer type. The function filters out all records that are not in the QVERIFY or QEXCEPTION queues. It also filters out all records that have an age less than one day.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_staff,
            app_source_staff,
        )
        items = export_csv(result, field_names, "ageing_retail_staff_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_staff_rt_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_rt_pdf"
    )
    def scheduled_ageing_report_staff_rt_pdf(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_rt_pdf function is used to generate a PDF report of all the Retail Staff-Assisted applications that are pending for verification, approval or Pending for review.
        The function takes in the request and returns a PDF file containing all the required information.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_staff,
            app_source_staff,
        )
        if len(result) > MAX_PDF_LIMIT:
            result = result[:MAX_PDF_LIMIT]
        items = export_pdf(
            result,
            field_names,
            "ageing_retail_staff_reports.pdf",
            "Ageing Report Retail (Staff)",
            request.user.username,
        )
        return items

    # self report for rt
    @extend_schema(
        operation_id="scheduled_ageing_report_self_rt",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_rt")
    def scheduled_ageing_report_self_rt(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_rt function is used to generate a report of all the Retail applications that are
            created by Self-Service channel. The report contains the following fields: Application Number, Application Type,
            Application Source, Application Status, Ageing (in days), Branch Code and CIF. This function is called from
            scheduled_ageing_report viewset.

        :param self: Pass the instance of the class to which this method belongs
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table of all the pending applications for self-service retail customers
        """
        result, _ = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_self,
            app_source_self,
        )
        return return_table(result, request)

    # CSV FOR self reports retail

    @extend_schema(
        operation_id="scheduled_ageing_report_self_rt_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_rt_csv"
    )
    def scheduled_ageing_report_self_rt_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_rt_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status,
        Application_create_date, Ageing (in days), Branch code of creation branch , CIF number of customer ,
        Account number 1 and 2 (if any) and Customer type. The function filters out all records that are not in the QVERIFY or QEXCEPTION queues. It also filters out all records that were created by an agent.

        :param self: Refer to the object itself
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_self,
            app_source_self,
        )
        items = export_csv(result, field_names, "ageing_retail_self_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_self_rt_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_rt_pdf"
    )
    def scheduled_ageing_report_self_rt_pdf(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_rt_pdf function is used to generate a PDF report of all the Retail Self-Service applications that are pending for verification, approval or Pending for review.
        The function takes in no parameters and returns a PDF file containing the following fields:
        Application_number, Application_type, Application_source, Application_status,
        Application_create_date (the date on which the application was created), Ageing (the number of days since creation), Branch code (of branch where application was created), CIF number(s) associated with account(s) in application form , Account Number 1 and 2 associated with CIF numbers provided in form , Customer

        :param self: Refer to the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifRetailData,
            app_type_ntb_rt,
            app_type_etb_rt,
            cust_type_ntb_rt,
            cust_type_etb_rt,
            channel_self,
            app_source_self,
        )
        if len(result) > MAX_PDF_LIMIT:
            result = result[:MAX_PDF_LIMIT]
        items = export_pdf(
            result,
            field_names,
            "ageing_retail_self_reports.pdf",
            "Ageing Report Retail (Self)",
            request.user.username,
        )
        return items

    # ------------------------------------------------------------------------------------------
    # SP REPORTS

    @extend_schema(
        operation_id="scheduled_ageing_report_agent_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_sp")
    def scheduled_ageing_report_agent_sp(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_agent_sp function is used to generate the scheduled ageing report for agent assisted SP applications.
        The function takes in a request object and returns a table of data containing the following fields:
        Application_number, Application_type, Application_source, Application_status, Agent Email Address (Agent ID),
        Application Create Date (DD/MM/YYYY), Ageing (in days) from application create date till current date and time
        (including weekends &amp; public holidays), Branch Code where application was created at by agent user.

        :param self: Represent the instance of the class
        :param request: Get the request object from the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table with the following columns:
        """
        result, _ = scheduled_ageing_report_agent_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
        )
        return return_table(result, request)

    # csv for agent sp
    @extend_schema(
        operation_id="scheduled_ageing_report_agent_sp_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_sp_csv"
    )
    def scheduled_ageing_report_agent_sp_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_agent_sp_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status, Agent Email Address (Agent ID),
        Application Create Date (DD/MM/YYYY), Ageing in Days (Ageing of application from creation date till now), Branch Code
        (Branch where application was created by agent) , CIF Number , Account Number 1 , Account Number 2 and Customer Type. The function filters out all applications that are not created by agents and also filters out all applications that are not in the QVERIFY or QEXCEPTION or

        :param self: Represent the instance of the class
        :param request: Get the request object which contains information about the current http request
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        response, field_names = scheduled_ageing_report_agent_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
        )
        items = export_csv(response, field_names, "ageing_sp_agent_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_agent_sp_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for Retail",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_agent_sp_pdf"
    )
    def scheduled_ageing_report_agent_sp_pdf(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_agent_sp_pdf function is used to generate a PDF report of all the Sole Proprietor applications that are in the QVERIFY, QEXCEPTION and QAPPROVE queues.
        The function takes in no parameters and returns a PDF file containing all the required information.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The following:
        """
        response, field_names = scheduled_ageing_report_agent_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "ageing_sp_agent_reports.pdf",
            "Sole Proprietor Ageing Reports (Agent)",
            request.user.username,
        )
        return items

    # For Staff assisted sp
    @extend_schema(
        operation_id="scheduled_ageing_report_staff_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for SP",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_sp")
    def scheduled_ageing_report_staff_sp(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_sp function is used to generate a report of all the applications that are in
        the QVERIFY, QEXCEPTION and QAPPROVE queues for staff assisted onboarding. The function takes in a request object as an
        argument and returns the data as JSON objects.

        :param self: Represent the instance of the class
        :param request: Get the current request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A table that contains the following columns:
        """
        result, _ = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_staff,
            app_source_staff,
        )
        return return_table(result, request)

    # csv for staff retail
    @extend_schema(
        operation_id="scheduled_ageing_report_staff_sp_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for sp",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_sp_csv"
    )
    def scheduled_ageing_report_staff_sp_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_sp_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status,
        Application_create_date, Ageing (in days), Branch code of creation branch , CIF number of customer ,
        Account number 1 and 2 (if any) and Customer type. The function filters out all records that are not in the QVERIFY or QEXCEPTION or QAPPROVE queues. It also filters out all records that have an onboarding channel other than Staff.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of dictionaries
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_staff,
            app_source_staff,
        )
        items = export_csv(result, field_names, "ageing_sp_staff_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_staff_sp_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Agent ageing for sp",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_staff_sp_pdf"
    )
    def scheduled_ageing_report_staff_sp_pdf(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_staff_sp_pdf function is used to generate a PDF report of all the Sole Proprietor applications that are in the QVERIFY, QEXCEPTION and QAPPROVE queues.
        The function takes in request as an argument and returns a PDF file containing all the required information.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_staff,
            app_source_staff,
        )
        if len(result) > MAX_PDF_LIMIT:
            result = result[:MAX_PDF_LIMIT]
        items = export_pdf(
            result,
            field_names,
            "ageing_sp_staff_reports.pdf",
            "Sole Proprietor Ageing Reports (Staff)",
            request.user.username,
        )
        return items

    # self report for sp
    @extend_schema(
        operation_id="scheduled_ageing_report_self_sp",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for SP",
    )
    @action(methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_sp")
    def scheduled_ageing_report_self_sp(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_sp function is used to generate a report of all the applications that are in
        the Self-Service channel and have been created by the user. The function takes in a request object as an argument,
        and returns a table containing all the relevant information.

        :param self: Pass the instance of the class to which this method belongs
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        result, _ = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_self,
            app_source_self,
        )
        return return_table(result, request)

    # CSV FOR self reports sp

    @extend_schema(
        operation_id="scheduled_ageing_report_self_sp_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for sp",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_sp_csv"
    )
    def scheduled_ageing_report_self_sp_csv(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_sp_csv function is used to generate a CSV file containing the following fields:
        Application_number, Application_type, Application_source, Application_status,
        Application_create_date, Ageing (in days), Branch code of application creation branch , CIF number of customer ,
        Account number 1 (if any) , Account number 2 (if any) , Customer type and Created by. The function filters out all records that are not related to Self-service applications for SP customers. It also filters out all records that do not have a queue code of QVERIFY or QEXCEPTION or QAPPROVE

        :param self: Refer to the object itself
        :param request: Get the request object from the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A csv file with the following columns:
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_self,
            app_source_self,
        )
        items = export_csv(result, field_names, "ageing_sp_self_reports.csv")
        return items

    @extend_schema(
        operation_id="scheduled_ageing_report_self_sp_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display Self ageing for sp",
    )
    @action(
        methods=["POST"], detail=False, url_path="scheduled_ageing_report_self_sp_pdf"
    )
    def scheduled_ageing_report_self_sp_pdf(self, request, *args, **kwargs):
        """
        The scheduled_ageing_report_self_sp_pdf function is used to generate a PDF report of the Sole Proprietor Self Service
           applications that are pending for verification, approval or Pending for review. The report will display the application number,
           type, source and status as well as the date it was created on. It will also display the ageing in days since creation.

        :param self: Refer to the class itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A pdf file
        """
        result, field_names = scheduled_ageing_report_generic(
            request,
            SingleCifSpData,
            app_type_ntb_sp,
            app_type_etb_sp,
            cust_type_ntb_sp,
            cust_type_etb_sp,
            channel_self,
            app_source_self,
        )
        if len(result) > MAX_PDF_LIMIT:
            result = result[:MAX_PDF_LIMIT]
        items = export_pdf(
            result,
            field_names,
            "ageing_sp_self_reports.pdf",
            "Sole Proprietor Ageing Reports (Self)",
            request.user.username,
        )
        return items
