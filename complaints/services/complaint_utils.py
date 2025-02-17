from datetime import timedelta
from django.db.models import (
    Count,
    Case,
    When,
    Value,
    Q,
    Max,
    Func,
    F,
    DateField,
    CharField,
    Window,
)
from django.db.models.functions import Cast, Trunc, RowNumber

from complaints.serializers import ComplaintTicketSerializer, ComplaintEmailSerializer
from console.models import (
    ComplaintTicketLogs,
    RecentTicketActivity,
    ComplaintsActivity,
    ComplaintEmailAudit,
)
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query, get_generic_response
from main.utils.dynamic_db import dynamic_db_connection, get_db_name

not_assigned = "Not assigned"


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def total_tickets_created_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ComplaintTicketLogs,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"status": "OPEN"},
        "distinct_args": ["srn"],
        "count": True,
        "query_set": True,
    }
    result = get_generic_response(params)
    return result


def assigned_tickets_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": RecentTicketActivity,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "exclude": {"status": "REOPENED"},
        "filter_kwargs": {
            "status__in": [
                "IN_PROGRESS",
                "HOLD",
                "RESOLVED",
                "ESCALATION1",
                "ESCALATION2",
            ],
            "user_name__isnull": False,
        },
        "distinct_args": ["srn"],
        "count": True,
        "query_set": True,
    }
    result = get_generic_response(params)
    return result


def unassigned_tickets_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    count = (
        qs.filter(status__in=["OPEN", "TRANSFER", "DUPLICATE", "CLOSED", "REOPENED"])
        .values("srn")
        .distinct()
        .count()
        + qs.filter(status__in=["ESCALATION1", "ESCALATION2"], user_name__isnull=True)
        .values("srn")
        .distinct()
        .count()
    )
    return count


def resolved_tickets_bigno_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": RecentTicketActivity,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "status": "RESOLVED",
        },
        "distinct_args": ["srn"],
        "count": True,
        "query_set": True,
    }
    result = get_generic_response(params)
    return result


def unresolved_tickets_bigno_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": RecentTicketActivity,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "exclude": {"status__in": ["RESOLVED", "CLOSED"]},
        "distinct_args": ["srn"],
        "count": True,
        "query_set": True,
    }
    result = get_generic_response(params)
    return result


def closed_tickets_bigno_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": RecentTicketActivity,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {"status": "CLOSED"},
        "distinct_args": ["srn"],
        "count": True,
        "query_set": True,
    }
    result = get_generic_response(params)
    return result


def ticket_timeline_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ComplaintTicketLogs,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "SRN": F("srn"),
            "Assignee_Name": Case(
                When(user_name__isnull=True, then=Value(not_assigned)),
                default=F("user_name"),
                output_field=CharField(),
            ),
            "Status": F("status"),
            "Priority": F("priority"),
        },
        "annotate": {
            "Created_Timestamp": Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_Updated_Timestamp": Trunc(
                F("last_updated_time"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-last_updated_time"],
    }
    return add_args(params, key, value)


def source_ticket_status_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs2 = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = qs.values(Channel=F("source")).annotate(
        Presently_Open=Count("srn", distinct=True, filter=Q(status="OPEN")),
        In_Progress=Count("srn", distinct=True, filter=Q(status="IN_PROGRESS")),
        Resolved=Count("srn", distinct=True, filter=Q(status="RESOLVED")),
        Escalation_1=Count("srn", distinct=True, filter=Q(status="ESCALATION1")),
        Escalation_2=Count("srn", distinct=True, filter=Q(status="ESCALATION2")),
        Closed=Count("srn", distinct=True, filter=Q(status="CLOSED")),
        Reopen=Count("srn", distinct=True, filter=Q(status="REOPENED")),
        Duplicate=Count("srn", distinct=True, filter=Q(status="DUPLICATE")),
        Hold=Count("srn", distinct=True, filter=Q(status="HOLD")),
        Transfer=Count("srn", distinct=True, filter=Q(status="TRANSFER")),
    )

    channel_names = qs2.values_list("source", flat=True).distinct()
    logs_qs = (
        qs2.filter(source__in=channel_names)
        .values("source")
        .annotate(Total_Tickets=Count("srn", distinct=True, filter=Q(status="OPEN")))
    )
    total_open_dict = {log["source"]: log["Total_Tickets"] for log in logs_qs}
    response = []
    for i in qs1:
        data = {
            "Channel": i.get("Channel"),
            "Total_Tickets": total_open_dict.get(i.get("Channel"), 0),
            "Presently_Open": i.get("Presently_Open"),
            "In_Progress": i.get("In_Progress"),
            "Resolved": i.get("Resolved"),
            "Escalation_1": i.get("Escalation_1"),
            "Escalation_2": i.get("Escalation_2"),
            "Closed": i.get("Closed"),
            "Reopen": i.get("Reopen"),
            "Duplicate": i.get("Duplicate"),
            "Hold": i.get("Hold"),
            "Transfer": i.get("Transfer"),
        }
        response.append(data)
    return (
        response,
        [
            "Channel",
            "Total_Tickets",
            "Presently_Open",
            "In_Progress",
            "Resolved",
            "Escalation_1",
            "Escalation_2",
            "Closed",
            "Reopen",
            "Duplicate",
            "Hold",
            "Transfer",
        ],
        "aggregate_by_channel",
    )


def ticket_user_priority_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.exclude(user_name__isnull=True)
        .values(
            Assignee_Name=Case(
                When(user_name__isnull=True, then=Value(not_assigned)),
                default=F("user_name"),
                output_field=CharField(),
            )
        )
        .annotate(
            High=Count("srn", distinct=True, filter=Q(priority="HIGH")),
            Medium=Count("srn", distinct=True, filter=Q(priority="MEDIUM")),
            Low=Count("srn", distinct=True, filter=Q(priority="LOW")),
        )
    )
    return qs1, ["Assignee_Name", "High", "Medium", "Low"], "priority_by_assignee"


def username_status_tickets_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.exclude(user_name__isnull=True)
        .values(
            Assignee_Name=Case(
                When(user_name__isnull=True, then=Value(not_assigned)),
                default=F("user_name"),
                output_field=CharField(),
            )
        )
        .annotate(
            In_Progress=Count("srn", distinct=True, filter=Q(status="IN_PROGRESS")),
            Resolved=Count("srn", distinct=True, filter=Q(status="RESOLVED")),
            Escalation_1=Count("srn", distinct=True, filter=Q(status="ESCALATION1")),
            Escalation_2=Count("srn", distinct=True, filter=Q(status="ESCALATION2")),
            Closed=Count("srn", distinct=True, filter=Q(status="CLOSED")),
            Reopen=Count("srn", distinct=True, filter=Q(status="REOPENED")),
            Duplicate=Count("srn", distinct=True, filter=Q(status="DUPLICATE")),
            Hold=Count("srn", distinct=True, filter=Q(status="HOLD")),
            Transfer=Count("srn", distinct=True, filter=Q(status="TRANSFER")),
        )
    )
    return (
        qs1,
        [
            "Assignee_Name",
            "Open",
            "In_Progress",
            "Resolved",
            "Escalation_1",
            "Escalation_2",
            "Closed",
            "Reopen",
            "Duplicate",
            "Hold",
            "Transfer",
        ],
        "Status_by_Assignee",
    )


def username_resolved_monthly_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.exclude(user_name__isnull=True)
        .values(
            Assignee_Name=Case(
                When(user_name__isnull=True, then=Value(not_assigned)),
                default=F("user_name"),
                output_field=CharField(),
            ),
            Created_Date=Trunc(F("created_timestamp"), "second", tzinfo=get_timezone()),
            Last_Updated=Trunc(F("last_updated_time"), "second", tzinfo=get_timezone()),
        )
        .annotate(count=Count("srn", distinct=True, filter=(Q(status="RESOLVED"))))
        .filter(count__gt=0)
        .order_by("Assignee_Name", "-Created_Date")
    )
    return (
        qs1,
        ["Assignee_Name", "Created_Date", "Last_Updated", "count"],
        "status_by_category",
    )


def category_priority_tickets_bar_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = qs.values("category_name").annotate(
        High=Count("srn", distinct=True, filter=Q(priority="HIGH")),
        Medium=Count("srn", distinct=True, filter=Q(priority="MEDIUM")),
        Low=Count("srn", distinct=True, filter=Q(priority="LOW")),
    )
    return qs1


def category_status_tickets_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs2 = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = qs.values("category_name").annotate(
        Presently_Open=Count("srn", distinct=True, filter=Q(status="OPEN")),
        In_Progress=Count("srn", distinct=True, filter=Q(status="IN_PROGRESS")),
        Resolved=Count("srn", distinct=True, filter=Q(status="RESOLVED")),
        Escalation_1=Count("srn", distinct=True, filter=Q(status="ESCALATION1")),
        Escalation_2=Count("srn", distinct=True, filter=Q(status="ESCALATION2")),
        Closed=Count("srn", distinct=True, filter=Q(status="CLOSED")),
        Reopen=Count("srn", distinct=True, filter=Q(status="REOPENED")),
        Duplicate=Count("srn", distinct=True, filter=Q(status="DUPLICATE")),
        Hold=Count("srn", distinct=True, filter=Q(status="HOLD")),
        Transfer=Count("srn", distinct=True, filter=Q(status="TRANSFER")),
    )
    category_names = qs2.values_list("category_name", flat=True).distinct()
    logs_qs = (
        qs2.filter(category_name__in=category_names)
        .values("category_name")
        .annotate(Total_Open=Count("srn", distinct=True, filter=Q(status="OPEN")))
    )
    total_open_dict = {log["category_name"]: log["Total_Open"] for log in logs_qs}
    response = []
    for i in qs1:
        data = {
            "Category_name": i.get("category_name"),
            "Total_Tickets": total_open_dict.get(i.get("category_name"), 0),
            "Presently_Open": i.get("Presently_Open"),
            "In_Progress": i.get("In_Progress"),
            "Resolved": i.get("Resolved"),
            "Escalation_1": i.get("Escalation_1"),
            "Escalation_2": i.get("Escalation_2"),
            "Closed": i.get("Closed"),
            "Reopen": i.get("Reopen"),
            "Duplicate": i.get("Duplicate"),
            "Hold": i.get("Hold"),
            "Transfer": i.get("Transfer"),
        }
        response.append(data)
    return (
        response,
        [
            "Category_name",
            "Total_Tickets",
            "Presently_Open",
            "In_Progress",
            "Resolved",
            "Escalation_1",
            "Escalation_2",
            "Closed",
            "Reopen",
            "Duplicate",
            "Hold",
            "Transfer",
        ],
        "Status_by_Category",
    )


def category_resolved_tickets_monthly_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.values(
            "category_name",
            Created_Date=Cast("created_timestamp", DateField()),
            Last_Updated=Cast("last_updated_time", DateField()),
        )
        .annotate(count=Count("srn", distinct=True, filter=(Q(status="RESOLVED"))))
        .filter(count__gt=0)
        .order_by("category_name", "-Created_Date")
    )
    return (
        qs1,
        ["category_name", "Created_Date", "Last_Updated", "count"],
        "resolved_by_category",
    )


def ticket_total_time_spent_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.filter(status="CLOSED")
        .values("srn")
        .annotate(max_last_updated_time=Max("last_updated_time"))
        .annotate(
            SRN=F("srn"),
            Assignee_Name=F("user_name"),
            Category=F("category_name"),
            Channel=F("source"),
            Priority=F("priority"),
            Created_Timestamp=Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            Last_Updated_Timestamp=Trunc(
                F("last_updated_time"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "SRN",
            "Assignee_Name",
            "Category",
            "Channel",
            "Priority",
            "Created_Timestamp",
            "Last_Updated_Timestamp",
        )
        .order_by("-Created_Timestamp")
    )
    return (
        qs1,
        [
            "SRN",
            "Assignee_Name",
            "Category",
            "Channel",
            "Priority",
            "Created_Timestamp",
            "Last_Updated_Timestamp",
        ],
        "closed_tickets",
    )


def resolved_tickets_monthly_graph_generic(request):
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.filter(tenant=get_current_tenant_name())
        .values(
            month=Cast(
                Func(
                    F("last_updated_time"),
                    Value("YYYY-Mon"),
                    function="TO_CHAR",
                ),
                output_field=CharField(),
            )
        )
        .annotate(
            Resolved_tickets=Count("srn", distinct=True, filter=(Q(status="RESOLVED")))
        )
        .order_by("-month")
    )
    return qs1


def open_closed_monthly_tickets_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.values(Date=Cast("created_timestamp", DateField()))
        .annotate(
            Open_Tickets=Count("srn", distinct=True, filter=Q(status="OPEN")),
            Closed_Tickets=Count("srn", distinct=True, filter=Q(status="CLOSED")),
            Resolved_Tickets=Count("srn", distinct=True, filter=Q(status="RESOLVED")),
        )
        .order_by("-Date")
    )
    return qs1


def tickets_assignee_escalation_generic(request):
    qs = query(
        request,
        ComplaintTicketLogs,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.filter(tenant=get_current_tenant_name())
        .filter(Q(status="ESCALATION1") | Q(status="ESCALATION2"))
        .exclude(user_name__isnull=True)
        .values(
            SRN=F("srn"),
            Assignee_Name=F("user_name"),
            Priority=F("priority"),
            Category_Name=F("category_name"),
            Created_Timestamp=Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            Last_Updated=Trunc(F("last_updated_time"), "second", tzinfo=get_timezone()),
            Status=F("status"),
        )
    )
    return qs1


def tickets_floating_escalation_generic(request):  # tickets that have no assignee
    params = {
        "request": request,
        "models": ComplaintTicketLogs,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_args": [Q(status="ESCALATION1") | Q(status="ESCALATION2")],
        "filter_kwargs": {
            "tenant": get_current_tenant_name(),
            "user_name__isnull": True,
        },
        "values": ["srn", "priority", "category_name", "status"],
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            "Last_Updated_Timestamp": Trunc(
                F("timestamp"), "second", tzinfo=get_timezone()
            ),
        },
        "order_by": ["-Timestamp"],
    }
    return params


def tickets_category_piechart_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.annotate(label=F("category_name"))
        .values("label")
        .annotate(count=Count("label"))
        .order_by("-count")
    )
    return qs1


def tickets_priority_piechart_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.annotate(label=F("priority"))
        .values("label")
        .annotate(count=Count("label"))
        .order_by("-count")
    )
    return qs1


def sla_breached_unbreached_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.annotate(
            label=Case(
                When(
                    status="RESOLVED",
                    breached_status__isnull=True,
                    then=Value("Resolved within SLA"),
                ),
                When(breached_status="ESCALATION1", then=Value("ESCALATION 1")),
                When(breached_status="ESCALATION2", then=Value("ESCALATION 2")),
            )
        )
        .exclude(label=None)
        .values("label")
        .annotate(count=Count("srn", distinct=True))
        .order_by("-count")
    )

    return qs1


def resolved_tickets_details_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.filter(status="RESOLVED", breached_status__isnull=True)
        .annotate(
            SRN=F("srn"),
            Assignee_Name=F("user_name"),
            Category=F("category_name"),
            Created_Timestamp=Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            Last_Updated_Timestamp=Trunc(
                F("last_updated_time"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "SRN",
            "Assignee_Name",
            "Category",
            "Created_Timestamp",
            "hold_time",
            "last_updated_time",
            "Last_Updated_Timestamp",
            "created_timestamp",
            "source",
            "priority",
        )
    )
    result = []
    for rows in qs1:
        time_difference = rows.get("last_updated_time") - rows.get("created_timestamp")
        hold_time = timedelta(seconds=rows.get("hold_time"))
        resolved_time = time_difference - hold_time
        time_seconds = round(resolved_time.total_seconds())
        time_timedelta = timedelta(seconds=time_seconds)
        time_string = str(time_timedelta)
        entries = {
            "SRN": rows.get("SRN"),
            "Assignee_Name": rows.get("Assignee_Name"),
            "Priority": rows.get("priority"),
            "Category": rows.get("Category"),
            "Channel": rows.get("source"),
            "Created_Timestamp": rows.get("Created_Timestamp"),
            "Resolved_Time": time_string,
            "Last_Updated_Timestamp": rows.get("Last_Updated_Timestamp"),
        }
        result.append(entries)
    return (
        result,
        [
            "SRN",
            "Assignee_Name",
            "Priority",
            "Category",
            "Channel",
            "Created_Timestamp",
            "Resolved_Time",
            "Last_Updated_Timestamp",
        ],
        "resolved_within_sla",
    )


def tickets_escalation_details_generic(request, escalation):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": RecentTicketActivity,
        "serializers": ComplaintTicketSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_args": [Q(breached_status=escalation)],
        "values_kwargs": {
            "SRN": F("srn"),
            "Assignee_Name": Case(
                When(user_name__isnull=True, then=Value(not_assigned)),
                default=F("user_name"),
                output_field=CharField(),
            ),
            "Priority": F("priority"),
            "Category": F("category_name"),
            "Channel": F("source"),
        },
        "annotate": {
            "Created_Timestamp": Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            "Last_Updated_Timestamp": Trunc(
                F("last_updated_time"), "second", tzinfo=get_timezone()
            ),
        },
        "query_set": True,
        "order_by": ["-Created_Timestamp"],
    }
    qs = get_generic_response(params)
    qs = sorted(list(qs), key=lambda x: x["Created_Timestamp"], reverse=True)
    return (
        qs,
        [
            "SRN",
            "Assignee_Name",
            "Priority",
            "Category",
            "Channel",
            "Created_Timestamp",
            "Last_Updated_Timestamp",
        ],
        "Escalation_details",
    )


def resolved_after_sla_breach_generic(request, breached_status):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        RecentTicketActivity,
        ComplaintTicketSerializer,
        db_schema=get_db_name("analytics"),
    )
    qs1 = (
        qs.filter(status="RESOLVED", breached_status__isnull=breached_status)
        .filter(Q(breached_status="ESCALATION1") | Q(breached_status="ESCALATION2"))
        .annotate(
            SRN=F("srn"),
            Assignee_Name=F("user_name"),
            Category=F("category_name"),
            Created_Timestamp=Trunc(
                F("created_timestamp"), "second", tzinfo=get_timezone()
            ),
            Last_Updated_Timestamp=Trunc(
                F("last_updated_time"), "second", tzinfo=get_timezone()
            ),
        )
        .values(
            "SRN",
            "Assignee_Name",
            "Category",
            "Created_Timestamp",
            "hold_time",
            "last_updated_time",
            "Last_Updated_Timestamp",
            "created_timestamp",
            "source",
            "priority",
        )
    )
    result = []
    result = [
        {
            "SRN": rows.get("SRN"),
            "Assignee_Name": rows.get("Assignee_Name"),
            "Priority": rows.get("priority"),
            "Category": rows.get("Category"),
            "Channel": rows.get("source"),
            "Created_Timestamp": rows.get("Created_Timestamp"),
            "Resolved_Time": str(
                timedelta(
                    seconds=round(
                        (
                            rows.get("last_updated_time")
                            - rows.get("created_timestamp")
                        ).total_seconds()
                        - rows.get("hold_time")
                    )
                )
            ),
            "Last_Updated_Timestamp": rows.get("Last_Updated_Timestamp"),
        }
        for rows in qs1
    ]
    return (
        result,
        [
            "SRN",
            "Assignee_Name",
            "Priority",
            "Category",
            "Channel",
            "Created_Timestamp",
            "Resolved_Time",
            "Last_Updated_Timestamp",
        ],
        "Resolved_after_breach",
    )


def assignee_status():
    dynamic_db_connection("analytics")
    qs = (
        ComplaintsActivity.objects.using(get_db_name("analytics"))
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=["user_name"],
                order_by=["-timestamp"],
            )
        )
        .filter(row_number=1)
        .values()
    )
    qs1 = qs.values(
        Assignee=F("user_name"),
        Status=Case(
            When(is_active=True, then=Value("Online")),
            When(is_active=False, then=Value("Offline")),
            output_field=CharField(),
        ),
        Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
    )
    return qs1, ["Assignee", "Status", "Timestamp"], "assignee_status"


def email_tickets_details(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ComplaintEmailAudit,
        "serializers": ComplaintEmailSerializer,
        "db_schema": get_db_name("analytics"),
        "values_kwargs": {
            "SRN": F("srn"),
            "Email_from": F("email_from"),
            "Email_to": F("email_to"),
            "CC_User": F("cc_user"),
            "Source": F("source"),
            "Agent_Name": F("agent_name"),
            "Type": F("type"),
            "Status": F("status"),
            "Message_Id": F("message_id"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone())
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)
