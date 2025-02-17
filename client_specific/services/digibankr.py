from client_specific.models import InventoryManagement, AccessoryMaster
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from client_specific.serializers import (
    AccessoryMasterSerializer,
    InventoryManagementSerializer,
)
from django.db.models import F
from console.services.api_logs_utils import add_args


def stock_management_count(request):
    dynamic_db_connection("accessory")
    params = {
        "request": request,
        "models": AccessoryMaster,
        "serializers": AccessoryMasterSerializer,
        "db_schema": get_db_name("accessory"),
        "filter_kwargs": {"current_event": "link_success"},
        "count": True,
    }
    return params


def stock_management_details_generic(request, key=None, value=None):
    dynamic_db_connection("accessory")
    params = {
        "request": request,
        "models": AccessoryMaster,
        "serializers": AccessoryMasterSerializer,
        "db_schema": get_db_name("accessory"),
        "filter_kwargs": {"current_event": "link_success"},
        "values_kwargs": {
            "Accessory_Ref_number": F("accessory_ref_number"),
            "Location": F("branch_code"),
            "Account_Number": F("account_number"),
            "Customer_Name": F("customer_name"),
            "Mobile_No": F("mobile_no"),
            "Card_Reference_Number": F("accessory_input_value"),
            "Created_By": F("created_by"),
            "Timestamp": F("create_timestamp"),
        },
    }
    return add_args(params, key, value)


def card_management_count(request):
    dynamic_db_connection("accessory")
    params = {
        "request": request,
        "models": InventoryManagement,
        "serializers": InventoryManagementSerializer,
        "db_schema": get_db_name("accessory"),
        "filter_kwargs": {"active": "Y"},
        "count": True,
    }
    return params


def card_management_details_generic(request, key=None, value=None):
    dynamic_db_connection("accessory")
    params = {
        "request": request,
        "models": InventoryManagement,
        "serializers": InventoryManagementSerializer,
        "db_schema": get_db_name("accessory"),
        "filter_kwargs": {"active": "Y"},
        "values_kwargs": {
            "Inventory_reference_number": F("inventory_reference_number"),
            "Uploaded_By": F("uploaded_by"),
            "Uploaded_Timestamp": F("uploaded_timestamp"),
        },
    }
    return add_args(params, key, value)
