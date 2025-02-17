from django.db.models import (
    Count,
    Case,
    When,
    Value,
    CharField,
    F,
)
from django.db.models.functions import Trunc

from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from profile_data.models import (
    Profile,
    Authentication,
    ChannelInformation,
    CategoryOptout,
)
from profile_data.serializers import ProfileSerializer, CategoryOptoutSerializer
from main.tenant_middleware import get_timezone
from main.utils.common_utils import add_args


def total_profiles_created(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": Profile,
        "serializers": ProfileSerializer,
        "db_schema": get_db_name("profile"),
        "count": True,
        "distinct": True,
    }
    return params


def total_is_authenticated_profiles(request, authenticated):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": Profile,
        "serializers": ProfileSerializer,
        "db_schema": get_db_name("profile"),
        "filter_kwargs": {
            "is_authenticated": authenticated,
        },
        "count": True,
        "distinct": True,
    }
    return params


def authenticated_or_not(request):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": Profile,
        "serializers": ProfileSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "label": Case(
                When(is_authenticated=True, then=Value("Verified")),
                default=Value("Unverified"),
                output_field=CharField(),
            ),
        },
        "annotate": {"count": Count("label")},
        "order_by": ["-count"],
        "not_paginated": True,
    }
    return params


def authenticated_details(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    qs = (
        Authentication.objects.using(get_db_name("profile"))
        .filter(
            profile__timestamp__range=filter_data.get("timestamp__range"),
            profile__is_authenticated=True,
        )
        .values(
            Profile_Id=F("profile__profile_id"),
            User_Id=F("user_id"),
            Username=F("profile__user_name"),
            Phone_Number=F("profile__mobile_number"),
            Email=F("profile__email"),
            Module=F("provider"),
            Timestamp=Trunc(F("profile__timestamp"), "second", tzinfo=get_timezone()),
        )
    )
    result = []
    for i in qs:
        auth_profile_id = i["Profile_Id"]
        channel_info = (
            ChannelInformation.objects.using(get_db_name("profile"))
            .filter(profile_id=auth_profile_id)
            .values("channel_name", "channel_id")
        )

        for channel in channel_info:
            data = {
                "Profile_Id": auth_profile_id,
                "User_Id": i.get("User_Id"),
                "Username": i.get("Username"),
                "Channel": channel.get("channel_name"),
                "Channel_Id": channel.get("channel_id"),
                "Phone_Number": i.get("Phone_Number"),
                "Email": i.get("Email"),
                "Module": i.get("Provider"),
                "Timestamp": i.get("Timestamp"),
            }
            result.append(data)

    return (
        result,
        [
            "Profile_Id",
            "User_Id",
            "Username",
            "Channel",
            "Channel_Id",
            "Phone_Number",
            "Email",
            "Module",
            "Timestamp",
        ],
        "verified_profile_details",
    )


def unauthenticated_details(request):
    dynamic_db_connection("profile")
    filter_data = request.data
    qs = (
        ChannelInformation.objects.using(get_db_name("profile"))
        .filter(
            profile__timestamp__range=filter_data.get("timestamp__range"),
            profile__is_authenticated=False,
        )
        .values(
            Profile_Id=F("profile_id"),
            Username=F("profile__user_name"),
            Channel=F("channel_name"),
            Channel_Id=F("channel_id"),
            Phone_Number=F("profile__mobile_number"),
            Email=F("profile__email"),
            Timestamp=Trunc(F("profile__timestamp"), "second", tzinfo=get_timezone()),
        )
    )
    return (
        qs,
        [
            "Profile_Id",
            "Username",
            "Channel",
            "Channel_Id",
            "Phone_Number",
            "Email",
            "Timestamp",
        ],
        "unverified_profile_details",
    )


def profile_opted_in_or_out_details(request, key=None, value=None):
    dynamic_db_connection("profile")
    params = {
        "request": request,
        "models": CategoryOptout,
        "serializers": CategoryOptoutSerializer,
        "db_schema": get_db_name("profile"),
        "values_kwargs": {
            "Profile_Id": F("profile__profile_id"),
            "Username": F("profile__user_name"),
            "Channel": F("channel_information__channel_name"),
            "Channel_Id": F("channel_information__channel_id"),
            "Opted_In": Case(
                When(category="OPTIN", then=Value("Utility and Marketing")),
                When(category="ALL", then=Value("None")),
                When(category="UTILITY", then=Value("Marketing")),
                When(category="MARKETING", then=Value("Utility")),
                output_field=CharField(),
            ),
            "Opted_Out": Case(
                When(category="OPTIN", then=Value("None")),
                When(category="ALL", then=Value("Utility and Marketing")),
                When(category="UTILITY", then=Value("Utility")),
                When(category="MARKETING", then=Value("Marketing")),
                output_field=CharField(),
            ),
        },
        "annotate": {
            "Timestamp": Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        },
        "order_by": ["-Timestamp"],
    }
    return add_args(params, key, value)
