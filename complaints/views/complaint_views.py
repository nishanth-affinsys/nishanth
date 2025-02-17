from auth.tags import AuthTags

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from complaints.services.complaint_utils import (
    total_tickets_created_generic,
    assigned_tickets_generic,
    unassigned_tickets_generic,
    resolved_tickets_bigno_generic,
    unresolved_tickets_bigno_generic,
    closed_tickets_bigno_generic,
    ticket_timeline_generic,
    source_ticket_status_generic,
    ticket_user_priority_generic,
    username_status_tickets_generic,
    username_resolved_monthly_generic,
    category_priority_tickets_bar_generic,
    category_status_tickets_generic,
    category_resolved_tickets_monthly_generic,
    ticket_total_time_spent_generic,
    resolved_tickets_monthly_graph_generic,
    open_closed_monthly_tickets_generic,
    tickets_assignee_escalation_generic,
    tickets_floating_escalation_generic,
    tickets_category_piechart_generic,
    tickets_priority_piechart_generic,
    sla_breached_unbreached_generic,
    resolved_tickets_details_generic,
    tickets_escalation_details_generic,
    resolved_after_sla_breach_generic,
    assignee_status,
    email_tickets_details,
)
from main.settings import MAX_PDF_LIMIT

from main.utils.boiler_plate import return_table, get_generic_response
from main.utils.export import export_csv, export_pdf
from drf_spectacular.utils import extend_schema


class ComplaintManagementViewSet(GenericViewSet):
    @extend_schema(
        operation_id="complaints_total_tickets_created",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets created",
    )
    @action(methods=["POST"], detail=False, url_path="complaints_total_tickets_created")
    def total_tickets_created(self, request, *args, **kwargs):
        result = total_tickets_created_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_assigned_tickets",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets that are assigned to the users",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_assigned_tickets")
    def assigned_tickets(self, request, *args, **kwargs):
        result = assigned_tickets_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_unassigned_tickets",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets that are unassigned to any users",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_unassigned_tickets")
    def unassigned_tickets(self, request, *args, **kwargs):
        result = unassigned_tickets_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_resolved_tickets_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets that are resolved to any users",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_resolved_tickets_bigno")
    def resolved_tickets_bigno(self, request, *args, **kwargs):
        result = resolved_tickets_bigno_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_unresolved_tickets_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets that are unresolved to any users",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_unresolved_tickets_bigno"
    )
    def unresolved_tickets_bigno(self, request, *args, **kwargs):
        result = unresolved_tickets_bigno_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_closed_tickets_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="The big number displays the total number of tickets that are closed",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_closed_tickets_bigno")
    def closed_tickets_bigno(self, request, *args, **kwargs):
        result = closed_tickets_bigno_generic(request)
        return Response(data={"count": result})

    @extend_schema(
        operation_id="complaint_ticket_timeline",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the complete timeline of a ticket",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_ticket_timeline")
    def ticket_timeline(self, request, *args, **kwargs):
        params = ticket_timeline_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="complaint_ticket_timeline_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the complete timeline of a ticket",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_ticket_timeline_export_csv"
    )
    def ticket_timeline_csv(self, request, *args, **kwargs):
        params = ticket_timeline_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "SRN",
                    "Assignee_Name",
                    "Status",
                    "Priority",
                    "Created_Timestamp",
                    "Last_Updated_Timestamp",
                ],
                "fileName": "tickets_timeline.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="complaint_ticket_timeline_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the complete timeline of a ticket",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_ticket_timeline_export_pdf"
    )
    def ticket_timeline_pdf(self, request, *args, **kwargs):
        params = ticket_timeline_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "SRN",
                    "Assignee_Name",
                    "Status",
                    "Priority",
                    "Created_Timestamp",
                    "Last_Updated_Timestamp",
                ],
                "fileName": "tickets_timeline.pdf",
                "title": "Ticket Timeline Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    # tickets status for each channel(aggregate by channel)
    @extend_schema(
        operation_id="complaint_source_ticket_status",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the different status of the tickets under each channel ",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_source_ticket_status")
    def source_ticket_status(self, request, *args, **kwargs):
        response, _, _ = source_ticket_status_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_source_ticket_status_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the different status of the tickets under each channel in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_source_ticket_status_export_csv",
    )
    def source_ticket_status_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = source_ticket_status_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_source_ticket_status_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="The table displays the different status of the tickets under each channel in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_source_ticket_status_export_pdf",
    )
    def source_ticket_status_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = source_ticket_status_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            " Aggregate by Channel",
            request.user.username,
        )
        return items

    # -------------------------------------------------------------------------------------------------

    # Reports by user in the format of table
    @extend_schema(
        operation_id="complaint_ticket_user_priority",
        tags=[AuthTags.AUTHORIZE],
        description="Reports of the tickets for each user",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_ticket_user_priority")
    def ticket_user_priority(self, request, *args, **kwargs):
        response, _, _ = ticket_user_priority_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_ticket_user_priority_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Reports of the tickets for each user in csv ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_ticket_user_priority_export_csv",
    )
    def ticket_user_priority_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = ticket_user_priority_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_ticket_user_priority_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Reports of the tickets for each user in pdf ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_ticket_user_priority_export_pdf",
    )
    def ticket_user_priority_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = ticket_user_priority_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Priority by Assignee",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="complaint_username_status_tickets",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets under each status",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_username_status_tickets"
    )
    def username_status_tickets(self, request, *args, **kwargs):
        response, _, _ = username_status_tickets_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_username_status_tickets_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets under each status in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_username_status_tickets_export_csv",
    )
    def username_status_tickets_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = username_status_tickets_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_username_status_tickets_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets under each status in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_username_status_tickets_export_pdf",
    )
    def username_status_tickets_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = username_status_tickets_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Status by Assignee",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="complaint_username_resolved_monthly",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets resolved in each month",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_username_resolved_monthly"
    )
    def username_resolved_monthly(self, request, *args, **kwargs):
        response, _, _ = username_resolved_monthly_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_username_resolved_monthly_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets resolved in each month in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_username_resolved_monthly_export_csv",
    )
    def username_resolved_monthly_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = username_resolved_monthly_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_username_resolved_monthly_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the username and the no of tickets resolved in each month in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_username_resolved_monthly_export_pdf",
    )
    def username_resolved_monthly_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = username_resolved_monthly_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Tickets Resolved By Assignee",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="complaint_category_priority_tickets_bar",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category name and the priority of the tickets",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_priority_tickets_bar",
    )
    def category_priority_tickets_bar(self, request, *args, **kwargs):
        qs1 = category_priority_tickets_bar_generic(request)
        return Response(qs1)

    # --------------------------------------------------------------------------------------------------------------------
    @extend_schema(
        operation_id="complaint_category_status_tickets",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category and the status",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_category_status_tickets"
    )
    def category_status_tickets(self, request, *args, **kwargs):
        response, _, _ = category_status_tickets_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_category_status_tickets_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category and the status",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_status_tickets_export_csv",
    )
    def category_status_tickets_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = category_status_tickets_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_category_status_tickets_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category and the status",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_status_tickets_export_pdf",
    )
    def category_status_tickets_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = username_resolved_monthly_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Status by Category",
            request.user.username,
        )
        return items

    # ----------------------------------------------------------------------------------------------------
    # tickets resolved in the month by catgeory
    @extend_schema(
        operation_id="complaint_category_resolved_tickets_monthly",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category the count of tickets opened monthly",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_resolved_tickets_monthly",
    )
    def category_resolved_tickets_monthly(self, request, *args, **kwargs):
        response, _, _ = category_resolved_tickets_monthly_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_category_resolved_tickets_monthly_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category the count of tickets opened monthly in csv ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_resolved_tickets_monthly_export_csv",
    )
    def category_resolved_tickets_monthly_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = category_resolved_tickets_monthly_generic(
            request
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_category_resolved_tickets_monthly_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the category the count of tickets opened monthly in pdf ",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_category_resolved_tickets_monthly_export_pdf",
    )
    def category_resolved_tickets_monthly_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = category_resolved_tickets_monthly_generic(
            request
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Resolved by Category",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="complaint_ticket_total_time_spent",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details of the closed tickets",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_ticket_total_time_spent"
    )
    def ticket_total_time_spent(self, request, *args, **kwargs):
        response, _, _ = ticket_total_time_spent_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_ticket_total_time_spent_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details f the resolved tickets",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_ticket_total_time_spent_export_csv",
    )
    def ticket_total_time_spent_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = ticket_total_time_spent_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_ticket_total_time_spent_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details f the resolved tickets",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_ticket_total_time_spent_export_pdf",
    )
    def ticket_total_time_spent_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = ticket_total_time_spent_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Closed Tickets",
            request.user.username,
        )
        return items

    # # all resolved tickets montly
    # @extend_schema(
    #     operation_id="resolved_tickets_monthly_graph",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="Displays a line chart of the resolved tickets in each month",
    # )
    # @action(methods=["POST"], detail=False, url_path="resolved_tickets_monthly_graph")
    # def resolved_tickets_monthly_graph(self, request, *args, **kwargs):
    #     response = resolved_tickets_monthly_graph_generic(request)
    #     return Response(response)

    @extend_schema(
        operation_id="complaint_open_closed_monthly_tickets",
        tags=[AuthTags.AUTHORIZE],
        description="Displays a line chart of the open and closed tickets in each month",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_open_closed_monthly_tickets"
    )
    def open_closed_monthly_tickets(self, request, *args, **kwargs):
        response = open_closed_monthly_tickets_generic(request)
        return Response(response)

    # @extend_schema(
    #     operation_id="tickets_assignee_escalation",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="The tickets that are ignored by the agents and now are under escalation",
    # )
    # @action(methods=["POST"], detail=False, url_path="tickets_assignee_escalation")
    # def tickets_assignee_escalation(self, request, *args, **kwargs):
    #     response = tickets_assignee_escalation_generic(request)
    #     return return_table(response, request)

    # @extend_schema(
    #     operation_id="tickets_floating_escalation",
    #     tags=[AuthTags.AUTHORIZE],
    #     description="The tickets that are unassigned to the agents and now are under escalation",
    # )
    # @action(methods=["POST"], detail=False, url_path="tickets_floating_escalation")
    # def tickets_floating_escalation(self, request, *args, **kwargs):
    #     params = tickets_floating_escalation_generic(request)
    #     return get_generic_response(params)

    # pie chart for category
    @extend_schema(
        operation_id="complaint_tickets_category_piechart",
        tags=[AuthTags.AUTHORIZE],
        description="The pie chart illustrates the different categories under which the tickets were being raised",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_tickets_category_piechart"
    )
    def tickets_category_piechart(self, request, *args, **kwargs):
        qs1 = tickets_category_piechart_generic(request)
        return Response(qs1)

    # pie chart for priority
    @extend_schema(
        operation_id="complaint_tickets_priority_piechart",
        tags=[AuthTags.AUTHORIZE],
        description="The pie chart illustrates the different priority under which the tickets were being raised",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_tickets_priority_piechart"
    )
    def tickets_priority_piechart(self, request, *args, **kwargs):
        qs1 = tickets_priority_piechart_generic(request)
        return Response(qs1)

    # Pie chart to show count of within SLA, escalation1 and escalation 2
    @extend_schema(
        operation_id="complaint_sla_breached_unbreached",
        tags=[AuthTags.AUTHORIZE],
        description="The pie chart illustrates the count of within sla,escalation1,escalation2 tickets",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_sla_breached_unbreached"
    )
    def sla_breached_unbreached(self, request, *args, **kwargs):
        qs1 = sla_breached_unbreached_generic(request)
        return Response(qs1)

    # Tickets details about all the resolved tickets within SLA(Service level Agreement)
    @extend_schema(
        operation_id="complaint_resolved_tickets_details",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details for the resolved tickets",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_resolved_tickets_details"
    )
    def resolved_tickets_details(self, request, *args, **kwargs):
        response, _, _ = resolved_tickets_details_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_resolved_tickets_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details for the resolved tickets",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_resolved_tickets_details_export_csv",
    )
    def resolved_tickets_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = resolved_tickets_details_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_resolved_tickets_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Displays the details for the resolved tickets",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_resolved_tickets_details_export_pdf",
    )
    def resolved_tickets_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = resolved_tickets_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Resolved Within SLA",
            request.user.username,
        )
        return items

    # -----------------------------------------------------------------------------------------------------------------
    # ticket details for escalation1
    @extend_schema(
        operation_id="complaint_tickets_escalation_one_details",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation1 details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_one_details",
    )
    def tickets_escalation_one_details(self, request, *args, **kwargs):
        response, _, _ = tickets_escalation_details_generic(request, "ESCALATION1")
        return return_table(response, request)

    # csv for escalation1
    @extend_schema(
        operation_id="complaint_tickets_escalation_one_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation1 details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_one_export_csv",
    )
    def tickets_escalation_one_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = tickets_escalation_details_generic(
            request, "ESCALATION1"
        )
        items = export_csv(
            response,
            field_names,
            "escalation1_details.csv",
        )
        return items

    # pdf for escalation 1 details
    @extend_schema(
        operation_id="complaint_tickets_escalation_one_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation1 details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_one_export_pdf",
    )
    def tickets_escalation_one_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = tickets_escalation_details_generic(
            request, "ESCALATION1"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "escalation1_details.pdf",
            "Escalation 1 Details",
            request.user.username,
        )
        return items

    # ------------------ESCALATION 2 DETAILS----------------------------------------------------------------
    @extend_schema(
        operation_id="complaint_tickets_escalation_two_details",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation2 details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_two_details",
    )
    def tickets_escalation_two_details(self, request, *args, **kwargs):
        response, _, _ = tickets_escalation_details_generic(request, "ESCALATION2")
        return return_table(response, request)

    # csv for escalation1
    @extend_schema(
        operation_id="complaint_tickets_escalation_two_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation2 details",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_two_export_csv",
    )
    def tickets_escalation_two_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = tickets_escalation_details_generic(
            request, "ESCALATION2"
        )
        items = export_csv(
            response,
            field_names,
            "escalation2_details.csv",
        )
        return items

    # pdf for escalation 1 details
    @extend_schema(
        operation_id="complaint_tickets_escalation_two_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets under escalation2 details in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_tickets_escalation_two_export_pdf",
    )
    def tickets_escalation_two_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = tickets_escalation_details_generic(
            request, "ESCALATION2"
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            "escalation2_details.pdf",
            "Escalation 2 Details",
            request.user.username,
        )
        return items

    # details of tickets that were resolved after sla
    @extend_schema(
        operation_id="complaint_resolved_after_sla_breach",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets that were resolved after the SLA was breached",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_resolved_after_sla_breach"
    )
    def resolved_after_sla_breach(self, request, *args, **kwargs):
        response, _, _ = resolved_after_sla_breach_generic(request, False)
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_resolved_after_sla_breach_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets that were resolved after the SLA was breached in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_resolved_after_sla_breach_export_csv",
    )
    def resolved_after_sla_breach_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = resolved_after_sla_breach_generic(
            request, False
        )
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="complaint_resolved_after_sla_breach_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Tickets that were resolved after the SLA was breached in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_resolved_after_sla_breach_export_pdf",
    )
    def resolved_after_sla_breach_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = resolved_after_sla_breach_generic(
            request, False
        )
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Resolved after SLA breach",
            request.user.username,
        )
        return items

    # assignee online and offline details
    @extend_schema(
        operation_id="complaint_assignee_status",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the details of the assignee's status and the latest timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_assignee_status")
    def assignee_status(self, request, *args, **kwargs):
        response, _, _ = assignee_status()
        return return_table(response, request)

    @extend_schema(
        operation_id="complaint_assignee_status_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the details of the assignee's status and the latest timestamp",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_assignee_status_export_csv"
    )
    def assignee_status_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = assignee_status()
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="complaint_assignee_status_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Shows the details of the assignee's status and the latest timestamp",
    )
    @action(
        methods=["POST"], detail=False, url_path="complaint_assignee_status_export_pdf"
    )
    def assignee_status_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = assignee_status()
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Assignee Status",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="complaint_email_tickets_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying details of API response details",
    )
    @action(methods=["POST"], detail=False, url_path="complaint_email_tickets_details")
    def complaints_email_tickets_details(self, request, *args, **kwargs):
        params = email_tickets_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="complaint_email_tickets_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API response in csv format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_email_tickets_details_export_csv",
    )
    def email_tickets_details_export_csv(self, request, *args, **kwargs):
        params = email_tickets_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "SRN",
                    "Email_from",
                    "Email_to",
                    "CC_User",
                    "Source",
                    "Agent_Name",
                    "Type",
                    "Status",
                    "Message_Id",
                    "Timestamp",
                ],
                "fileName": "email_tickets_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="complaint_email_tickets_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for downloading details of API response in pdf format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="complaint_email_tickets_details_export_pdf",
    )
    def email_tickets_details_export_pdf(self, request, *args, **kwargs):
        params = email_tickets_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "SRN",
                    "Email_from",
                    "Email_to",
                    "CC_User",
                    "Source",
                    "Agent_Name",
                    "Type",
                    "Status",
                    "Message_Id",
                    "Timestamp",
                ],
                "fileName": "email_tickets_details.pdf",
                "title": "Email Ticket Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
