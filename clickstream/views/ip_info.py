# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
#
# from clickstream.services.ip_info_utils import (
#     ip_information_generic,
#     user_country_funnel_generic,
#     user_country_geo_generic,
#     total_sessions_on_website_generic,
#     total_users_on_website_generic,
#     location_based_visits_details_generic,
#     device_based_visits_generic,
# )
# from main.settings import MAX_PDF_LIMIT
# from main.utils.boiler_plate import (
#     get_generic_response,
#     return_table,
# )
# from main.utils.export import export_csv, export_pdf
#
#
# class IpInfoViewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="ip_information",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying IP Details of a User",
#     )
#     @action(methods=["POST"], detail=False, url_path="ip_information")
#     def ip_information(self, request, *args, **kwargs):
#         """
#         The ip_information function returns a table of IP information for each session.
#
#         :param self: Represent the instance of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A table of ip information
#         """
#         qs, _, _ = ip_information_generic(request)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="ip_information_export_csv",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading IP Details of a User in csv formate",
#     )
#     @action(methods=["POST"], detail=False, url_path="ip-export")
#     def ip_information_export(self, request, *args, **kwargs):
#         """
#         The ip_information_export function is a view that returns a CSV file containing the following fields:
#         IP_address, User_id, Session_id, Continent, Country, City Region and Location.
#         The data is filtered by the parameters passed in through the request object.  The query function handles this filtering.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the query string from the url
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A csv file
#         """
#         response, field_names, file_name = ip_information_generic(request)
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="ip_information_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading IP Details of a User in pdf formate",
#     )
#     @action(methods=["POST"], detail=False, url_path="ip_information_export_pdf")
#     def ip_information_export_pdf(self, request, *args, **kwargs):
#         """
#         The ip_information_export_pdf function is used to export the IP information details in a PDF format.
#         The function takes in the request, and returns an iterator of bytes that can be written to a file.
#
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = ip_information_generic(request)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(response, field_names, f"{file_name}.pdf", "IP information")
#         return items
#
#     @extend_schema(
#         operation_id="total_sessions_on_website",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total Sessions on a Website",
#     )
#     @action(methods=["POST"], detail=False, url_path="total_sessions_on_website")
#     def total_sessions_on_website(self, request, *args, **kwargs):
#         """
#         The total_sessions_on_website function returns the total number of sessions on the website.
#
#         :param self: Represent the instance of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of sessions on the website
#         """
#         params = total_sessions_on_website_generic(request)
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="total_Users_on_website",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total Users on a Website",
#     )
#     @action(methods=["POST"], detail=False, url_path="total_Users_on_website")
#     def total_Users_on_website(self, request, *args, **kwargs):
#         """
#         The total_Users_on_website function returns the total number of unique users on the website.
#             This is accomplished by querying all ClickstreamRecord objects in the clickstream database,
#             and returning a count of distinct user_identifier__browser_id values.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The total number of users on the website
#         """
#         params = total_users_on_website_generic(request)
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="location_based_visits",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total visits by each location",
#     )
#     @action(methods=["POST"], detail=False, url_path="location_based_visits")
#     def location_based_visits(self, request, *args, **kwargs):
#         """
#         The location_based_visits function returns a table of the top 10 cities and countries
#             where users are visiting from. The data is pulled from the clickstream database,
#             specifically the ClickstreamIpinformation table.
#
#         :param self: Allow an instance of a class to access its own attributes and methods
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A table of the most visited cities and countries
#         """
#         qs = location_based_visits_details_generic(request)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="device_based_visits",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total visits by each device",
#     )
#     @action(methods=["POST"], detail=False, url_path="device_based_visits")
#     def device_based_visits(self, request, *args, **kwargs):
#         """
#         The device_based_visits function returns a table of the number of visits by device type.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass a variable number of keyword arguments to the function
#         :return: The number of visits to the website based on the device type
#         """
#         qs = device_based_visits_generic(request)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="visits_by_device_export_csv",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading Total visits by each device in csv formate",
#     )
#     @action(methods=["POST"], detail=False, url_path="visits_device-export")
#     def visits_by_device_export(self, request, *args, **kwargs):
#         """
#         The visits_by_device_export function returns a CSV file containing the number of visits by device type.
#
#         :param self: Refer to the current object
#         :param request: Get the query parameters from the request
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A csv file with the device type and count of visits
#         """
#         items = device_based_visits_generic(request)
#         it = export_csv(items, ["device_type", "count"], "visits_by_device.csv")
#         return it
#
#     @extend_schema(
#         operation_id="user_country_geo",
#         tags=[AuthTags.AUTHORIZE],
#         description="The map displays number of people coming from different countries",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_country_geo")
#     def user_country_geo(self, request, *args, **kwargs):
#         """
#         The user_country_geo function returns a list of countries and the number of users from each country.
#         The function takes in a request object, which is used to query the ClickstreamIpinformation table.
#         The query filters out duplicate session_ids, then counts how many times each country appears in the filtered results.
#
#         :param self: Access the attributes and methods of the class in python
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A list of dictionaries containing the country name and the number of users from that country
#         """
#         qs = user_country_geo_generic(request)
#         return Response(qs)
#
#     @extend_schema(
#         operation_id="user_country_funnel",
#         tags=[AuthTags.AUTHORIZE],
#         description="The funnel displays number of people coming from different countries",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_country_funnel")
#     def user_country_funnel(self, request, *args, **kwargs):
#         qs = user_country_funnel_generic(request)
#         return Response(qs)
