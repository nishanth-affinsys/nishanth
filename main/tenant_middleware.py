import threading

import pytz
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from main.utils.time_zone_utils import get_zone

_LOCAL = threading.local()


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        tenant = request.COOKIES.get("tenant")
        offset = request.headers.get("offset")
        setattr(
            _LOCAL,
            "timezone",
            get_zone(offset) if settings.USE_OFFSET else get_zone("UTC"),
        )
        setattr(_LOCAL, "tenant", tenant)
        response = self.get_response(request)
        return response


def get_current_tenant_name():
    return getattr(_LOCAL, "tenant", None)


def set_current_tenant_name(tenant_name):
    setattr(_LOCAL, "tenant", tenant_name)


def set_timezone(offset):
    setattr(_LOCAL, "timezone", get_zone(offset) if settings.USE_OFFSET else get_zone("UTC"))


def get_timezone():
    return getattr(_LOCAL, "timezone", pytz.timezone("UTC"))
