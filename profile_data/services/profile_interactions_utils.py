from django.db.models import (
    Count,
    Case,
    Sum,
    When,
    Value,
    Func,
    CharField,
    F,
    IntegerField,
)
from django.db.models.functions import TruncDate

from profile_data.models import (
    Interaction,
    BotInteraction,
    HandoffInteraction,
    ComplaintInteraction,
)
from profile_data.serializers import (
    InteractionSerializer,
    BotInteractionSerializer,
    HandoffInteractionSerializer,
    ComplaintInteractionSerializer,
)

from main.utils.boiler_plate import query
from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.common_utils import add_args
from main.utils.date_range import get_date_ranges

from main.utils.dynamic_db import get_db_name, dynamic_db_connection


def user_interactions_by_service(request, key=None, value=None):
    dynamic_db_connection("profile")

    params = {
        "request": request,
        "models": Interaction,
        "serializers": InteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "Profile_Id": F("profile_id"),
            "Customer_Id": F("cust_id"),
            "Username": F("profile__user_name"),
            "Date": TruncDate("timestamp", tzinfo=get_timezone()),
        },
        "annotate": {
            # "Bot": Sum(Case(When(service_type="bot", then=1), default=0)),
            "Handoff": Sum(Case(When(service_type="handoff", then=1), default=0)),
            "Complaint": Sum(Case(When(service_type="complaint", then=1), default=0)),
        },
        "order_by": ["-Date"],
    }
    return add_args(params, key, value)


def interactions_by_service(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": Interaction,
        "serializers": InteractionSerializer,
        "db_schema": get_db_name("profile"),
        "exclude": {"service_type": "bot"},
        "values_kwargs": {"label": F("service_type")},
        "annotate": {"count": Count("profile_id")},
        "not_paginated": True,
    }
    return params


def profile_hourly_interactions_by_service(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": Interaction,
        "serializers": InteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "Date_and_Hour": Func(
                F("timestamp"),
                Value("YYYY-MM-DD HH24"),
                function="TO_CHAR",
                output_field=CharField(),
            )
        },
        "annotate": {
            # "Bot": Sum(Case(When(service_type="bot", then=1), default=0)),
            "Handoff": Sum(Case(When(service_type="handoff", then=1), default=0)),
            "Complaints": Sum(Case(When(service_type="complaint", then=1), default=0)),
        },
        "order_by": ["-Date_and_Hour"],
        "not_paginated": True,
    }
    return params


def profile_bot_interactions(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": BotInteraction,
        "serializers": BotInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {"label": F("channel_name")},
        "annotate": {"count": Count("profile_id", distinct=True)},
        "not_paginated": True,
    }
    return params


def profile_handoff_interactions(request, key=None, value=None):  # after handoff accept
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": HandoffInteraction,
        "serializers": HandoffInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "Profile_Id": F("profile_id"),
            "Agent_Name": F("agent_name"),
            "Customer_Id": F("channel_id"),
        },
        "annotate": {"Interactions": Count("interaction_id", distinct=True)},
        "order_by": ["-Interactions"],
    }
    return add_args(params, key, value)


def profile_complaint_category(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {"label": F("category")},
        "annotate": {"count": Count("profile_id", distinct=True)},
        "order_by": ["-count"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def profile_complaint_category_interactions_details(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "Profile_Id": F("profile_id"),
            "Username": F("user_name"),
            "Category": F("category"),
        },
        "annotate": {"Interactions": Count("interaction_id", distinct=True)},
        "order_by": ["-Interactions"],
    }
    return add_args(params, key, value)


def profile_complaint_channel_interactions(request, key=None, value=None):
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": "profile",
        "filter_kwargs": {
            "profile__tenant": get_current_tenant_name(),
        },
        "values_kwargs": {"label": F("channel_name")},
        "annotate": {"count": Count("interaction_id", distinct=True)},
        "order_by": ["-count"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def profile_complaints_remarks_wordcloud(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {"name": F("remarks")},
        "annotate": {"count": Count("name")},
        "order_by": ["-count"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def profile_complaints_channel_interactions(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {"channel": F("channel_name")},
        "annotate": {"Interactions": Count("interaction_id", distinct=True)},
        "order_by": ["-Interactions"],
        "not_paginated": True,
    }
    return add_args(params, key, value)


def interaction_daily_heatmap(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    date_range = get_date_ranges(
        filter_data.get("timestamp__range")[1],
        filter_data.get("timestamp__range")[0],
        4,
    )
    qs = query(request, Interaction, InteractionSerializer, get_db_name("profile"))
    qs1 = (
        qs.annotate(date=TruncDate("timestamp", tzinfo=get_timezone()))
        .values("date")
        .annotate(count=Count("date"))
        .values("date", "count")
        .order_by("-date")
    )
    response = {"date_range": date_range, "values": qs1}
    return response


def complaints_srn_category_interactions(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": ComplaintInteraction,
        "serializers": ComplaintInteractionSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "SRN": F("srn"),
            "Category": F("category"),
            "Channel": F("channel_name"),
        },
        "annotate": {"Interactions": Count("interaction_id", distinct=True)},
        "order_by": ["-Interactions"],
    }
    return add_args(params, key, value)


def top10_profiles_interactions(request):
    dynamic_db_connection("profile")
    qs = query(request, Interaction, InteractionSerializer, get_db_name("profile"))
    qs1 = (
        qs.values("profile_id")
        .annotate(  # Bot=Sum(Case(When(service_type="bot", then=1), default=0)),
            Handoff=Sum(Case(When(service_type="handoff", then=1), default=0)),
            Complaints=Sum(Case(When(service_type="complaint", then=1), default=0)),
            Total_Interactions=Sum(
                Case(
                    When(service_type__in=["bot", "handoff", "complaint"], then=1),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
        )
        .values("profile_id", "Handoff", "Complaints")
        .order_by("-Total_Interactions")[:10]
    )
    return qs1
