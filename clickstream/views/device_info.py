# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
#
# from clickstream.services.device_info_utils import (
#     device_information_generic,
#     sessions_per_device_generic,
#     operating_system_info_generic,
#     browser_info_generic,
# )
#
#
# # Visitors data has only OS info, device info and Browser info pie chart from this
# class DeviceInfoViewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="device_information",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Device Information",
#     )
#     @action(methods=["POST"], detail=False, url_path="device_information")
#     def device_information(self, request, *args, **kwargs):
#         """
#         The device_information function returns a list of device types and the number of times each type was used.
#         The function takes in a request object, which is passed to the query function. The query function returns a queryset
#         of ClickstreamDevice objects from the clickstream database schema. The queryset is then filtered by distinct session_id's,
#         and then grouped by device_type and counted.
#
#         :param self: Represent the instance of the object
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of users who used a particular device to access the website
#         """
#         items = device_information_generic(request)
#         return Response(items)
#
#     @extend_schema(
#         operation_id="sessions_per_device",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total Sessions per Device",
#     )
#     @action(methods=["POST"], detail=False, url_path="sessions_per_device")
#     def sessions_per_device(self, request, *args, **kwargs):
#         """
#         The sessions_per_device function returns the number of sessions per device type.
#
#         :param self: Refer to the class itself
#         :param request: Get the query string from the request
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass in any additional parameters
#         :return: The number of sessions per device type
#         """
#         items = sessions_per_device_generic(request)
#         return Response(items)
#
#     @extend_schema(
#         operation_id="operating_system_info",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Operating System",
#     )
#     @action(methods=["POST"], detail=False, url_path="operating_system_info")
#     def operating_system_info(self, request, *args, **kwargs):
#         """
#         The operating_system_info function returns a list of operating systems and the number of times each one was used.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass in keyword arguments to the function
#         :return: The operating system name and the count of users who use that operating system
#         """
#         items = operating_system_info_generic(request)
#         return Response(items)
#
#     @extend_schema(
#         operation_id="browser_info",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Browser Details",
#     )
#     @action(methods=["POST"], detail=False, url_path="browser_info")
#     def browser_info(self, request, *args, **kwargs):
#         """
#         The browser_info function is a function that returns the number of unique users
#         that have visited the website using each browser. The function takes in a request,
#         and then uses query to get all of the data from ClickstreamBrowser and serialize it.
#         It then gets all distinct session_ids from this data, and filters out any values that are not in this list.
#         Then it counts how many times each browser name appears in this filtered list.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of times each browser was used to access the website
#         """
#         items = browser_info_generic(request)
#         return Response(items)
