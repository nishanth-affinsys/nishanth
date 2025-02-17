from datetime import timedelta
from django.db.models import (
    Q,
    F,
    Count,
    Case,
    When,
    Sum,
    CharField,
    Value,
    Max,
    FloatField,
    TextField,
)

from django.db.models.functions import Cast, Trunc, TruncDate
from django.utils import timezone

from handoff.models import (
    AnalyticsSocialevent,
    SocialconversationAgenttenant,
    SocialconversationTempsocialuser,
    AgentLastActivityTime,
    AgentSkill,
    CurrentLoggedIn,
    AbandonedDetails,
    Handoffduration,
)
from console.models import MessageLog
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.common_utils import convert_seconds_to_hhmmss
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from main.utils.common_utils import custom_filters


def online_agents_generic():
    qs = (
        SocialconversationAgenttenant.objects.using("handoff")
        .filter(agent__is_online=True)
        .filter(tenant__tenant_name=get_current_tenant_name())
        .values()
        .count()
    )
    return qs


def message_agent_and_user_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(Q(event="chat-message") | Q(event="social-message"))
        .values()
        .count()
    )
    return qs


def chats_in_queue_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(event="handoff-initial", social__is_circulating=True)
        .values()
        .count()
    )
    return qs


def chats_in_queue_detail_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(event="handoff-initial", social__is_circulating=True)
        .values("event", "social__username")
        .annotate(
            Username=F("social__username"),
            Timestamp=Max(
                Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
            ),
        )
        .values("Username", "Timestamp")
        .order_by("-Timestamp")
    )
    return qs


def handoff_called_today_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(event="handoff-initial")
        .all()
        .count()
    )
    return qs


def online_detail_generic():
    qs = (
        SocialconversationAgenttenant.objects.using("handoff")
        .filter(tenant__tenant_name=get_current_tenant_name())
        .filter(agent__is_online=True)
        .values("agent__username", "agent__is_online")
        .annotate(
            Username=F("agent__username"),
            Is_Online=Case(
                When(Q(agent__is_ready=True), then=Value("Yes")),
                When(Q(agent__is_ready=False), then=Value("No")),
                output_field=CharField(),
            ),
        )
        .values("Username", "Is_Online")
    )
    return qs


def online_customers_agent_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    now = timezone.now() - timedelta(minutes=1)
    qs = (
        SocialconversationTempsocialuser.objects.using("handoff")
        .filter(**filters)
        .filter(last_activity__gte=now)
        .values("channel_id")
        .count()
    )
    return qs


def online_customers_bot_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    now = timezone.now() - timedelta(minutes=1)
    dynamic_db_connection("analytics")
    qs = (
        MessageLog.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(timestamp__gte=now, tenant=get_current_tenant_name())
        .filter(source="user")
        .values("channel_id")
        .distinct()
        .count()
    )
    return qs


def handoff_duration_generic():
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    qs = (
        Handoffduration.objects.using("handoff")
        .filter(tenant=get_current_tenant_name())
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .values("username")
        .annotate(Duration=Sum("minutes"))
    )
    response = []
    for i in qs:
        duration_minutes = i.get("Duration")
        duration_formatted = convert_seconds_to_hhmmss(duration_minutes * 60)
        data = {"username": i.get("username"), "Duration": duration_formatted}
        response.append(data)
    return response


def agent_last_activity_time_generic():
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    qs = (
        AgentLastActivityTime.objects.using("handoff")
        .filter(tenant=get_current_tenant_name())
        .filter(diff__gte=today, diff__lte=tomorrow)
        .annotate(
            Username=F("username"),
            Timestamp=Trunc(F("diff"), "second", tzinfo=get_timezone()),
        )
        .values("Username", "Timestamp")
    )
    return qs


def ended_chats_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AnalyticsSocialevent.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(
            Q(event="agent-end-confirm")
            | Q(event="user-end-confirm")
            | Q(event="agent-force-end")
            | Q(event="user-inactive")
        )
        .annotate(label=F("event"))
        .values("label")
        .annotate(count=Count("event"))
        .order_by("-count")
    )
    return qs


def agent_skill_generic():
    qs = (
        AgentSkill.objects.using("handoff")
        .filter(tenant=get_current_tenant_name())
        .values("username")
        .distinct()
    )
    response = []
    for i in qs:
        qs1 = (
            AgentSkill.objects.using("handoff")
            .filter(tenant=get_current_tenant_name(), username=i.get("username"))
            .values_list("skill_name", flat=True)
        )
        data = {
            "User Name": i.get("username"),
            "Skills": qs1,
            "Number of Skills": qs1.count(),
        }
        response.append(data)
    return response


def ongoing_max_chats_generic():
    qs = (
        SocialconversationAgenttenant.objects.using("handoff")
        .filter(tenant__tenant_name=get_current_tenant_name())
        .values("agent__username", "agent__max_concurrent", "agent__current_chats")
        .annotate(
            username=F("agent__username"),
            max_concurrent=F("agent__max_concurrent"),
            current_chats=F("agent__current_chats"),
        )
        .values("username", "max_concurrent", "current_chats")
    )
    return qs


def current_loggedin_skills_generic():
    qs = (
        CurrentLoggedIn.objects.using("handoff")
        .filter(tenant=get_current_tenant_name())
        .filter(is_online=True)
        .values("skill_name")
        .annotate(count=Count("skill_name"))
    )
    return qs


def abandoned_users_details_live_generic(request):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    qs = (
        AbandonedDetails.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .filter(Q(event="user-fallout") | Q(event="user-cancel-routing"))
        .exclude(session__isnull=True)
        .values(
            Customer_name=F("username"),
            Phone_Number=F("phone_number"),
            Email=F("email"),
            Channel=F("channel"),
            Session=F("session"),
        )
        .annotate(Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()))
        .order_by("-timestamp")
    )
    return qs


def interaction_live_generic(request, event_type):
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
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
            .filter(timestamp__gte=today, timestamp__lte=tomorrow)
            .filter(event=event_type, agent_id=user["id"])
            .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
            .annotate(count=Count("session", distinct=True))
        )
        res[user["username"]] = qs1
    response = []
    for user, item in res.items():  # user = Agent Name, item is the qs1 object
        for data in item:
            value = {
                "Agent": user,
                "Date": data["Date"],
                "Interactions": data["count"],
            }
            response.append(value)
    return response


def conversations_live_generic(request):
    dynamic_db_connection("analytics")
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    result = (
        MessageLog.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(tenant=get_current_tenant_name(), source="user")
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .values(
            Customer_id=F("channel_id"),
            Channel=F("channel"),
            Message=F("message"),
            Source=F("source"),
            Handled=F("handled"),
            Intent=F("intent"),
            Score=Cast(F("score"), output_field=FloatField()),
        )
        .annotate(
            timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("timestamp")
    )
    return result


def top_messages_live_generic(request):
    dynamic_db_connection("analytics")
    today = timezone.now() - timedelta(minutes=3)
    tomorrow = timezone.now()
    filter_data = request.data
    filters = custom_filters(filter_data, None, "channel__in", None)
    result = (
        MessageLog.objects.using(get_db_name("analytics"))
        .filter(**filters)
        .filter(tenant=get_current_tenant_name(), source="user")
        .filter(timestamp__gte=today, timestamp__lte=tomorrow)
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("Message"))
        .order_by("-count")[:5]
    )
    return result
