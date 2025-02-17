from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from console.services.activity_utils import (
    complete_activity_details_generic,
    audit_log_details_generic,
)

from main.utils.boiler_plate import (
    get_generic_response,
)


class ActivityViewSet(GenericViewSet):
    @extend_schema(
        operation_id="list_user_activity",
        tags=[AuthTags.AUTHORIZE],
        description="details of all the actions performed in the console",
    )
    @action(methods=["POST"], detail=False, url_path="complete_activity_details")
    def complete_activity_details(self, request, *args, **kwargs):
        """
        The complete_activity_details function is a generic function that returns the activity details of all activities
            in the database. The function takes in a request object and returns an HTTP response with status code 200 if
            successful, or 400 if unsuccessful.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to the function
        :return: A response that contains the following information:
        """
        params = complete_activity_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="audit_log_user",
        tags=[AuthTags.AUTHORIZE],
        description="Detailed actions of audit are displayed here",
    )
    @action(methods=["POST"], detail=False, url_path="audit_log_details")
    def audit_log_details(self, request, *args, **kwargs):
        params = audit_log_details_generic(request)
        return get_generic_response(params)
