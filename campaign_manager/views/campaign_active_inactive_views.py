from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from campaign_manager.services.campaign_active_inactive_utils import (
    created_campaigns_bignum_generic,
    campaigns_status_bignum_generic,
    deleted_campaigns_bignum_generic,
    active_inactive_linechart_generic,
    campaign_aggregate_details_generic,
    campaign_types_details_generic,
    sub_campaign_targeted_user_generic,
)
from main.settings import MAX_PDF_LIMIT
from main.utils.boiler_plate import get_generic_response, return_table
from main.utils.export import export_csv, export_pdf


class CampaignActiveInActiveViewSet(GenericViewSet):
    @extend_schema(
        operation_id="campaign_created_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Total Created campaign",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_created_bigNum")
    def created_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The created_campaigns_bigNum function returns a list of all campaigns created by the current tenant.
        The function is not paginated, and it returns a count of the number of variants for each campaign.

        :param self: Represent the instance of the object itself
        :param request: Get the request object from the view
        :param *args: Pass a variable number of arguments to a function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        params = created_campaigns_bignum_generic(request)
        return get_generic_response(params)

    # completed campaigns
    @extend_schema(
        operation_id="campaigns_completed_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display completed campaign Variants in the given Timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="campaigns_completed_bigNum")
    def completed_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The completed_campaigns_bigNum function returns a list of completed campaigns,
            with the number of variants in each campaign.

        :param self: Represent the instance of the object itself
        :param request: Pass the request object to the function
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of completed campaigns
        """
        params = campaigns_status_bignum_generic(request, "COMPLETED")
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaigns_active_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Active campaign Variants in the given Timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="campaigns_active_bigNum")
    def active_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The active_campaigns_bigNum function returns a list of all active campaigns,
            along with the number of variants in each campaign.

        :param self: Allow an instance of a class to access its own attributes and methods
        :param request: Pass the request object to the function
        :param *args: Send a non-keyworded variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A count of active campaigns
        """
        params = campaigns_status_bignum_generic(request, "ACTIVE")
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaigns_inactive_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display InActive campaign Variants in the given Timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="campaigns_inactive_bigNum")
    def inactive_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The inactive_campaigns_bigNum function returns a list of all inactive campaigns,
            along with the number of variants in each campaign.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Pass a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of inactive campaigns
        """
        params = campaigns_status_bignum_generic(request, "INACTIVE")
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaigns_deleted_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Deleted campaign Variants in the given Timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="campaigns_deleted_bigNum")
    def deleted_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The deleted_campaigns_bigNum function returns a list of all campaigns that have been deleted.
        The function takes in the request and *args, **kwargs parameters.
        It then creates a dictionary called params which contains the following keys:
            - request: The request parameter passed into the function.
            - models: The CampaignsCampaignvariant model from campaign/models.py file (the database table).  This is used to query data from this table in order to return it as JSON data via an API call later on in this function's code block (see below).  It is also used for filtering purposes when querying data from this database

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of all the campaigns that have been deleted
        """
        params = deleted_campaigns_bignum_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="campaigns_active_inactive_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of active and inactive and completed campaigns(Multiline chart)",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaigns_active_inactive_linechart"
    )
    def active_inactive_linechart(self, request, *args, **kwargs):
        """
        The active_inactive_linechart function returns a line chart of the number of active and inactive campaigns over time.
        The function takes in a request object, which is used to query the CampaignsCampaignvariant table for all campaign variants that are not archived and belong to the current tenant. The queryset is then filtered by date (timestamp) and status (active or inactive). The values() method groups each row by date, while annotate() counts how many rows have an active or inactive status on each day.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The number of active and inactive campaigns on a daily basis
        """
        response = active_inactive_linechart_generic(request)
        return Response(response)

    @extend_schema(
        operation_id="campaign_aggregate_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign aggregate details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_aggregate_details")
    def campaign_aggregate_details(self, request, *args, **kwargs):
        response, _, _ = campaign_aggregate_details_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_aggregate_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign aggregate details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_aggregate_details_export_csv"
    )
    def campaign_aggregate_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = campaign_aggregate_details_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_aggregate_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign aggregate details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_aggregate_details_export_pdf"
    )
    def campaign_aggregate_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = campaign_aggregate_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Campaigns Aggregate Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_types_details",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign types details",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_types_details")
    def campaign_types_details(self, request, *args, **kwargs):
        response, _, _ = campaign_types_details_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_types_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign types details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_types_details_export_csv"
    )
    def campaign_types_details_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = campaign_types_details_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_types_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the campaign types details",
    )
    @action(
        methods=["POST"], detail=False, url_path="campaign_types_details_export_pdf"
    )
    def campaign_types_details_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = campaign_types_details_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Campaign Types Details",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="campaign_sub_targeted_users",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the sub campaign's targeted users",
    )
    @action(methods=["POST"], detail=False, url_path="campaign_sub_targeted_users")
    def sub_campaign_targeted_user(self, request, *args, **kwargs):
        response, _, _ = sub_campaign_targeted_user_generic(request)
        items = return_table(response, request)
        return items

    @extend_schema(
        operation_id="campaign_sub_targeted_users_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the sub campaign's targeted users in csv",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_sub_targeted_users_export_csv",
    )
    def sub_campaign_targeted_user_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = sub_campaign_targeted_user_generic(request)
        items = export_csv(
            response,
            field_names,
            f"{file_name}.csv",
        )
        return items

    @extend_schema(
        operation_id="campaign_sub_targeted_users_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying the sub campaign's targeted users in pdf",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="campaign_sub_targeted_users_export_pdf",
    )
    def sub_campaign_targeted_user_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = sub_campaign_targeted_user_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Targeted Users for Sub-Campaigns",
            request.user.username,
        )
        return items


# --------------------------------OLD campaign views--------------------------------------------------------------
# @extend_schema(
#     operation_id="active_or_inactive",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying pie chart of Active and InActive and completed",
# )
# @action(methods=["POST"], detail=False, url_path="active_or_inactive")
# def active_or_inactive(self, request, *args, **kwargs):
#     """
#     The active_or_inactive function is a custom function that returns the number of active and inactive variants in a campaign.
#     It takes in the request, *args, and **kwargs as parameters. It then uses query to get all CampaignVariants from the database
#     that are not archived (archived=False) and belong to the current tenant (tenant=get_current_tenant_name()). It then annotates each variant with its status label ('active' or 'inactive') using F('status'). The values method is used on this queryset to return only those two labels. Finally, it counts how many variants have each
#
#     :param self: Refer to the object itself
#     :param request: Get the query string from the request
#     :param *args: Pass a non-keyworded variable-length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries
#     """
#     get_qs = query(
#         request,
#         CampaignsCampaignvariant,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     items = (
#         get_qs.filter(archived=False, tenant=get_current_tenant_name())
#         .annotate(label=F("status"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(items)
#
# @extend_schema(
#     operation_id="active_dynamic_notification",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying pie chart of Campaigns which are active_dynamic and active_notification",
# )
# @action(methods=["POST"], detail=False, url_path="active_dynamic_notification")
# def active_dynamic_notification(self, request, *args, **kwargs):
#     """
#     The active_dynamic_notification function is a custom function that returns the number of active dynamic
#      notifications for each content type.
#
#     :param self: Represent the instance of the class
#     :param request: Get the query string from the request object
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries, each dictionary containing the label and count for a given content type
#     """
#     get_qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     items = (
#         get_qs.filter(
#             campaign_variant__status="ACTIVE",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("content_type"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(items)
#
# @extend_schema(
#     operation_id="inactive_dynamic_notification",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying pie chart of Campaigns which are inactive_dynamic and inactive_notification",
# )
# @action(methods=["POST"], detail=False, url_path="inactive_dynamic_notification")
# def inactive_dynamic_notification(self, request, *args, **kwargs):
#     """
#     The inactive_dynamic_notification function returns a list of inactive dynamic notifications.
#
#     :param self: Allow an instance of a class to access its own attributes and methods
#     :param request: Get the request object
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries
#     """
#     get_qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     items = (
#         get_qs.filter(
#             campaign_variant__status="INACTIVE",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("content_type"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(items)
#
# @extend_schema(
#     operation_id="completed_dynamic_notification",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying pie chart of Campaigns which are completed_dynamic and completed_notification",
# )
# @action(methods=["POST"], detail=False, url_path="completed_dynamic_notification")
# def completed_dynamic_notification(self, request, *args, **kwargs):
#     """
#     The completed_dynamic_notification function is a viewset that returns the number of completed dynamic notifications for each content type.
#
#     :param self: Represent the instance of a class
#     :param request: Get the request object
#     :param *args: Pass a non-keyworded, variable-length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries
#     :doc-author: Trelent
#     """
#     get_qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     items = (
#         get_qs.filter(
#             campaign_variant__status="COMPLETED",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("content_type"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(items)
#
# @extend_schema(
#     operation_id="active_dynamic_notification_linechart",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Line chart of Campaigns which are active_dynamic and active_notification",
# )
# @action(
#     methods=["POST"], detail=False, url_path="active_dynamic_notification_linechart"
# )
# def active_dynamic_notification_linechart(self, request, *args, **kwargs):
#     """
#     The active_dynamic_notification_linechart function is a viewset that returns the number of active dynamic and notification campaigns for each day in the past 30 days.
#
#     :param self: Represent the instance of the class
#     :param request: Get the request object
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list
#     :return: The number of active dynamic and notification campaigns for each day
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="ACTIVE",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .values(Date=Cast("timestamp", DateField()))
#         .annotate(
#             Dynamic_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="DYNAMIC")
#             ),
#             Notification_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="NOTIFICATION")
#             ),
#         )
#         .order_by("Date")
#     )
#     return Response(qs1)
#
# @extend_schema(
#     operation_id="inactive_dynamic_notification_linechart",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Line chart of Campaigns which are inactive_dynamic and inactive_notification",
# )
# @action(
#     methods=["POST"],
#     detail=False,
#     url_path="inactive_dynamic_notification_linechart",
# )
# def inactive_dynamic_notification_linechart(self, request, *args, **kwargs):
#     """
#     The inactive_dynamic_notification_linechart function is used to return a list of inactive dynamic and notification campaigns for the last 30 days.
#     The function takes in a request object, which contains information about the current HTTP request being made to this endpoint.
#     It also takes in *args and **kwargs, which are used to pass arbitrary arguments into functions (in this case they are not needed).
#     The function returns an HTTP response containing a list of inactive dynamic and notification campaigns for the last 30 days.
#
#     :param self: Represent the instance of the class
#     :param request: Get the request object
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list
#     :return: A line chart with the number of inactive dynamic and notification campaigns per day
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="INACTIVE",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .values(Date=Cast("timestamp", DateField()))
#         .annotate(
#             Dynamic_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="DYNAMIC")
#             ),
#             Notification_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="NOTIFICATION")
#             ),
#         )
#         .order_by("Date")
#     )
#     return Response(qs1)
#
# @extend_schema(
#     operation_id="completed_dynamic_notification_linechart",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Line chart of Campaigns which are completed_dynamic and completed_notification",
# )
# @action(
#     methods=["POST"],
#     detail=False,
#     url_path="completed_dynamic_notification_linechart",
# )
# def completed_dynamic_notification_linechart(self, request, *args, **kwargs):
#     """
#     The completed_dynamic_notification_linechart function is a viewset that returns the number of completed dynamic and notification campaigns for each day in the past 30 days.
#     The function takes in a request object, which contains information about the HTTP request made to this endpoint.
#     It then queries CampaignsCreativecontent using query() from utils/query_utils.py, filtering by campaign status COMPLETED and archived False, as well as tenant name (from get_current_tenant_name()).
#     It then annotates with values Date=Cast(&quot;timestamp&quot;, DateField()) and Dynamic_Campaigns=Count(&quot;id&quot;, distinct=True, filter=Q
#
#     :param self: Represent the instance of the object itself
#     :param request: Get the request object and pass it to query function
#     :param *args: Pass a non-keyworded, variable-length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A queryset of the number of dynamic and notification campaigns completed on a given date
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="COMPLETED",
#             campaign_variant__archived=False,
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .values(Date=Cast("timestamp", DateField()))
#         .annotate(
#             Dynamic_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="DYNAMIC")
#             ),
#             Notification_Campaigns=Count(
#                 "id", distinct=True, filter=Q(content_type="NOTIFICATION")
#             ),
#         )
#         .order_by("Date")
#     )
#     return Response(qs1)
#
# @extend_schema(
#     operation_id="active_notification_donut",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Donut chart of Campaigns which are active_notification channels",
# )
# @action(methods=["POST"], detail=False, url_path="active_notification_donut")
# def active_notification_donut(self, request, *args, **kwargs):
#     """
#     The active_notification_donut function returns a list of active notification campaigns,
#     grouped by channel. The function is called when the user clicks on the &quot;Active Notification&quot;
#     donut chart in the Campaigns dashboard.
#
#     :param self: Represent the instance of the class
#     :param request: Get the current request, which is used to get the tenant name
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="ACTIVE",
#             campaign_variant__archived=False,
#             content_type="NOTIFICATION",
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("channel"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(qs1)
#
# @extend_schema(
#     operation_id="inactive_notification_donut",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Donut chart of Campaigns which are inactive_notification channels",
# )
# @action(methods=["POST"], detail=False, url_path="inactive_notification_donut")
# def inactive_notification_donut(self, request, *args, **kwargs):
#     """
#     The inactive_notification_donut function returns a list of inactive notification campaigns,
#     grouped by channel. The function is called when the user clicks on the &quot;Inactive Notification&quot;
#     donut chart in the Campaigns dashboard.
#
#     :param self: Represent the instance of a class
#     :param request: Get the request object
#     :param *args: Send a non-keyworded variable length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list to a function
#     :return: A list of dictionaries
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="INACTIVE",
#             campaign_variant__archived=False,
#             content_type="NOTIFICATION",
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("channel"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(qs1)
#
# @extend_schema(
#     operation_id="completed_notification_donut",
#     tags=[AuthTags.AUTHORIZE],
#     description="Used for displaying Donut chart of Campaigns which are completed_notification channels",
# )
# @action(methods=["POST"], detail=False, url_path="completed_notification_donut")
# def completed_notification_donut(self, request, *args, **kwargs):
#     """
#     The completed_notification_donut function returns a list of completed notification campaigns,
#     grouped by channel. The function is called when the user clicks on the &quot;Completed Notification Campaigns&quot;
#     button in the dashboard.
#
#     :param self: Represent the instance of the class
#     :param request: Get the request object
#     :param *args: Pass a non-keyworded, variable-length argument list to the function
#     :param **kwargs: Pass keyworded, variable-length argument list
#     :return: The number of completed notification campaigns by channel
#     """
#     qs = query(
#         request,
#         CampaignsCreativecontent,
#         CampaignVariantSerializer,
#         db_schema="campaign",
#     )
#     qs1 = (
#         qs.filter(
#             campaign_variant__status="COMPLETED",
#             campaign_variant__archived=False,
#             content_type="NOTIFICATION",
#             campaign_variant__tenant=get_current_tenant_name(),
#         )
#         .annotate(label=F("channel"))
#         .values("label")
#         .annotate(count=Count("label"))
#         .order_by("-count")
#     )
#     return Response(qs1)
