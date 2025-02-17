from __future__ import annotations

from django.db.models import Count, F, TextField
from django.db.models.functions import Cast, Trunc

from console.models import MessageLogDetails, ChannelsReactions
from console.serializers import MessageLogSessionsSerializer, ChannelReactionSerializer
from console.services.api_logs_utils import add_args
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import get_generic_response, query
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def top_10_message_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user", message__isnull=False)
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("Message"))
        .order_by("-count")[:10]
    )
    return items, ["Message", "count"], "top_ten_messages"


def top_10_intents_generic(request):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": MessageLogDetails,
        "serializers": MessageLogSessionsSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "source": "user",
            "message__isnull": False,
        },
        "values": ["intent"],
        "annotate": {"count": Count("intent")},
        "order_by": ["-count"],
        "query_set": True,
    }
    items = get_generic_response(params)
    if len(items) > 10:
        items = items[:10]
    return items, ["intent", "count"], "top_10_intents"


def message_wordcloud_generic(request):
    dynamic_db_connection("analytics")
    qs = query(
        request, MessageLogDetails, MessageLogSessionsSerializer, db_schema=get_db_name("analytics")
    )
    items = (
        qs.filter(source="user", message__isnull=False)
        .annotate(Message=Cast("message", output_field=TextField()))
        .values("Message")
        .annotate(count=Count("Message"))
        .order_by("-count")
    )
    items = [{"name": item["Message"], "count": item["count"]} for item in items]
    return items


def channels_reaction_generic(request, key=None, value=None):
    dynamic_db_connection("analytics")
    params = {
        "request": request,
        "models": ChannelsReactions,
        "serializers": ChannelReactionSerializer,
        "db_schema": get_db_name("analytics"),
        "filter_kwargs": {
            "remarks__isnull": False,
        },
        "values_kwargs": {
            "Username": F("user_name"),
            "User_Id": F("user_id"),
            "Page_Id": F("page_id"),
            "Post_Id": F("post_id"),
            "Action_Type": F("action_type"),
            "Remarks": F("remarks"),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)
