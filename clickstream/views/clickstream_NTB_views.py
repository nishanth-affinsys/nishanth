# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
# from rest_framework.decorators import action
# from rest_framework.viewsets import GenericViewSet
#
# from clickstream.services.clickstream_ETB_NTB_utils import (
#     clickstream_complete_user_details_generic,
#     uservice_clicks_count_generic,
#     uservice_browser_details_generic,
#     uservice_device_details_generic,
#     number_of_ntb_cust_generic,
#     uservice_ipinformation_details_generic,
# )
# from main.settings import MAX_PDF_LIMIT
# from main.utils.boiler_plate import (
#     get_generic_response,
#     return_table,
# )
# from main.utils.export import export_csv, export_pdf
#
# ntb = "NTB"
#
#
# class NTBviewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="Number_of_NTB_cust",
#         tags=[AuthTags.AUTHORIZE],
#         description="Total number of users in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="number_of_NTB_cust")
#     def number_of_NTB_cust(self, request, *args, **kwargs):
#         """
#         The number_of_NTB_cust function returns the number of customers who have never been to a branch.
#         This is accomplished by filtering out all records where the user_id and browser_id are equal,
#         and then counting how many distinct session IDs there are.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of customers who have never been to the website before
#         """
#         params = number_of_ntb_cust_generic(request)
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="uservice_ipinformation_NTB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Ip information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_ipinformation_NTB")
#     def uservice_ipinformation_NTB(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_NTB function is a generic function that returns the ip information of users.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A response with the following attributes
#         """
#         qs, _, _ = uservice_ipinformation_details_generic(request, ntb)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="uservice_ipinformation_NTB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Ip information of each user in NTB",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_ipinformation_NTB_export"
#     )
#     def uservice_ipinformation_NTB_export(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_NTB_export function is used to export the IP information of users who have not been tagged as bots.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A csv file
#         """
#         response, field_names, file_name = uservice_ipinformation_details_generic(
#             request, ntb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="uservice_ipinformation_NTB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Ip information of each user in NTB",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_ipinformation_NTB_export_pdf"
#     )
#     def uservice_ipinformation_NTB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_NTB_export_pdf function is used to export the IP information of users in a PDF file.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_ipinformation_details_generic(
#             request, ntb
#         )
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "NTB IP information details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_device_NTB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Device information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_NTB")
#     def uservice_device_NTB(self, request, *args, **kwargs):
#         """
#         The uservice_device_NTB function is a generic function that returns the device information for each user.
#         The function takes in a request and uses it to get the parameters from the url. The parameters are then used to filter
#         the data based on what was requested by the user. The filtered data is then serialized using ClickStreamDeviceSerializer,
#         and returned as JSON.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A response object
#         """
#         qs, _, _ = uservice_device_details_generic(request, ntb)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="uservice_device_NTB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Device information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_NTB_export")
#     def uservice_device_NTB_export(self, request, *args, **kwargs):
#         """
#         The uservice_device_NTB_export function is a view that exports the device information of users who have not been tagged as bots.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A generator object
#         """
#         response, field_names, file_name = uservice_device_details_generic(request, ntb)
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="uservice_device_NTB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Device information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_NTB_export_pdf")
#     def uservice_device_NTB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_device_NTB_export_pdf function is used to export the device information of users in a PDF file.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_device_details_generic(request, ntb)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "NTB device Details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_browser_NTB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Browser information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_NTB")
#     def uservice_browser_NTB(self, request, *args, **kwargs):
#         """
#         The uservice_browser_NTB function is a generic function that returns the browser information for each user.
#         The function takes in a request and *args, **kwargs as parameters. The params variable is set to an object containing
#         the following keys: &quot;request&quot;, &quot;models&quot;, &quot;serializers&quot;, &quot;db_schema&quot;, &quot;filter_kwargs&quot; (which contains the key-value pair
#         &quot;record__user_identifier__user_id&quot;: F(&quot;record__user_identifier__browser_id&quot;)), values (which contains the list of strings
#         [&quot;browser family&quot;,&quot;browser type&quot;,&quot;browser name&quot;,&quot;language&quot;]), values k
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A response object with the following keys:
#         """
#         qs, _, _ = uservice_browser_details_generic(request, ntb)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="uservice_browser_NTB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Browser information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_NTB_export")
#     def uservice_browser_NTB_export(self, request, *args, **kwargs):
#         """
#         The uservice_browser_NTB_export function is used to export the browser information for users who have not been tagged as bots.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A csv file
#         """
#         response, field_names, file_name = uservice_browser_details_generic(
#             request, ntb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="uservice_browser_NTB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Browser information of each user in NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_NTB_export_pdf")
#     def uservice_browser_NTB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_browser_NTB_export_pdf function is a custom function that allows the user to export the data from
#         the uservice_browser_NTB endpoint as a PDF file. The function takes in request, *args, and **kwargs parameters.
#         The tz_info variable stores the timezone information for this particular instance of NTB. The qs variable stores
#         the query results from querying ClickstreamBrowser with ClickStreamBrowserSerializer using db schema &quot;clickstream&quot;.
#         The items variable filters out all records where record__user_identifier__user_id does not equal record__user_identifier__browser id, then values are
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_browser_details_generic(
#             request, ntb
#         )
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "NTB Browser Details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="Complete_NTB_details",
#         tags=[AuthTags.AUTHORIZE],
#         description="Complete details of an NTB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="complete_NTB_details")
#     def complete_NTB_details(self, request, *args, **kwargs):
#         """
#         The complete_NTB_details function returns a table of user_id, session_id, IP address, continent, country and city
#         of the user's location at the time of login. It also returns device type and OS name as well as browser name used by
#         the user to access the website.
#
#         :param self: Represent the instance of the class
#         :param request: Get the query parameters from the url
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A table with the following columns:
#         """
#         response, _, _ = clickstream_complete_user_details_generic(request, ntb)
#         return return_table(response, request)
#
#     @extend_schema(
#         operation_id="Complete_NTB_details_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Complete details of an NTB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="complete_NTB_details_export")
#     def complete_NTB_details_export(self, request, *args, **kwargs):
#         """
#         The complete_NTB_details_export function is used to export a CSV file containing the following information:
#         user_id, session_id, IP address, continent, country, city (of user), device type (of user), device OS name (of user), browser name of the user and timestamp.
#
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A response object
#         """
#         response, field_names, file_name = clickstream_complete_user_details_generic(
#             request, ntb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="Complete_NTB_details_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Complete details of an NTB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="complete_NTB_details_export_pdf")
#     def complete_NTB_details_export_pdf(self, request, *args, **kwargs):
#         """
#         The complete_NTB_details_export_pdf function is used to export the complete details of NTB users in a PDF file.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = clickstream_complete_user_details_generic(
#             request, ntb
#         )
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response,
#             field_names,
#             f"{file_name}.pdf",
#             "Complete NTB Customer Information",
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_NTB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total number of clicks made by each user in session",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_clicks_count_NTB")
#     def uservice_clicks_count_NTB(self, request, *args, **kwargs):
#         """
#         The uservice_clicks_count_NTB function returns a table of the number of clicks per user.
#             The function is called by the uservice_clicks_count_NTB endpoint in urls.py, which is accessed via a GET request to /api/uservice-clicks-count-ntb/.
#             The function uses query() from utils.py to create an initial queryset (qs) based on ClickstreamRecord objects in the clickstream database, using ClickStreamRecordSerializer as its serializer class and &quot;clickstream&quot; as its db schema name.
#             It then filters qs for only those records
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A table with the following columns:
#         """
#         qs1 = uservice_clicks_count_generic(request, ntb)
#         return return_table(qs1, request)
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_NTB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading Total number of clicks made by each user in session",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_clicks_count_NTB_export")
#     def uservice_clicks_count_NTB_export(self, request, *args, **kwargs):
#         """
#             The uservice_clicks_count_NTB_export function is a custom function that returns the number of clicks per user and session.
#             It takes in a request object, which contains information about the HTTP request that triggered this view.
#             The *args and **kwargs are arguments to be passed to other functions or methods. They allow us to pass an arbitrary number of arguments
#             to our function without having any prior knowledge of how many arguments can be passed in.
#
#         :param self: Represent the instance of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of clicks per user_id and session_id
#         """
#         response, field_names, file_name = uservice_clicks_count_generic(request, ntb)
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_NTB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading Total number of clicks made by each user in session",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_clicks_count_NTB_export_pdf"
#     )
#     def uservice_clicks_count_NTB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_clicks_count_NTB_export_pdf function is a custom function that allows the user to export the top MAX_PDF_LIMIT users with the most clicks on their NTBs.
#         The uservice_clicks_count_NTB_export_pdf function takes in a request and returns an exported PDF file containing information about each user's number of clicks on their NTBs.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The items
#         """
#         response, field_names, file_name = uservice_clicks_count_generic(request, ntb)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "Clicks by Each User"
#         )
#         return items
