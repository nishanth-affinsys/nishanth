import json

from django.db.models import (
    F,
)
from django.db.models.functions import Cast, Trunc

from main.tenant_middleware import get_current_tenant_name, get_timezone
from handoff.models import (
    SocialconversationAgenttenant,
    AuditlogLogentry,
    AgentProductivity,
)
from main.utils.common_utils import custom_filters


def agent_routing_generic(request):
    filter_data = request.data
    filters = custom_filters(filter_data, "initial_time__range", "channel__in", None)
    values = {
        "accepted_time": F("accept_time"),
        "initialized_time": Trunc(F("initial_time"), "second", tzinfo=get_timezone()),
    }
    qs = (
        AgentProductivity.objects.using("handoff")
        .filter(**filters)
        .filter(tenant=get_current_tenant_name())
        .values(
            "username",
            "agent_routed",
            "session_id",
            "channel",
            "agent_accept",
            **values
        )
        .order_by("-initialized_time")
    )
    return (
        qs,
        [
            "username",
            "agent_routed",
            "session_id",
            "channel",
            "agent_accept",
            "accepted_time",
            "initialized_time",
        ],
        "agent_routing",
    )


def agent_login_status_generic(request):
    filter_data = request.data
    qs = (
        AuditlogLogentry.objects.using("handoff")
        .filter(timestamp__range=filter_data.get("timestamp__range"))
        .filter(changes__icontains="is_online")
        .using("handoff")
        .annotate(Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()))
        .values("object_id", "object_repr", "changes", "Timestamp")
        .order_by("-Timestamp")
    )
    response = []
    for i in qs:
        if (
            SocialconversationAgenttenant.objects.using("handoff")
            .filter(
                agent_id=i.get("object_id"),
                tenant__tenant_name=get_current_tenant_name(),
            )
            .exists()
        ):
            state = json.loads(i.get("changes"))
            data = {
                "Agent_Name": (
                    i.get("object_repr")
                    if i.get("object_repr") == " "
                    else SocialconversationAgenttenant.objects.using("handoff")
                    .filter(
                        agent_id=i.get("object_id"),
                        tenant__tenant_name=get_current_tenant_name(),
                    )
                    .values("agent__username")
                    .first()
                    .get("agent__username")
                ),
                "Status": (
                    "Logged in" if state.get("is_online")[1] == "True" else "Logged out"
                ),
                "Timestamp": i.get("Timestamp"),
            }
            response.append(data)
    return response, ["Agent_Name", "Status", "Timestamp"], "agent_login_status"


def agent_availability_generic(request):
    filter_data = request.data
    qs = (
        AuditlogLogentry.objects.using("handoff")
        .filter(timestamp__range=filter_data.get("timestamp__range"))
        .filter(changes__icontains="is_ready")
        .using("handoff")
        .annotate(Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()))
        .values("object_id", "object_repr", "changes", "Timestamp")
        .order_by("-Timestamp")
    )
    response = []
    for i in qs:
        if (
            SocialconversationAgenttenant.objects.using("handoff")
            .filter(
                agent_id=i.get("object_id"),
                tenant__tenant_name=get_current_tenant_name(),
            )
            .exists()
        ):
            state = json.loads(i.get("changes"))
            data = {
                "Agent_name": (
                    i.get("object_repr")
                    if i.get("object_repr") == " "
                    else SocialconversationAgenttenant.objects.using("handoff")
                    .filter(
                        agent_id=i.get("object_id"),
                        tenant__tenant_name=get_current_tenant_name(),
                    )
                    .values("agent__username")
                    .first()
                    .get("agent__username")
                ),
                "Status": "Online" if state.get("is_ready")[1] == "True" else "Offline",
                "Timestamp": i.get("Timestamp"),
            }
            response.append(data)
    return (
        response,
        ["Agent_name", "Status", "Timestamp"],
        "agent_availability_status",
    )
