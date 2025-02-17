# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
#
# from rest_framework.decorators import action
# from rest_framework.response import Response
#
# from rest_framework.viewsets import GenericViewSet
#
# from clickstream.services.clickstream_ETB_NTB_utils import (
#     number_of_etb_cust_generic,
#     etb_cust_per_ntb_cust_generic,
#     clickstream_complete_user_details_generic,
#     uservice_clicks_count_generic,
#     uservice_browser_details_generic,
#     uservice_device_details_generic,
#     uservice_ipinformation_details_generic,
# )
#
# from main.settings import MAX_PDF_LIMIT
# from main.utils.export import export_csv, export_pdf
# from main.utils.boiler_plate import (
#     get_generic_response,
#     return_table,
# )
#
# # constant
# etb = "ETB"
#
#
# class ETBViewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="Number_of_ETB_cust",
#         tags=[AuthTags.AUTHORIZE],
#         description="total number of users in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="number_of_ETB_cust")
#     def number_of_ETB_cust(self, request, *args, **kwargs):
#         """
#         The number_of_ETB_cust function returns the number of unique users who have visited the site.
#         This is accomplished by querying ClickstreamRecord for all records where user_id and browser_id are not equal,
#         and then counting the distinct session ids.
#
#         :param self: Represent the instance of the class
#         :param request: Pass the request object to the view
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of distinct session_ids where the user_id and browser_id are not equal
#         """
#         params = number_of_etb_cust_generic(request)
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="ETB_cust_per_NTB_cust",
#         tags=[AuthTags.AUTHORIZE],
#         description="Ration of ETB per NTB",
#     )
#     @action(methods=["POST"], detail=False, url_path="ETB_cust_per_NTB_cust")
#     def ETB_cust_per_NTB_cust(self, request, *args, **kwargs):
#         """
#         The ETB_cust_per_NTB_cust function returns the ratio of ETB customers to NTB customers.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of etb customers per ntb customer
#         """
#         etb_res, ntb_res = etb_cust_per_ntb_cust_generic(request)
#         return Response(data={"count": int(etb_res / ntb_res)})
#
#     @extend_schema(
#         operation_id="uservice_ipinformation_ETB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Ip information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_ipinformation_ETB")
#     def uservice_ipinformation_ETB(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_ETB function is a generic function that returns the ip information of users.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A list of dictionaries
#         """
#         qs, _, _ = uservice_ipinformation_details_generic(request, etb)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="uservice_ipinformation_ETB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Ip information of each user in ETB",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_ipinformation_ETB_export"
#     )
#     def uservice_ipinformation_ETB_export(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_ETB_export function is a view that returns the ip information of users who have logged in to the ETB.
#
#         :param self: Represent the instance of the class
#         :param request: Get the query parameters from the url
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The ip_information
#         """
#         response, field_names, file_name = uservice_ipinformation_details_generic(
#             request, etb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     # pdf export for etb ip info
#     @extend_schema(
#         operation_id="uservice_ipinformation_ETB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Ip information of each user in ETB",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_ipinformation_ETB_export_pdf"
#     )
#     def uservice_ipinformation_ETB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_ipinformation_ETB_export_pdf function is a view that returns a PDF file containing the IP information of users who have visited the ETB website.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the query string from the url
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_ipinformation_details_generic(
#             request, etb
#         )
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "ETB Browser Details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_device_ETB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Device information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_ETB")
#     def uservice_device_ETB(self, request, *args, **kwargs):
#         """
#         The uservice_device_ETB function is a generic function that returns the device information for each user.
#         The function takes in a request object and uses it to get the parameters from the URL. The parameters are then used to filter
#         the data returned by this endpoint. The params dictionary contains all of the necessary information needed by
#         get_generic_response, which is called at the end of this function.
#
#         :param self: Represent the instance of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A response object
#         """
#         qs, _, _ = uservice_device_details_generic(request, etb)
#         return return_table(qs, request)
#
#     @extend_schema(
#         operation_id="uservice_device_ETB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Device information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_ETB_export")
#     def uservice_device_ETB_export(self, request, *args, **kwargs):
#         """
#         The uservice_device_ETB_export function is a view that exports the device information for each user session.
#         The function takes in a request and returns an iterator of CSV rows. The query filters out any sessions where the browser_id and user_id are equal, which means that there was no login event during that session. It then selects only distinct sessions based on their session id.
#
#         :param self: Represent the instance of the class
#         :param request: Get the query parameters from the request
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: An iterator
#         """
#         response, field_names, file_name = uservice_device_details_generic(request, etb)
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     # pdf for device info
#     @extend_schema(
#         operation_id="uservice_device_ETB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Device information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_device_ETB_export_pdf")
#     def uservice_device_ETB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_device_ETB_export_pdf function is used to export a PDF file containing the device information of users.
#
#         :param self: Represent the instance of a class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_device_details_generic(request, etb)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "ETB Device Details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_browser_ETB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Browser information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_ETB")
#     def uservice_browser_ETB(self, request, *args, **kwargs):
#         """
#         The uservice_browser_ETB function is a generic function that returns the browser data for each user.
#         The function takes in a request and *args, **kwargs as parameters. The params variable is set to an object containing:
#             - request: the request parameter passed into the uservice_browser_ETB function
#             - models: ClickstreamBrowser model from clickstream/models.py file (the model we are querying)
#             - serializers: ClickStreamBrowserSerializer from clickstream/serializers.py file (the serializer we are using)
#                 to format our response data before sending it back to the
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A response object
#         """
#         response, _, _ = uservice_browser_details_generic(request, etb)
#         return return_table(response, request)
#
#     @extend_schema(
#         operation_id="uservice_browser_ETB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Browser information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_ETB_export")
#     def uservice_browser_ETB_export(self, request, *args, **kwargs):
#         """
#         The uservice_browser_ETB_export function is a custom function that exports the browser data for each user session.
#         The export includes the following fields:
#         - browser_family (e.g., Chrome, Firefox)
#         - browser_type (e.g., desktop, mobile)
#         - browser_name (e.g., Chrome Mobile iOS, Firefox Desktop Linux)
#         - language
#         - timestamp of first event in session
#
#
#         :param self: Represent the instance of the class
#         :param request: Get the query parameters from the url
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A generator object
#         """
#         response, field_names, file_name = uservice_browser_details_generic(
#             request, etb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     # pdf for users browser info
#     @extend_schema(
#         operation_id="uservice_browser_ETB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Browser information of each user in ETB",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_browser_ETB_export_pdf")
#     def uservice_browser_ETB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_browser_ETB_export_pdf function returns a PDF file containing the browser information of users.
#
#         :param self: Represent the instance of the class
#         :param request: Get the query string
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = uservice_browser_details_generic(
#             request, etb
#         )
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "ETB Browser Details"
#         )
#         return items
#
#     @extend_schema(
#         operation_id="Complete_ETB_details",
#         tags=[AuthTags.AUTHORIZE],
#         description="Complete details of an ETB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="Complete_ETB_details")
#     def Complete_ETB_details(self, request, *args, **kwargs):
#         """
#         The Complete_ETB_details function returns a table of all the ETB records in the clickstream database.
#         The table includes columns for user_id, session_id, IP address, continent, country and city.
#         It also includes device type and OS name as well as browser name.  Finally it has a timestamp column.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A table of data
#         """
#         response, _, _ = clickstream_complete_user_details_generic(request, etb)
#         return return_table(response, request)
#
#     @extend_schema(
#         operation_id="Complete_ETB_details_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Complete details of an ETB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="complete_ETB_details_export")
#     def complete_ETB_details_export(self, request, *args, **kwargs):
#         """
#         The complete_ETB_details_export function is used to export a CSV file containing the following information:
#         user_id, session_id, IP address, continent, country, city (of user), device type (of user), device OS name (of user), browser name (used by the user) and timestamp.
#         The function takes in a request object as an argument and returns an iterator object.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A csv file
#         """
#         response, field_names, file_name = clickstream_complete_user_details_generic(
#             request, etb
#         )
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="Complete_ETB_details_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Download Complete details of an ETB customer",
#     )
#     @action(methods=["POST"], detail=False, url_path="complete_ETB_details_export_pdf")
#     def complete_ETB_details_export_pdf(self, request, *args, **kwargs):
#         """
#         The complete_ETB_details_export_pdf function is used to export a PDF file containing the complete ETB customer information.
#         The function takes in a request object and returns an iterator that can be used to generate the PDF file.
#
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = clickstream_complete_user_details_generic(
#             request, etb
#         )
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response,
#             field_names,
#             f"{file_name}.pdf",
#             "Complete ETB Customer Information",
#         )
#         return items
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_ETB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total number of clicks made by each user in session",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_clicks_count_ETB")
#     def uservice_clicks_count_ETB(self, request, *args, **kwargs):
#         """
#         The uservice_clicks_count_ETB function returns a table of the top users by number of clicks.
#         The function is called from the clickstream_uservice_clicks_count endpoint in urls.py, which is accessed via:
#         http://localhost:8000/clickstream/uservice-clicks-count/?format=json&amp;startDate=2020-01-01&amp;endDate=2020-02-29
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A table of data
#         """
#         qs1 = uservice_clicks_count_generic(request, etb)
#         return return_table(qs1, request)
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_ETB_export",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading Total number of clicks made by each user in session",
#     )
#     @action(methods=["POST"], detail=False, url_path="uservice_clicks_count_ETB_export")
#     def uservice_clicks_count_ETB_export(self, request, *args, **kwargs):
#         """
#         The uservice_clicks_count_ETB_export function is a custom function that allows the user to export a CSV file containing
#         the number of clicks per session for each user. The data in this CSV file is filtered by excluding any sessions where the
#         user_id and browser_id are equal, which means that only sessions where users were logged in will be included.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A csv file
#         """
#         response, field_names, file_name = uservice_clicks_count_generic(request, etb)
#         items = export_csv(response, field_names, f"{file_name}.csv")
#         return items
#
#     @extend_schema(
#         operation_id="uservice_clicks_count_ETB_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading Total number of clicks made by each user in session",
#     )
#     @action(
#         methods=["POST"], detail=False, url_path="uservice_clicks_count_ETB_export_pdf"
#     )
#     def uservice_clicks_count_ETB_export_pdf(self, request, *args, **kwargs):
#         """
#         The uservice_clicks_count_ETB_export_pdf function is a custom function that allows the user to export a PDF file
#         of the top MAX_PDF_LIMIT users with the most clicks on their session.
#
#         :param self: Represent the instance of the class
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: pdf file
#         """
#         response, field_names, file_name = uservice_clicks_count_generic(request, etb)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response, field_names, f"{file_name}.pdf", "Clicks by Each User"
#         )
#         return items
