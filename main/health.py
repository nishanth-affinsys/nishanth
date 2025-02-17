import os
import socket

import django.db.utils
import redis.exceptions
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from lib.exception_handling import StandardException
from auth.tags import AuthTags

from django.db import connection
from django.core.cache import cache

from django.conf import settings


@extend_schema(
    operation_id="get_healthz",
    description="This api gets the successful redis and database connection",
    tags=[AuthTags.INTERNAL],
    exclude=True,
)
@api_view(["GET"])
def get_healthz(request):
    try:
        cache.keys("*")
    except redis.exceptions.ConnectionError as e:
        raise StandardException(
            code="ER-0009", status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        ) from e

    try:
        connection.ensure_connection()
    except django.db.utils.OperationalError as e:
        raise StandardException(
            code="ER-0010", status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        ) from e

    if not os.path.isfile(f"{settings.BASE_DIR}/post_start.txt"):
        raise StandardException(
            code="ER-0011", status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    return Response({"message": "success"}, status=status.HTTP_200_OK)


@extend_schema(
    operation_id="get_liveness",
    description="This api gets the liveness status",
    tags=[AuthTags.INTERNAL],
    exclude=True,
)
@api_view(["GET"])
def get_liveness(request):
    return Response({"message": "success"}, status=status.HTTP_200_OK)
