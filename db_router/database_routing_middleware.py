import threading
import logging
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

logger = logging.getLogger("db_router")
_LOCAL = threading.local()


class DatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        logger.info(f"Request Received : aaasbbb1233")
        if not settings.USE_DATABASE_AS_DEFAULT:
            client_code = request.COOKIES.get("project")
            if client_code in settings.TENANTS:
                setattr(_LOCAL, "client_code", client_code)
                response = self.get_response(request)
            else:
                response = Response(
                    data={
                        "detail": "Invalid Client Code",
                        "status_code": status.HTTP_401_UNAUTHORIZED,
                    }
                )
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                response.render()
        else:
            setattr(_LOCAL, "client_code", "default")
            response = self.get_response(request)
        return response


def get_current_db_name():
    return getattr(_LOCAL, "client_code", None)


def set_db_for_router(client_code):
    setattr(_LOCAL, "client_code", client_code)


def delete_db_for_router_if_exists():
    if hasattr(_LOCAL, "client_code"):
        delattr(_LOCAL, "client_code")
