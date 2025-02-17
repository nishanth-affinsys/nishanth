from datetime import timedelta

import pytz
from django.db.models import (
    F,
    Func,
    Count,
    Value,
    CharField,
    DurationField,
    ExpressionWrapper,
    DateTimeField,
)
from django.db.models.functions import Cast, Trunc
from main.tenant_middleware import get_current_tenant_name, get_timezone
from clickstream.models import ClickstreamIpinformation, ClickstreamAction
from clickstream.serializers import (
    ClickStreamIpInformationSerializer,
    ClickStreamActionSerializer,
)
from main import settings
from main.utils.boiler_plate import (
    query,
)


def add_args(params, key, value):
    if key:
        params[key] = value
    return params


def user_location_piechart_generic(request, location):
    qs = query(
        request,
        ClickstreamIpinformation,
        ClickStreamIpInformationSerializer,
        db_schema="clickstream",
    )
    get_distinct_id = qs.distinct("record__session_id").values_list("id", flat=True)
    qs1 = (
        qs.values(location)
        .filter(id__in=list(get_distinct_id))
        .annotate(count=Count(location))
    )
    items = qs1.annotate(label=F(location)).values("count", "label")
    return items


def user_redirection_generic(request, key=None, value=None):
    params = {
        "request": request,
        "models": ClickstreamAction,
        "serializers": ClickStreamActionSerializer,
        "db_schema": "clickstream",
        "filter_kwargs": {"action_type": "navigate"},
        "values_kwargs": {
            "User_id": F("record__user_identifier__user_id"),
            "Session_id": F("record__session_id"),
            "Time_spent": Cast(
                Func(
                    (
                        timedelta(milliseconds=1)
                        * ExpressionWrapper(
                            F("time_spent_on_page"), output_field=DurationField()
                        )
                    ),
                    Value("HH24:MI:SS"),
                    function="TO_CHAR",
                ),
                output_field=CharField(),
            ),
            "Redirect_from": F("redirect_from"),
            "Redirect_to": F("redirect_to"),
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-time_spent_on_page"],
    }
    return add_args(params, key, value)
