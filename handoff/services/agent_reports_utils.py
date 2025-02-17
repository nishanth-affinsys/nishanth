from django.db.models import (
    Count,
    Value,
    Q,
    Max,
    Min,
    Case,
    When,
    F,
    CharField,
)

from handoff.serializers import AgentReportSerializer
from django.db.models.functions import TruncDate

from handoff.models import (
    AnalyticsSocialevent,
    SocialconversationAgenttenant,
    HandoffFlow,
)

from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from main.utils.common_utils import convert_seconds_to_hhmmss
from main.utils.common_utils import custom_filters

# constant
entered_queue = "Entered in Queue"
notifications = "Notifications Arrived"
agent_ended = "Agent ended"
inactive_user = "Inactive User"
user_ended = "User ended"


def interaction_arrived_bar_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(event="handoff-notification")
        .values(Channel=F("channel"))
        .annotate(Count=Count("session", distinct=True))
        .order_by("-Count")
    )
    return qs


def interactions_arrived_or_accepted_generic(request, event_type):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs_agents = (
        SocialconversationAgenttenant.objects.using("handoff")
        .filter(tenant__tenant_name=get_current_tenant_name())
        .values("agent__username", "agent__id")
        .annotate(username=F("agent__username"), id=F("agent__id"))
        .values("username", "id")
    )
    res = {}
    for user in qs_agents:
        qs_events = (
            AnalyticsSocialevent.objects.using("handoff")
            .filter(**filters)
            .filter(tenant=get_current_tenant_name())
            .filter(event=event_type, agent_id=user["id"])
            .values(
                Channel=F("channel"),
                Timestamp=TruncDate("timestamp", tzinfo=get_timezone()),
            )
            .annotate(count=Count("session", distinct=True))
        )
        res[user["username"]] = qs_events

    response = [
        {
            "Agent Name": user,
            "Date": data["Timestamp"],
            "Channel": data["Channel"],
            "Interactions": data["count"],
        }
        for user, item in res.items()
        for data in item
    ]

    return (
        response,
        ["Agent Name", "Date", "Channel", "Interactions"],
        "interactions",
    )


def interaction_accepted_channelwise_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(tenant=get_current_tenant_name())
        .filter(**filters)
        .filter(event="agent-accept")
        .values(Channel=F("channel"))
        .annotate(Count=Count("session", distinct=True))
        .order_by("-Count")
    )
    return qs


def interaction_accepted_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        SocialconversationAgenttenant.objects.using("handoff")
        .filter(tenant__tenant_name=get_current_tenant_name())
        .values("agent__username", "agent__id")
        .annotate(username=F("agent__username"), id=F("agent__id"))
        .values("username", "id")
    )
    res = {}
    for user in qs:
        qs1 = (
            AnalyticsSocialevent.objects.using("handoff")
            .filter(**filters)
            .filter(tenant=get_current_tenant_name())
            .filter(event="agent-accept", agent_id=user["id"])
            .values(
                Channel=F("channel"),
                Timestamp=TruncDate("timestamp", tzinfo=get_timezone()),
            )
            .annotate(count=Count("session", distinct=True))
        )
        res[user["username"]] = qs1
    response = [
        {
            "Agent Name": user,
            "Date": data["Timestamp"],
            "Channel": data["Channel"],
            "Interactions Accepted": data["count"],
        }
        for user, item in res.items()
        for data in item
    ]
    return (
        response,
        ["Agent Name", "Date", "Channel", "Interactions Accepted"],
        "interactions_accepted",
    )


def agent_average_session_time_by_channel_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            tenant=get_current_tenant_name(),
            **filters,
        )
        .filter(
            event__in=[
                "agent-accept",
                "user-end-confirm",
                "agent-force-end",
                "agent-end-confirm",
                "user-inactive",
            ]
        )
        .values(
            "agent__username",
            "session",
            "channel",
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(duration=Max("timestamp") - Min("timestamp"))
        .values("agent__username", "channel", "Date", "duration")
        .order_by("-Date")
    )
    qs1 = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            tenant=get_current_tenant_name(),
            **filters,
        )
        .filter(event="agent-accept")
        .values(
            "agent__username",
            Channel=F("channel"),
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .distinct()
        .order_by("-Date")
    )
    response = []
    for i in qs1:
        duration = 0
        count = 0
        for j in qs:
            if (
                j.get("Date") == i.get("Date")
                and j.get("agent__username") == i.get("agent__username")
                and j.get("channel") == i.get("Channel")
            ):
                duration = duration + int(j.get("duration").total_seconds())
                count = count + 1
        formatted_duration = (
            convert_seconds_to_hhmmss(duration / count) if count > 0 else "00:00:00"
        )
        data = {
            "Agent Name": i.get("agent__username"),
            "Date": i.get("Date"),
            "Channel": i.get("Channel"),
            "Average Handling time": formatted_duration,
        }
        response.append(data)
    return (
        response,
        ["Agent Name", "Date", "Channel", "Average Handling time"],
        "average_handling_time",
    )


def entered_accepted_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    items = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            **filters,
        )
        .filter(tenant=get_current_tenant_name())
        .values("channel")
        .annotate(
            Entered_in_Queue=Count(
                "session", distinct=True, filter=Q(event="handoff-initial")
            ),
            Accepted_by_Agent=Count(
                "session", distinct=True, filter=Q(event="agent-accept")
            ),
            Unhandled_Chats=(
                Count("session", distinct=True, filter=(Q(event="agent-unavailable")))
                + Count("session", distinct=True, filter=Q(event="agent-out-of-office"))
                + Count(
                    "session",
                    distinct=True,
                    filter=Q(event="user-immediate-cancel"),
                )
            ),
            Abandoned_Chats=(
                Count("session", distinct=True, filter=Q(event="user-fallout"))
                + Count("session", distinct=True, filter=Q(event="user-cancel-routing"))
            ),
        )
    )
    return (
        items,
        [
            "channel",
            "Entered_in_Queue",
            "Accepted_by_Agent",
            "Unhandled_Chats",
            "Abandoned_Chats",
        ],
        "Aggregate_agents_report",
    )


def messages_in_each_interactions_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "timestamp__range", "channel__in", None)
    result = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(
            tenant=get_current_tenant_name(),
            **filters,
        )
        .filter(Q(event="social-message") | Q(event="chat-message"))
        .values(
            Agent_Name=F("agent__username"),
            Customer_Name=F("social__username"),
            Session=F("session"),
            Channel=F("channel"),
            Timestamp=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(Count=Count("event"))
    )

    return (
        result,
        ["Agent_Name", "Customer_Name", "Session", "Channel", "Timestamp", "Count"],
        "messages_interactions",
    )


def handoff_flow_shankey_chart_generic(request):
    qs = query(request, HandoffFlow, AgentReportSerializer, db_schema="handoff")
    values = (
        qs.filter(tenant=get_current_tenant_name())
        .values(
            Target=Case(
                When(target="handoff-initial", then=Value(entered_queue)),
                When(target="agent-unavailable", then=Value("Unhandled")),
                When(target="agent-out-of-office", then=Value("Unhandled")),
                When(target="user-immediate-cancel", then=Value("Unhandled")),
                When(
                    target="handoff-notification",
                    then=Value(notifications),
                ),
                When(target="user-fallout", then=Value("Abandoned")),
                When(target="user-cancel-routing", then=Value("Abandoned")),
                When(target="agent-accept", then=Value("Handled")),
                When(target="user-inactive", then=Value(inactive_user)),
                When(target="user-end-confirm", then=Value(user_ended)),
                When(target="agent-force-end", then=Value(agent_ended)),
                When(target="agent-end-confirm", then=Value(agent_ended)),
                output_field=CharField(),
            )
        )
        .filter(Target__isnull=False)
        .annotate(value=Count("Target"))
        .distinct()
        .values("Target", "value")
    )
    qs1 = (
        qs.filter(tenant=get_current_tenant_name())
        .filter(source__isnull=False)
        .values(
            Source=Case(
                When(source="handoff-initial", then=Value(entered_queue)),
                When(source="agent-unavailable", then=Value("Unhandled")),
                When(source="agent-out-of-office", then=Value("Unhandled")),
                When(source="user-immediate-cancel", then=Value("Unhandled")),
                When(
                    source="handoff-notification",
                    then=Value(notifications),
                ),
                When(source="user-fallout", then=Value("Abandoned")),
                When(source="user-cancel-routing", then=Value("Abandoned")),
                When(source="agent-accept", then=Value("Handled")),
                When(source="user-inactive", then=Value(inactive_user)),
                When(source="user-end-confirm", then=Value(user_ended)),
                When(source="agent-force-end", then=Value(agent_ended)),
                When(source="agent-end-confirm", then=Value(agent_ended)),
                output_field=CharField(),
            ),
            Target=Case(
                When(target="handoff-initial", then=Value(entered_queue)),
                When(target="agent-unavailable", then=Value("Unhandled")),
                When(target="agent-out-of-office", then=Value("Unhandled")),
                When(target="user-immediate-cancel", then=Value("Unhandled")),
                When(
                    target="handoff-notification",
                    then=Value(notifications),
                ),
                When(target="user-fallout", then=Value("Abandoned")),
                When(target="user-cancel-routing", then=Value("Abandoned")),
                When(target="agent-accept", then=Value("Handled")),
                When(target="user-inactive", then=Value(inactive_user)),
                When(target="user-end-confirm", then=Value(user_ended)),
                When(target="agent-force-end", then=Value(agent_ended)),
                When(target="agent-end-confirm", then=Value(agent_ended)),
                output_field=CharField(),
            ),
        )
        .filter(Source__isnull=False, Target__isnull=False)
        .exclude(Source=F("Source"), Target=F("Source"))
        .annotate(value=Count("target"))
        .values("Source", "Target", "value")
    )
    response = {"values": values, "links": qs1}
    return response
