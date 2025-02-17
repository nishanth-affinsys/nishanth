import json
import time
import conf
import pytz
from datetime import datetime

from http.client import responses

from django.db.models.functions import Concat
from auth.tags import AuthTags
from auth.user_types import UserType
from django.db.models import F, Value, CharField
from drf_spectacular.utils import extend_schema
from metadata.client import get_project_metadata
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from metadata.loader import MetadataLoader
from console.services.get_dashboard_names import (
    get_dashboard_names,
    refresh_dashboard_cache,
    get_repo_url
)
from console.services.transaction_reports_utils import get_intent_details, get_customer
from campaign_manager.models import Campaign
from lib.exception_handling import StandardException
from django.conf import settings
from main.tenant_middleware import get_current_tenant_name
from api_request_logging.middleware import get_location
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from console.serializers import RequestDataSerializer
from django.core.cache import cache
import os


# For Dashboard API
def get_dashboard_details(request, chartid):
    tenant = get_current_tenant_name()
    """Metadata Loading"""
    if get_project_metadata(tenant) is None:
        metadata_loader = MetadataLoader(tenant, repo_url=get_repo_url(tenant), force_clone=True)
        metadata_loader()
    start_time = time.time()
    client_ip = get_client_ip(request)
    client_location = get_location(client_ip)
    try:
        # dashboard_data = json.load(open(f"{settings.BASE_DIR}/console/static/{chartid}.json"))
        with open(f"{settings.BASE_DIR}/console/static/{chartid}.json") as file:
            dashboard_data = json.load(file)
        file.close()
        if conf.getenv(tenant, key="DASHBOARD_LOCATION") in dashboard_data.keys():
            data = dashboard_data[conf.getenv(tenant, key="DASHBOARD_LOCATION")]
        else:
            data = dashboard_data["common"]

        data["time_offset"] = conf.getenv(tenant, key="MAX_TIME_RANGE")
        data["USE_TZ"] = settings.USE_OFFSET
        response = Response(data)
        if settings.LOG_ACTIVITY_PUBSUB:
            payload = dict(
                method="activity",
                provider=request.headers.get("Bb-Provider"),
                user_id=request.headers.get("Bb-User-Id"),
                username=request.headers.get("Bb-Username"),
                operation="",
                endpoint=request.path,
                result="pass",
                status_code=response.status_code,
                status_code_description=responses[response.status_code],
                request_timestamp=start_time,
                request_method=request.method,
                execution_time=start_time,
                service_name=settings.SERVICE_NAME,
                request_body=None,
                response_body=data,
                timestamp=start_time,
                ip_address=client_ip,
                location=client_location,
                tenant=tenant,
            )
            (
                settings.PUBSUB.produce(
                    f"{tenant}.{settings.SERVICE_NAME}.logging.request",
                    json.dumps(payload),
                )
                if os.getenv("PUBSUB_BROKEN") == "nats"
                else settings.PUBSUB.produce(tenant, payload)
            )
        return response
    except KeyError as e:
        res = Response(status=404)
        if settings.LOG_ACTIVITY_PUBSUB:
            payload = dict(
                method="activity",
                provider=request.headers.get("Bb-Provider"),
                user_id=request.headers.get("Bb-User-Id"),
                username=request.headers.get("Bb-Username"),
                operation="",
                endpoint=request.path,
                result="fail",
                status_code=res.status_code,
                status_code_description=responses[res.status_code],
                request_timestamp=start_time,
                request_method=request.method,
                execution_time=start_time,
                service_name=settings.SERVICE_NAME,
                request_body=None,
                response_body=None,
                timestamp=start_time,
                ip_address=client_ip,
                location=client_location,
                tenant=tenant,
            )
            (
                settings.PUBSUB.produce(
                    f"{tenant}.{settings.SERVICE_NAME}.logging.request",
                    json.dumps(payload),
                )
                if os.getenv("PUBSUB_BROKEN") == "nats"
                else settings.PUBSUB.produce(tenant, payload)
            )
        raise StandardException(code="ER-0008", status_code=status.HTTP_404_NOT_FOUND)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        _ip = x_forwarded_for.split(",")[0]
    else:
        _ip = request.META.get("REMOTE_ADDR")
    return _ip


@extend_schema(
    operation_id="dashboard",
    tags=[AuthTags.AUTHORIZE, {UserType.WALLET_CUSTOMER: AuthTags.AUTHENTICATE}],
    description="Used for get the respective dashboard",
)
@api_view(["GET"])
def dashboard(request, chartid):
    """
    The dashboard function is a view that returns the dashboard template for the
        chartid passed in. The chartid is used to look up the correct dashboard
        template from a dictionary of templates.

    :param request: Get the request object
    :param chartid: Get the chart data from the dashboard_tempalate dictionary
    :return: A response object with the dashboard template
    :doc-author: Trelent
    """
    response = get_dashboard_details(request, chartid)
    return response


@extend_schema(
    operation_id="get_channels",
    tags=[AuthTags.AUTHORIZE],
    description="Used for get the channel filters for a client",
)
@api_view(["GET"])
def channels(request):
    """
    The channels function returns a list of channels that are available for the current tenant.

    :param request: Get the current tenant name
    :return: The following:
    :doc-author: Trelent
    """
    try:
        dict_map = {
            "messenger": "Facebook",
            "instagram": "Instagram",
            "webchat": "Webchat",
            "line": "Line",
            "telegram": "Telegram",
            "twitter": "Twitter",
            "viber": "Viber",
            "smst": "SMS (Twilio)",
            "sm": "SoulMachine",
            "smsa": "SMS (AWS)",
            "smsi": "SMS (Infobip)",
            "email": "Email",
            "ivr": "IVR",
            "firebase": "Firebase",
            "firebasec": "Firebase (Customer)",
            "firebasem": "Firebase (Merchant)",
            "mobile": "Mobile",
            "whatsapp": "Whatsapp (Meta)",
            "whatsappc": "Whatsapp (Clickatell)",
            "whatsappi": "Whatsapp (Infobip)",
            "whatsapps": "Whatsapp (Sunshine)",
            "whatsappk": "Whatsapp (Tanla Karyx)",
            "whatsapprcm": "Whatsapp (Tanla RCM)",
            "whatsappt": "Whatsapp (Twilio)",
            "whatsappa": "Whatsapp (Ameyo)",
        }
        tenant = get_current_tenant_name().replace("_bkp", "")
        special_channels = conf.getenv(tenant, key="SPECIAL_CHANNELS")
        special_channels_dict = json.loads(special_channels)
        channels = get_project_metadata(tenant).get("channel_code")
        response = []
        # for regular channels
        for channel in channels:
            display_value = dict_map.get(channel)
            if display_value:
                data = {"display_value": display_value, "api_value": channel}
                response.append(data)
        # for special channels
        for special_channel, special_display in special_channels_dict.items():
            if special_channel not in dict_map:
                data = {"display_value": special_display, "api_value": special_channel}
                response.append(data)
        return Response({"list_of_values": response})
    except AttributeError:
        if settings.USE_METADATA:
            raise StandardException(
                code="ER-0007", status_code=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response([])


@extend_schema(
    operation_id="get_campaigns",
    tags=[AuthTags.AUTHORIZE],
    description="Used for get the campaign filters for a client",
)
@api_view(["POST"])
def campaign_names(request, **kwargs):
    dynamic_db_connection("campaign")
    filter_data = request.data
    filter_data.update(**kwargs)
    qs = (
        Campaign.objects.using(get_db_name("campaign"))
        .filter(last_modified__range=filter_data.get("timestamp__range"))
        .filter(tenant=get_current_tenant_name())
        .values(
            api_value=F("id"),
            display_value=Concat(F("campaign_id"), Value(" "), F("campaign_name"), output_field=CharField()))
        .order_by("-created_timestamp")
    )
    return Response({"list_of_values": qs})


# @extend_schema(
#     operation_id="endpoints",
#     tags=[AuthTags.INTERNAL],
#     description="Used for get all api endpoints",
# )
# @api_view(["GET"])
# def endpoints(request):
#     data = {}
#     service_prefix = "/analytics-new/reports/"
#     for key, value in dashboard_tempalate.items():
#         dashboard = f"/analytics-new/reports/dashboard/{key}"
#         chart_api_url = [
#             service_prefix + item["chart_api_url"]
#             for item in value["charts"]
#             if item.get("chart_api_url") and item["chart_api_url"] != 0
#         ]
#         chart_report_api = [
#             service_prefix + item["chart_report_api"]
#             for item in value["charts"]
#             if item.get("chart_report_api") and item["chart_report_api"] != 0
#         ]
#         chart_report_pdf_api = [
#             service_prefix + item["chart_report_pdf_api"]
#             for item in value["charts"]
#             if item.get("chart_report_pdf_api") and item["chart_report_api"] != 0
#         ]
#         endpoints = [
#             dashboard,
#             *chart_api_url,
#             *chart_report_api,
#             *chart_report_pdf_api,
#         ]
#         if len(endpoints) > 1:
#             data[key] = endpoints
#         print(endpoints[1:])
#     return Response(data)
@extend_schema(
    operation_id="get_dashboard_details",
    tags=[AuthTags.AUTHORIZE],
    description="Function to return all dashboard names to analytics frontend",
)
@api_view(["GET"])
def get_dashboard_name(request, *args, **kwargs):
    if cache.get("dashboard_details"):
        dashboard_details = json.loads(cache.get("dashboard_details"))
    else:
        tenant = get_current_tenant_name()
        dashboard_details = get_dashboard_names(request, tenant)
    return Response(dashboard_details)


@extend_schema(
    operation_id="get_intents",
    tags=[AuthTags.AUTHORIZE],
    description="Used to fetch the intents for the transaction dashboard"
)
@api_view(["GET"])
def get_intents(request, *args, **kwargs):
    intents = get_intent_details(request)
    return Response({"list_of_values": intents})


@extend_schema(
    operation_id="get_customer_types",
    tags=[AuthTags.AUTHORIZE],
    description="Used to fetch the customer type for the dashboard"
)
@api_view(["GET"])
def get_customer_types(request, *args, **kwargs):
    customer_types = get_customer(request)
    return Response({"list_of_values": customer_types})


@extend_schema(
    operation_id="check_changes",
    tags=[AuthTags.AUTHORIZE],
    description="Endpoint to serialize the commit and check github changes",
)
@api_view(["POST"])
def handle_request(request, *args, **kwargs):
    serializer = RequestDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    tenant = get_current_tenant_name()
    for commits in validated_data["commits"]:
        if "config.env" in commits["modified"]:
            refresh_dashboard_cache(request, tenant)
            return Response("refreshed")


@extend_schema(
    operation_id="live_transaction",
    tags=[AuthTags.PUBLIC],
    description="Used to show the live public dashboard for dib."
)
@api_view(["GET"])
def live_transaction(request):
    response = get_dashboard_details(request, "live_transaction")
    return response


@extend_schema(
    operation_id="get_timezones",
    tags=[AuthTags.AUTHORIZE],
    description="used to load the timezones for analytics scheduler"
)
@api_view(["GET"])
def get_timezones(request, *args, **kwargs):
    timezone_list = []
    for tz in pytz.all_timezones:
        timezone = pytz.timezone(tz)
        offset = timezone.utcoffset(datetime.now())
        hours = offset.total_seconds() // 3600
        minutes = (offset.total_seconds() % 3600) // 60
        offset_str = f"{'+' if hours >= 0 else '-'}{int(abs(hours)):02}:{int(abs(minutes)):02}"
        timezone_list.append({'key': tz, 'value': offset_str})
    return Response(timezone_list)
