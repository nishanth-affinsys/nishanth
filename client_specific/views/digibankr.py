from auth.tags import AuthTags
from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from client_specific.services.digibankr import (
    stock_management_details_generic,
    card_management_details_generic,
    card_management_count,
    stock_management_count,
)

from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf
from main.utils.boiler_plate import get_generic_response


class StockManagementViewSet(GenericViewSet):

    @extend_schema(
        operation_id="digibankr_stock_management_count",
        tags=[AuthTags.AUTHORIZE],
        description="count the number of linked cards.",
    )
    @action(methods=["POST"], detail=False, url_path="digibankr_stock_management_count")
    def digibankr_card_count(self, request):
        """
        this endpoint is used to display the count of linked cards.
        """
        params = stock_management_count(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_stock_management_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the stock management details",
    )
    @action(
        methods=["POST"], detail=False, url_path="digibankr_stock_management_details"
    )
    def stock_management_details(self, request):
        """
        This endpoint is used to show the details for the stock management inventory.
        """
        params = stock_management_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_stock_management_details_export",
        tags=[AuthTags.AUTHORIZE],
        description="export the stock management details in csv format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="digibankr_stock_management_details_export",
    )
    def digibankr_stock_management_details_export(self, request):
        params = stock_management_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Accessory_Ref_number",
                    "Location",
                    "Account_Number",
                    "Customer_Name",
                    "Mobile_No",
                    "Card_Reference_Number",
                    "Created_By",
                    "Timestamp",
                ],
                "fileName": "stock_management_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_stock_management_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="export the stock management details in pdf format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="digibankr_stock_management_details_export_pdf",
    )
    def digibankr_stock_management_details_export_pdf(self, request):
        params = stock_management_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Accessory_Ref_number",
                    "Location",
                    "Account_Number",
                    "Customer_Name",
                    "Mobile_No",
                    "Card_Reference_Number",
                    "Created_By",
                    "Timestamp",
                ],
                "fileName": "stock_management_details.pdf",
                "title": "Stock Management Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)


class CardManagementViewSet(GenericViewSet):

    @extend_schema(
        operation_id="digibankr_card_count",
        tags=[AuthTags.AUTHORIZE],
        description="count the number of linked cards.",
    )
    @action(methods=["POST"], detail=False, url_path="digibankr_card_count")
    def digibankr_card_count(self, request):
        """
        this endpoint is used to display the count of linked cards.
        """
        params = card_management_count(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_card_management_details",
        tags=[AuthTags.AUTHORIZE],
        description="used to show the stock management details",
    )
    @action(
        methods=["POST"], detail=False, url_path="digibankr_card_management_details"
    )
    def card_management_details(self, request):
        """
        This endpoint is used to show the details for the stock management inventory.
        """
        params = card_management_details_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_card_management_details_export",
        tags=[AuthTags.AUTHORIZE],
        description="export the stock management details in csv format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="digibankr_card_management_details_export",
    )
    def digibankr_card_management_details_export(self, request):
        params = card_management_details_generic(
            request,
            key="csv_kwargs",
            value={
                "fieldNames": [
                    "Inventory_reference_number",
                    "Uploaded_By",
                    "Uploaded_Timestamp",
                ],
                "fileName": "card_management_details.csv",
            },
        )
        return get_generic_response(params)

    @extend_schema(
        operation_id="digibankr_card_management_details_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="export the stock management details in pdf format",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="digibankr_card_management_details_export_pdf",
    )
    def digibankr_card_management_details_export_pdf(self, request):
        params = card_management_details_generic(
            request,
            key="pdf_kwargs",
            value={
                "fieldNames": [
                    "Inventory_reference_number",
                    "Uploaded_By",
                    "Uploaded_Timestamp",
                ],
                "fileName": "card_management_details.pdf",
                "title": "Card Management Details",
                "user": request.user.username,
            },
        )
        return get_generic_response(params)
