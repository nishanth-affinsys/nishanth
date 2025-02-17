from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from client_specific.services.dib import (
    subscription_new_generic,
    subscription_new_details_generic,
    unsubscription_new_generic,
    unsubscription_new_details_generic,
    resubscription_generic,
    resubscription_details_generic,
    subscription_etb_change_generic,
    subscription_etb_change_details,
    net_subscription_generic,
    subscription_messages_wordcloud,
    distinct_open_account_generic,
    distinct_open_account_details,
    subscription_leads_generic,
    subscription_check_status
)
from main.utils.boiler_plate import (
    get_generic_response,
    return_table,
)
from main.utils.export import export_csv, export_pdf


class SubscriptionDashboardViewSet(GenericViewSet):
    """ETB Activities"""

    @extend_schema(
        operation_id="subscription_new_etb",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_new_etb")
    def subscription_new_etb_generic(self, request):
        params = subscription_new_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_new_etb_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_new_etb_details")
    def subscription_new_etb_details_generic(self, request):
        params = subscription_new_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_new_etb_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="subscription_new_etb_details_export_csv",
    )
    def subscription_new_etb_details_export_csv(self, request):
        params = subscription_new_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp"],
                "fileName": "Subscription(new).csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_new_etb_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="subscription_new_etb_details_export_pdf",
    )
    def subscription_new_etb_details_export_pdf(self, request):
        params = subscription_new_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp"],
                "fileName": "Subscription(new).pdf",
                "title": "New ETB Subscription Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="unsubscription_new_etb",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="unsubscription_new_etb")
    def unsubscription_new_etb_generic(self, request):
        params = unsubscription_new_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="unsubscription_new_etb_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="unsubscription_new_etb_details")
    def unsubscription_new_etb_details_generic(self, request):
        params = unsubscription_new_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="unsubscription_new_etb_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="unsubscription_new_etb_details_export_csv",
    )
    def unsubscription_new_etb_details_export_csv(self, request):
        params = unsubscription_new_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp", "Remarks"],
                "fileName": "New Unubscription.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="unsubscription_new_etb_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="unsubscription_new_etb_details_export_pdf",
    )
    def unsubscription_new_etb_details_export_pdf(self, request):
        params = unsubscription_new_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp", "Remarks"],
                "fileName": "New Unubscription.pdf",
                "title": "New ETB Un-subscription details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="resubscription_etb",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="resubscription_etb")
    def resubscription_etb_generic(self, request):
        params = resubscription_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="resubscription_etb_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="resubscription_etb_details")
    def resubscription_etb_details_generic(self, request):
        params = resubscription_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="resubscription_etb_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="resubscription_etb_details_export_csv"
    )
    def resubscription_etb_details_export_csv(self, request):
        params = resubscription_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp"],
                "fileName": "ETB Resubscription Details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="resubscription_etb_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="resubscription_etb_details_export_pdf"
    )
    def resubscription_etb_details_export_pdf(self, request):
        params = resubscription_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp"],
                "fileName": "ETB Resubscription Details.pdf",
                "title": "ETB Resubscription Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_etb_change",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_etb_change")
    def subscription_etb_change_generic(self, request):
        params = subscription_etb_change_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_etb_change_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_etb_change_details")
    def subscription_etb_change_details(self, request):
        params = subscription_etb_change_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_etb_change_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="subscription_etb_change_details_export_csv",
    )
    def subscription_etb_change_details_export_csv(self, request):
        params = subscription_etb_change_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp", "Remarks"],
                "fileName": "ETB Resubscription Details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_etb_change_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="subscription_etb_change_details_export_pdf",
    )
    def subscription_etb_change_details_export_pdf(self, request):
        params = subscription_etb_change_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": ["Channel_id", "Timestamp", "Remarks"],
                "fileName": "ETB Resubscription Details.pdf",
                "title": "ETB Resubscription Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="net_subscription_etb_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="net_subscription_etb_details")
    def net_subscription_etb_details(self, request):
        response, _, _ = net_subscription_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="net_subscription_etb_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="net_subscription_etb_details_export_csv",
    )
    def net_subscription_etb_details_export_csv(self, request):
        response, fieldNames, fileName = net_subscription_generic(request)
        return export_csv(response, fieldNames, fileName)

    @extend_schema(
        operation_id="net_subscription_etb_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="net_subscription_etb_details_export_pdf",
    )
    def net_subscription_etb_details_export_pdf(self, request):
        response, fieldNames, fileName = net_subscription_generic(request)
        return export_pdf(
            response,
            fieldNames,
            fileName,
            "Net Subscription Details",
            request.user.username,
        )

    @extend_schema(
        operation_id="subscription_etb_messages_wordcloud",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="subscription_etb_messages_wordcloud"
    )
    def subscription_etb_messages_wordcloud(self, request):
        response = subscription_messages_wordcloud(request)
        return Response(response)

    @extend_schema(
        operation_id="distinct_open_etb_account",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="distinct_open_etb_account")
    def distinct_open_etb_account(self, request):
        params = distinct_open_account_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="distinct_open_account_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="distinct_open_account_details")
    def distinct_open_account_details(self, request):
        params = distinct_open_account_details(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="distinct_open_account_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="distinct_open_account_details_export_csv",
    )
    def distinct_open_account_details_export_csv(self, request):
        params = distinct_open_account_details(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Timestamp",
                    "Intent",
                    "Customer_type",
                    "Message",
                    "Channel",
                ],
                "fileName": "Distinct Open Registration.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="distinct_open_account_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="distinct_open_account_details_export_pdf",
    )
    def distinct_open_account_details_export_pdf(self, request):
        params = distinct_open_account_details(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Timestamp",
                    "Intent",
                    "Customer_type",
                    "Message",
                    "channel",
                ],
                "fileName": "Distinct Open Registration.pdf",
                "title": "Open Account Intents(Details)",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_leads_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_leads_details")
    def subscription_leads_details(self, request):
        params = subscription_leads_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_leads_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="subscription_leads_details_export_csv"
    )
    def subscription_leads_details_export_csv(self, request):
        params = subscription_new_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Timestamp",
                    "Intent",
                    "Customer_type",
                    "Message",
                ],
                "fileName": "Subscription Leads.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_leads_details_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="subscription_leads_details_export_csv"
    )
    def subscription_leads_details_export_csv(self, request):
        params = subscription_leads_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Timestamp",
                    "Intent",
                    "Customer_type",
                    "Message",
                ],
                "fileName": "Subscription Leads.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_leads_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the comments made by approvers",
    )
    @action(
        methods=["POST"], detail=False, url_path="subscription_leads_details_export_pdf"
    )
    def subscription_leads_details_export_pdf(self, request):
        params = subscription_leads_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Channel_id",
                    "Timestamp",
                    "Intent",
                    "Customer_type",
                    "Message",
                ],
                "fileName": "Subscription Leads.pdf",
                "title": "Subscription Leads",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="subscription_check_status",
        tags=[AuthTags.INTERNAL],
        description="used to check the internal status of a customer",
    )
    @action(methods=["POST"], detail=False, url_path="subscription_check_status")
    def subscription_check_status(self, request):
        response = subscription_check_status(request)
        return Response({"count": response})
