from dataclasses import asdict
from typing import List

from django.conf import settings
from django.utils.encoding import force_str
from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.handler import ExceptionHandler
from drf_standardized_errors.types import ErrorResponse, Error
from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
    NotFound,
    PermissionDenied,
    ValidationError,
    MethodNotAllowed,
    UnsupportedMediaType,
    Throttled,
)
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


def get_error_details(data, code=None):
    """
    Same as drf's _get_error_details but will only use the code passed to this function.
    The original function will first try to use a code attribute of the data argument passed, if the attribute exists.
    We don't want that since default serializer errors will contain codes like 'invalid', 'required', etc.
    This function ensures that the codes returned in the response are always ER-XXXX.
    """
    if isinstance(data, (list, tuple)):
        ret = [get_error_details(item, code) for item in data]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {key: get_error_details(value, code) for key, value in data.items()}
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret
    text = force_str(data)
    return ErrorDetail(text, code)


class StandardExceptionFormatter(ExceptionFormatter):
    """
    Modifying default error response format to:
    {
        "errors": [
            {
                "code": "ER-XXXX",
                "detail": "Error message",
                "attr": "attribute name"
            }
        ]
    }
    """

    def format_error_response(self, error_response: ErrorResponse):
        errors: List[Error] = error_response.errors
        errors_list = [asdict(error) for error in errors]

        return {"errors": errors_list}


class StandardException(APIException):
    """
    Standard Exception class that takes in status_code
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Unknown Error"
    default_code = "ER-XXXX"

    def __init__(
        self,
        detail=None,
        code=None,
        status_code=None,
        params=None,
        locale=None,
        attr=None,
    ):
        if (
            not params
        ):  # Formatting params can't be None, and default argument type can't be mutable
            params = {}
        if code:
            # Later, locale to be used can be inferred from the request,
            # like get_current_locale() similar to get_current_db_name()
            detail = detail or settings.ERROR_MESSAGES.get(
                f"{code}_{locale or settings.DEFAULT_LOCALE}", self.default_detail
            )
        else:
            code, detail = self.default_code, detail or self.default_detail
        if isinstance(detail, str):
            detail = detail.format(**params)

        if attr:
            detail = {attr: detail}

        if status_code:
            self.status_code = status_code

            # For validation failures, we may collect many errors together,
            # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = get_error_details(detail, code)


class StandardExceptionHandler(ExceptionHandler):
    def convert_known_exceptions(self, exc: Exception) -> Exception:
        """
        Converts drf exceptions into StandardExceptions + converting validation errors into input errors so that
        default serializer errors get converted to StandardExceptions.
        Note that explicit ValidationErrors must not be raised, raise StandardExceptions directly instead.
        """
        if isinstance(exc, ValidationError):  # For default serializer errors
            return StandardException(
                code="ER-0001",
                detail=exc.detail,
                status_code=status.HTTP_400_BAD_REQUEST,
            )  # Invalid Input
        elif isinstance(exc, PermissionDenied):
            return StandardException(
                code="ER-0002", detail=exc.detail, status_code=status.HTTP_403_FORBIDDEN
            )  # Permission Denied
        elif isinstance(exc, NotFound):
            return StandardException(
                code="ER-0003", detail=exc.detail, status_code=status.HTTP_404_NOT_FOUND
            )  # Not Found
        elif isinstance(exc, MethodNotAllowed):
            return StandardException(
                code="ER-0004",
                detail=exc.detail,
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            )  # Method Not Allowed
        elif isinstance(exc, UnsupportedMediaType):
            return StandardException(
                code="ER-0005",
                detail=exc.detail,
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )  # Unsupported Media Type
        elif isinstance(exc, Throttled):
            return StandardException(
                code="ER-0006",
                detail=exc.detail,
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            )  # Throttled
        else:
            return exc
