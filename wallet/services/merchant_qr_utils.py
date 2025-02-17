from django.db.models import (
    Q,
    Case,
    When,
    F,
    Count,
    FloatField,
    IntegerField,
    Avg,
    Func,
    DateTimeField,
    Value,
    CharField,
)
from django.db.models.functions import Cast, Trunc, TruncDate

from main.tenant_middleware import get_current_tenant_name, get_timezone
from main.utils.boiler_plate import query
from wallet.models import AccountingMerchant, QrWallet
from wallet.serializers import AccMerchantSerializer, QrWalletSerializer
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def get_all_nodes(request):
    allowed_nodes = list(
        filter(None, request.headers.get("Bb-Allowed-Nodes", "").split(","))
    )
    logged_user_id = request.user.user_id
    if not allowed_nodes:
        return logged_user_id
    else:
        return allowed_nodes


def get_allowed_merchant(request):
    """if the merchant is standalone then getting the receiver id and filter by it
    and if the merchant is associated with hierarchy then node id is used"""
    dynamic_db_connection("analytics")
    qs = query(
        request,
        AccountingMerchant,
        AccMerchantSerializer,
        db_schema=get_db_name("analytics"),
    )
    all_nodes = get_all_nodes(request)
    filters = {"tenant": get_current_tenant_name()}  # "receiver_provider": "merchants"}
    if isinstance(all_nodes, list) and all_nodes:
        filters["node_id__in"] = all_nodes
    else:
        filters["receiver_id"] = all_nodes

    qs1 = qs.filter(**filters)
    return qs1


def get_allowed_merchant_qr(request):
    dynamic_db_connection("analytics")
    qs = query(
        request,
        QrWallet,
        QrWalletSerializer,
        db_schema=get_db_name("analytics"),
    )
    all_users = get_all_nodes(request)
    filters = {"tenant": get_current_tenant_name(), "provider": "merchants"}
    if isinstance(all_users, list) and all_users:
        filters["node_id__in"] = all_users
    else:
        filters["receiver_id"] = all_users
    qs = qs.filter(**filters)
    return qs


def total_merchant_qr_scanned_bigno_generic(request):
    qs = get_allowed_merchant_qr(request).filter(behaviour="scan").count()
    return qs


def total_merchant_qr_type_scanned_bigno_generic(request, qr_type):
    qs = (
        get_allowed_merchant_qr(request)
        .filter(behaviour="scan", qr_type=qr_type)
        .distinct("id")
        .count()
    )
    return qs


# only dynamic QRS can be generated
def merchant_qr_created_generic(request):
    qs = (
        get_allowed_merchant_qr(request)
        .filter(
            behaviour="create",
        )
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            static=Count(
                "qr_uuid",
                distinct=True,
                filter=Q(qr_type="static"),
            ),
            dynamic=Count(
                "qr_uuid",
                distinct=True,
                filter=Q(qr_type="dynamic"),
            ),
        )
    )
    return qs


def merchant_qr_scanned_vs_successful_generic(request):
    qs = (
        get_allowed_merchant_qr(request)
        .filter(behaviour="scan")
        .values("qr_type")
        .annotate(
            success=Count(
                Case(
                    When(status="Success", then=1),
                    default=None,
                    output_field=IntegerField(),
                )
            ),
            failed=Count(
                Case(
                    When(status="Failed", then=1),
                    default=None,
                    output_field=IntegerField(),
                )
            ),
        )
    )

    return qs


def merchant_revenue_by_qr_type_generic(request, aggregation_function):
    qs = (
        get_allowed_merchant(request)
        .filter(
            source="W",
            qr_id__isnull=False,
            qr_type__in=["static", "dynamic"],
            transaction_status="S",
            transaction_type="QR Payment",
        )
        .values(label=F("qr_type"))
        .annotate(
            count=aggregation_function(
                Cast(
                    "transaction_amount", output_field=FloatField()
                ),  # count is the revenue
            )
        )
    )
    return qs


def merchant_transaction_details_by_qr(request):
    qs = (
        get_allowed_merchant(request)
        .filter(
            source="W",
            qr_id__isnull=False,
            transaction_type="QR Payment",
        )
        .values(
            "transaction_id",
            "qr_type",
            "currency",
            "transaction_amount",
            "transaction_remarks",
            "sender_name",
            "source",
            "transaction_status"
        )
        .annotate(
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .distinct("transaction_id")
    )
    ordered_qs = sorted(qs, key=lambda x: x["Timestamp"], reverse=True)
    return (
        ordered_qs,
        [
            "transaction_id",
            "qr_type",
            "currency",
            "transaction_amount",
            "transaction_remarks",
            "sender_name",
            "source",
            "Timestamp",
            "Transaction_status"
        ],
        "transaction_details",
    )
