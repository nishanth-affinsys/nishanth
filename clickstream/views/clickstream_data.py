# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
#
# from clickstream.services.clickstream_data_utils import (
#     user_location_piechart_generic,
#     user_redirection_generic,
# )
# from main.utils.boiler_plate import (
#     get_generic_response,
# )
#
#
# class ClickStreamDataViewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="user_city",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Cities",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_city")
#     def user_city(self, request, *args, **kwargs):
#         """
#         The user_city function returns a list of cities and the number of users from each city.
#         The function takes in a request object, which is used to query the ClickstreamIpinformation table.
#         The query filters out duplicate session_ids, then counts how many times each city appears in the filtered results.
#
#         :param self: Represent the instance of the object itself
#         :param request: Pass the request object to the view
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of distinct users per city
#         """
#         items = user_location_piechart_generic(request, "city")
#         return Response(items)
#
#     @extend_schema(
#         operation_id="user_country",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Countries",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_country")
#     def user_country(self, request, *args, **kwargs):
#         """
#         The user_country function returns a list of countries and the number of users from each country.
#         The function takes in a request object, which is used to query the ClickstreamIpinformation table.
#         The query is then filtered by distinct session_id's, and then grouped by country with an annotation for count.
#
#         :param self: Access the attributes and methods of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The country of the user
#         """
#         items = user_location_piechart_generic(request, "country")
#         return Response(items)
#
#     @extend_schema(
#         operation_id="user_region",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Regions",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_region")
#     def user_region(self, request, *args, **kwargs):
#         """
#         The user_region function returns a list of dictionaries containing the count and label for each region.
#         The function takes in a request, *args, and **kwargs as parameters.
#         It then creates a query set (qs) using the ClickstreamIpinformation model from clickstream database schema.
#         The serializer used is ClickStreamIpInformationSerializer which is imported from clickstream_serializers module.
#         Next it gets distinct session id's by filtering out duplicate records with same session id's using qs object created above and stores them in get_distinct_id variable as queryset values list of integers(
#
#         :param self: Refer to the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A list of dictionaries with the count and label keys
#         """
#         items = user_location_piechart_generic(request, "region")
#         return Response(items)
#
#     @extend_schema(
#         operation_id="user_continent",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying pie chart of Users Continent",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_continent")
#     def user_continent(self, request, *args, **kwargs):
#         """
#         The user_continent function returns a list of continents and the number of users from each continent.
#         The function takes in a request object, which is used to query the ClickstreamIpinformation table.
#         The query filters out duplicate session_ids, then counts how many times each continent appears in the filtered data set.
#
#         :param self: Access the class attributes and methods
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A list of dictionaries
#         """
#         items = user_location_piechart_generic(request, "continent")
#         return Response(items)
#
#     @extend_schema(
#         operation_id="user_redirection",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying details of user redirection from one page to other",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_redirection")
#     def user_redirection(self, request, *args, **kwargs):
#         """
#         The user_redirection function is used to return a table of all the redirects that have occurred on the site.
#         The function takes in a request object and returns an items object which contains information about each redirect.
#
#
#         :param self: Refer to the class itself
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A list of dictionaries
#         """
#         params = user_redirection_generic(request)
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="user_redirection_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading details of user redirection from one page to other",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_redirection_export")
#     def user_redirection_export(self, request, *args, **kwargs):
#         """
#         The user_redirection_export function is used to export a CSV file containing the following information:
#             - User ID
#             - Session ID
#             - Redirect from (the page that the user was redirected from)
#             - Redirect to (the page that the user was redirected to)
#             - Time spent on redirecting pages in HH24:MI:SS format.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A list of dictionaries
#         """
#         params = user_redirection_generic(
#             request,
#             key="csv_kwargs",
#             value={
#                 "fieldNames": [
#                     "User_id",
#                     "Session_id",
#                     "Redirect_from",
#                     "Redirect_to",
#                     "Time_spent",
#                     "Timestamp",
#                 ],
#                 "fileName": "user_redirection.csv",
#             },
#         )
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="user_redirection_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading details of user redirection from one page to other",
#     )
#     @action(methods=["POST"], detail=False, url_path="user_redirection_export_pdf")
#     def user_redirection_export_pdf(self, request, *args, **kwargs):
#         """
#         The user_redirection_export_pdf function is used to export the user redirection data in a PDF format.
#         The function takes in the request, and *args and **kwargs as parameters. The tz_info variable is set to
#         the timezone of settings.TIME_ZONE (which is UTC). The qs variable queries ClickstreamAction using query(),
#         and uses ClickStreamActionSerializer for serialization, with db_schema=&quot;clickstream&quot;. Then qs filters by action type &quot;navigate&quot;,
#         and annotates User id, Session id, Time spent on page (in HH:MM:SS), Redirect
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         params = user_redirection_generic(
#             request,
#             key="pdf_kwargs",
#             value={
#                 "fieldNames": [
#                     "User_id",
#                     "Session_id",
#                     "Redirect_from",
#                     "Redirect_to",
#                     "Time_spent",
#                     "Timestamp",
#                 ],
#                 "fileName": "user_redirection.pdf",
#                 "title": "User Redirections",
#             },
#         )
#         return get_generic_response(params)
