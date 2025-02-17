# from auth.tags import AuthTags
# from drf_spectacular.utils import extend_schema
#
# from client_specific.services.nbf_lead_generator_utils import (
#     leads_generic,
#     lead_by_products_generic,
# )
#
# from main.settings import MAX_PDF_LIMIT
# from main.utils.export import export_csv, export_pdf
# from rest_framework.decorators import action
# from rest_framework.viewsets import GenericViewSet
#
# from main.utils.boiler_plate import get_generic_response, return_table
#
#
# class LeadGeneratorViewSet(GenericViewSet):
#     @extend_schema(
#         operation_id="leads_total",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total leads",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_total")
#     def total_leads(self, request, *args, **kwargs):
#         """
#         The total_leads function returns the total number of leads for a given tenant.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object from the view
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of leads (distinct) that have completed a goal
#         """
#         params = leads_generic(request, "Final Response", "Goal Completed")
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="leads_total_NTB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total NTB leads",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_total_NTB")
#     def total_ntb_leads(self, request, *args, **kwargs):
#         """
#         The total_NTB_leads function returns the total number of NTB leads for a given tenant.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object, which contains all the information about the current request
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of leads that are not yet booked
#         """
#         params = leads_generic(request, "User status", "no")
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="leads_total_ETB",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total ETB leads",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_total_ETB")
#     def total_etb_leads(self, request, *args, **kwargs):
#         """
#         The total_ETB_leads function returns the total number of ETB leads.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: The number of leads that have been
#         """
#         params = leads_generic(request, "User status", "yes")
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="leads_interested_for_call",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total customers interested for call",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_interested_for_call")
#     def interested_for_call(self, request, *args, **kwargs):
#         """
#         The interested_for_call function is used to get the number of interested people for call.
#
#         :param self: Represent the instance of the class
#         :param request: Get the tenant name from the request
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: A dictionary with the following keys:
#         """
#         params = leads_generic(request, "Call", "yes")
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="leads_not_interested_for_call",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying Total customers not interested for call",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_not_interested_for_call")
#     def not_interested_for_call(self, request, *args, **kwargs):
#         """
#         The not_interested_for_call function returns the number of unique channel_ids for which a call was made and the
#         result was 'no'
#
#         :param self: Represent the instance of the object
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list to a function
#         :return: The number of distinct channel_ids for which the stage is call and stage_result is no
#         """
#         params = leads_generic(request, "Call", "no")
#         return get_generic_response(params)
#
#     @extend_schema(
#         operation_id="leads_by_products",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for displaying detailed report of lead products",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_by_products")
#     def lead_by_products(self, request, *args, **kwargs):
#         """
#         The lead_by_products function returns a table of leads by product.
#
#         :param self: Represent the instance of the object itself
#         :param request: Get the request object
#         :param *args: Pass a non-keyworded, variable-length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A table of the following format:
#         """
#
#         response, _, _ = lead_by_products_generic(request)
#         items = return_table(response, request)
#         return items
#
#     @extend_schema(
#         operation_id="leads_by_products_export_csv",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading detailed report of lead products",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_by_products_export_csv")
#     def lead_by_products_export(self, request, *args, **kwargs):
#         """
#         The lead_by_products_export function is used to export a CSV file containing the following information:
#             - channel_id (the unique identifier of the user)
#             - product (the product that was inquired about by the user)
#             - status (whether or not this lead has been converted into an ETB or NTB)
#             - timestamp (when this lead was created/updated).
#
#         :param self: Represent the instance of the object
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A csv file with the following columns:
#         """
#         response, field_names, file_name = lead_by_products_generic(request)
#         items = export_csv(
#             response,
#             field_names,
#             f"{file_name}.csv",
#         )
#         return items
#
#     @extend_schema(
#         operation_id="leads_by_products_export_pdf",
#         tags=[AuthTags.AUTHORIZE],
#         description="Used for downloading detailed report of lead products",
#     )
#     @action(methods=["POST"], detail=False, url_path="leads_by_products_export_pdf")
#     def lead_by_products_export_pdf(self, request, *args, **kwargs):
#         """
#         The lead_by_products_export_pdf function is used to export a PDF file containing the lead by products data.
#         The function takes in the request, *args and **kwargs as parameters. The tz_info variable is set to pytz.timezone(settings.TIME_ZONE).
#         The field variable is set to &quot;Loan&quot;. If get_current_tenant_name() returns &quot;islamic&quot;, then field will be set to &quot;Finance&quot;.
#         A qs object is created using query(), StageLog, TransactionSerializer and db schema=&quot;event&quot; as parameters for the query().
#         qs object filters out all transactions
#
#         :param self: Represent the instance of the object
#         :param request: Get the request object
#         :param *args: Send a non-keyworded variable length argument list to the function
#         :param **kwargs: Pass keyworded, variable-length argument list
#         :return: A pdf file
#         """
#         response, field_names, file_name = lead_by_products_generic(request)
#         if len(response) > MAX_PDF_LIMIT:
#             response = response[:MAX_PDF_LIMIT]
#         items = export_pdf(
#             response,
#             field_names,
#             f"{file_name}.pdf",
#             "Lead by products",
#             request.user.username,
#         )
#         return items
