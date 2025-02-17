from auth.tags import AuthTags
from django.db.models import F, Case, When, Q
from django.db.models import Count, DateField
from django.db.models.functions import Extract, Cast, Trunc
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from main.tenant_middleware import get_current_tenant_name
from campaign_manager.models import CampaignsCampaignvariant, CampaignsCreativecontent
from campaign_manager.serializers import CampaignVariantSerializer
from main.utils.boiler_plate import query, get_generic_response


# OLD CAMPAIGN VIEWS
class CamapignTypeViewSet(GenericViewSet):
    @extend_schema(
        operation_id="user_specific_campaigns_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display User Specific campaign Variants in the given Timestamp",
    )
    @action(methods=["POST"], detail=False, url_path="user_specific_campaigns_bigNum")
    def user_specific_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The user_specific_campaigns_bigNum function returns a list of all user-specific campaigns that have been created by the current tenant.
        The function is called when the /campaigns/user_specific_campaigns endpoint is hit with a GET request.
        The function uses get_generic_response to return data from the CampaignsCampaignvariant model, which contains information about each campaign variant in our database.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of user-specific campaigns in the database
        """
        params = {
            "request": request,
            "models": CampaignsCampaignvariant,
            "serializers": CampaignVariantSerializer,
            "db_schema": "campaign",
            "filter_kwargs": {
                "type": "USER_SPECIFIC",
                "archived": False,
                "tenant": get_current_tenant_name(),
            },
            "values_kwargs": {"Date": Cast("timestamp", DateField())},
            "annotate": {"count": Count("identifier", distinct=True)},
            "order_by": ["-Date"],
            "not_paginated": True,
        }
        return get_generic_response(params)

    @extend_schema(
        operation_id="product_specific_campaigns_bigNum",
        tags=[AuthTags.AUTHORIZE],
        description="Used for display Product Specific campaign Variants in the given Timestamp",
    )
    @action(
        methods=["POST"], detail=False, url_path="product_specific_campaigns_bigNum"
    )
    def product_specific_campaigns_bigNum(self, request, *args, **kwargs):
        """
        The product_specific_campaigns_bigNum function is used to get the number of product specific campaigns that have been created in a given time period.
        The function takes in a request object and returns an array of objects containing the date, count, and tenant name for each day within the specified time range.


        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of all the product specific campaigns that have been created in a particular tenant
        """
        params = {
            "request": request,
            "models": CampaignsCampaignvariant,
            "serializers": CampaignVariantSerializer,
            "db_schema": "campaign",
            "filter_kwargs": {
                "type": "PRODUCT_SPECIFIC",
                "archived": False,
                "tenant": get_current_tenant_name(),
            },
            "values_kwargs": {"Date": Cast("timestamp", DateField())},
            "annotate": {"count": Count("identifier", distinct=True)},
            "order_by": ["-Date"],
            "not_paginated": True,
        }
        return get_generic_response(params)

    @extend_schema(
        operation_id="user_product_specific_campaigns",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying graph of Product and user Specific Customers Line chart",
    )
    @action(methods=["POST"], detail=False, url_path="user_product_specific_campaigns")
    def user_product_specific_campaigns(self, request, *args, **kwargs):
        """
        The user_product_specific_campaigns function returns a list of the number of user-specific and product-specific campaigns
            that were created on each day.

        :param self: Bind the method to an object
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        qs = query(
            request,
            CampaignsCampaignvariant,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(archived=False, tenant=get_current_tenant_name())
            .values(Date=Cast("timestamp", DateField()))
            .annotate(
                User_Specific_Campaigns=Count(
                    "identifier", distinct=True, filter=Q(type="USER_SPECIFIC")
                ),
                Product_Specific_Campaigns=Count(
                    "identifier", distinct=True, filter=Q(type="PRODUCT_SPECIFIC")
                ),
            )
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="user_specific_dynamic_notification",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying pie chart of Campaigns which are user_specific_dynamic and user_specific_notification",
    )
    @action(
        methods=["POST"], detail=False, url_path="user_specific_dynamic_notification"
    )
    def user_specific_dynamic_notification(self, request, *args, **kwargs):
        """
        The user_specific_dynamic_notification function is used to get the count of user specific dynamic notifications.
            It takes in a request and returns a response with the count of user specific dynamic notifications.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries
        """
        get_qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        items = (
            get_qs.filter(
                campaign_variant__type="USER_SPECIFIC",
                campaign_variant__archived=False,
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .annotate(label=F("content_type"))
            .values("label")
            .annotate(count=Count("label"))
            .order_by("-count")
        )
        return Response(items)

    @extend_schema(
        operation_id="product_specific_dynamic_notification",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying pie chart of Campaigns which are product_specific_dynamic and product_specific_notification",
    )
    @action(
        methods=["POST"], detail=False, url_path="product_specific_dynamic_notification"
    )
    def product_specific_dynamic_notification(self, request, *args, **kwargs):
        """
        The product_specific_dynamic_notification function is a viewset that returns the number of product specific dynamic notifications for each content type.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of objects
        """
        get_qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        items = (
            get_qs.filter(
                campaign_variant__type="PRODUCT_SPECIFIC",
                campaign_variant__archived=False,
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .annotate(label=F("content_type"))
            .values("label")
            .annotate(count=Count("label"))
            .order_by("-count")
        )
        return Response(items)

    @extend_schema(
        operation_id="user_specific_dynamic_lineChart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Line chart of Campaigns which are user_specific_dynamic",
    )
    @action(methods=["POST"], detail=False, url_path="user_specific_dynamic_lineChart")
    def user_specific_dynamic_lineChart(self, request, *args, **kwargs):
        """
        The user_specific_dynamic_lineChart function is used to return a list of all user_specific dynamic campaigns
            that have been created by the current tenant. The function returns a list of dictionaries, each dictionary containing
            the date and number of user_specific dynamic campaigns created on that day.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The count of user_specific dynamic campaigns for each day
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="USER_SPECIFIC",
                campaign_variant__archived=False,
                content_type="DYNAMIC",
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .values(Date=Cast("timestamp", DateField()))
            .annotate(Dynamic_Campaigns=Count("id", distinct=True))
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="product_specific_dynamic_lineChart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Line chart of Campaigns which are product_specific_dynamic",
    )
    @action(
        methods=["POST"], detail=False, url_path="product_specific_dynamic_lineChart"
    )
    def product_specific_dynamic_lineChart(self, request, *args, **kwargs):
        """
        The product_specific_dynamic_lineChart function is used to return a list of all the product specific dynamic campaigns that have been created in the last 30 days.
        The function takes in a request object and returns a response object containing data about all product specific dynamic campaigns created within the last 30 days.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of product specific dynamic campaigns created on a particular date
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="PRODUCT_SPECIFIC",
                campaign_variant__archived=False,
                content_type="DYNAMIC",
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .values(Date=Cast("timestamp", DateField()))
            .annotate(Dynamic_Campaigns=Count("id", distinct=True))
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="user_specific_dynamic_notification_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Line chart of Campaigns which are product_specific_dynamic",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="user_specific_dynamic_notification_linechart",
    )
    def user_specific_dynamic_notification_linechart(self, request, *args, **kwargs):
        """
        The user_specific_dynamic_notification_linechart function is used to return a list of all user specific dynamic and notification campaigns,
            grouped by date. The function takes in the request object as an argument, and returns a response containing the queryset.

        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The count of dynamic and notification campaigns
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="USER_SPECIFIC",
                campaign_variant__archived=False,
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .values(Date=Cast("timestamp", DateField()))
            .annotate(
                Dynamic_Campaigns=Count(
                    "id", distinct=True, filter=Q(content_type="DYNAMIC")
                ),
                Notification_Campaigns=Count(
                    "id", distinct=True, filter=Q(content_type="NOTIFICATION")
                ),
            )
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="product_specific_dynamic_notification_linechart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Line chart of Campaigns which are product_specific_dynamic",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="product_specific_dynamic_notification_linechart",
    )
    def product_specific_dynamic_notification_linechart(self, request, *args, **kwargs):
        """
        The product_specific_dynamic_notification_linechart function is used to return a list of all product specific campaigns,
            dynamic campaigns and notification campaigns for the current tenant. The data returned by this function is used in the
            Product Specific Dynamic Notification Linechart on the Campaigns page.

        :param self: Represent the instance of the class
        :param request: Pass the request object to the view
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: A list of dictionaries
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="PRODUCT_SPECIFIC",
                campaign_variant__archived=False,
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .values(Date=Cast("timestamp", DateField()))
            .annotate(
                Dynamic_Campaigns=Count(
                    "id", distinct=True, filter=Q(content_type="DYNAMIC")
                ),
                Notification_Campaigns=Count(
                    "id", distinct=True, filter=Q(content_type="NOTIFICATION")
                ),
            )
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="product_specific_notification_lineChart",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Line chart of Campaigns which are product_specific_notification",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="product_specific_notification_lineChart",
    )
    def product_specific_notification_lineChart(self, request, *args, **kwargs):
        """
        The product_specific_notification_lineChart function returns a list of all the product specific notification campaigns that have been created in the last 30 days.
        The function takes in a request object and returns a response object containing data about each campaign.


        :param self: Represent the instance of the class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list
        :return: The number of product specific notification campaigns created on a particular date
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="PRODUCT_SPECIFIC",
                campaign_variant__archived=False,
                content_type="NOTIFICATION",
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .values(Date=Cast("timestamp", DateField()))
            .annotate(Notification_Campaigns=Count("id", distinct=True))
            .order_by("Date")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="user_specific_notification_donut",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Donut chart of Campaigns which are user_specific_notification channels",
    )
    @action(methods=["POST"], detail=False, url_path="user_specific_notification_donut")
    def user_specific_notification_donut(self, request, *args, **kwargs):
        """
        The user_specific_notification_donut function returns a list of all user-specific notification campaigns,
        grouped by channel. The function is called when the /campaigns/user_specific_notification_donut endpoint is hit.

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A list of dictionaries with the following structure:
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="USER_SPECIFIC",
                campaign_variant__archived=False,
                content_type="NOTIFICATION",
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .annotate(label=F("channel"))
            .values("label")
            .annotate(count=Count("label"))
            .order_by("-count")
        )
        return Response(qs1)

    @extend_schema(
        operation_id="product_specific_notification_donut",
        tags=[AuthTags.AUTHORIZE],
        description="Used for displaying Donut chart of Campaigns which are product_specific_notification channels",
    )
    @action(
        methods=["POST"], detail=False, url_path="product_specific_notification_donut"
    )
    def product_specific_notification_donut(self, request, *args, **kwargs):
        """
        The product_specific_notification_donut function returns a list of all product specific notification channels,
            and the number of times each channel has been used. This is done by querying the CampaignsCreativecontent table
            for all rows where campaign_variant__type = &quot;PRODUCT_SPECIFIC&quot;, campaign_variant__archived = False, content_type = "NOTIFICATION&quot",
            and campaign_variant__tenant matches the current tenant name. The query then annotates each row with a label equal to its channel value,
            groups these rows by their labels (channels), counts how many rows are in

        :param self: Represent the instance of a class
        :param request: Get the request object
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: The product specific notification donut
        """
        qs = query(
            request,
            CampaignsCreativecontent,
            CampaignVariantSerializer,
            db_schema="campaign",
        )
        qs1 = (
            qs.filter(
                campaign_variant__type="PRODUCT_SPECIFIC",
                campaign_variant__archived=False,
                content_type="NOTIFICATION",
                campaign_variant__tenant=get_current_tenant_name(),
            )
            .annotate(label=F("channel"))
            .values("label")
            .annotate(count=Count("label"))
            .order_by("-count")
        )
        return Response(qs1)


# END OF OLD CAMPAIGN VIEWS
