from django.db.models import (
    Sum,
    Max,
    Count,
    F,
    FloatField,
    Q,
    Value,
    Window,
    CharField,
    When,
    Case,
)
from django.db.models.functions import Cast, Trunc, TruncDate, Coalesce, RowNumber

from datetime import timedelta, datetime
from main.settings import get_int_env_value
from main.tenant_middleware import get_timezone
from main.utils.dynamic_db import dynamic_db_connection, get_db_name
from wallet.models import MerchantHierarchy
from wallet.services.merchant_qr_utils import (
    get_allowed_merchant,
)


def add_row_numbers_for_transactions(request):
    qs = (
        get_allowed_merchant(request)
        .annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=["transaction_id"],
                order_by=["-id"],
            )
        )
        .filter(row_number=1)
        .values()
    )
    return qs


def merchant_transactions_bigno_generic(request, transaction_status):
    abandoned_interval = get_int_env_value("TRANSACTION_ABANDON_TIMEOUT")
    now = datetime.now(get_timezone())
    data = add_row_numbers_for_transactions(request)
    if transaction_status in ["S", "F","A"]:
        has_desired_status = (
            lambda row: row.get("transaction_status", "") == transaction_status
        )
    elif transaction_status in ["I", "P"]:
        has_desired_status = (
            lambda row: row.get("transaction_status", "") == transaction_status
                        and row.get("timestamp") + timedelta(seconds=abandoned_interval) > now
        )
    else:
        has_desired_status = (
            lambda row: row.get("transaction_status", "") in ["I", "P"]
                        and row.get("timestamp") + timedelta(seconds=abandoned_interval) <= now
        )
    response = filter(has_desired_status, data)
    count = len(list(response))
    return {"count": count}


def merchant_trans_initiated_bigno_generic(request):
    qs = (
        get_allowed_merchant(request)
        .filter(transaction_status="I")
        .values("transaction_id")
        .distinct()
        .count()
    )
    return {"count": qs}


def merchant_revenue_earned_bigno_generic(request, aggregate_func):
    qs = (
        get_allowed_merchant(request)
        .filter(transaction_status="S")
        .aggregate(
            count=aggregate_func(
                Cast("transaction_amount", output_field=FloatField()),
            )
        )
    )
    return qs


def merchant_max_revenue_earned_generic(request):
    qs = (
        get_allowed_merchant(request)
        .filter(transaction_status="S")
        .values("transaction_id", "sender_name", "product_name")
        .annotate(
            revenue=Max(
                Cast("transaction_amount", output_field=FloatField()),
            ),
            Receiver_name=F("receiver_name"),
            Source=F("source"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("-Timestamp")
    )
    return (
        qs,
        [
            "transaction_id",
            "sender_name",
            "product_name",
            "revenue",
            "Receiver_name",
            "Source",
            "Timestamp",
        ],
        "Max Revenue details",
    )


def merchant_transaction_trend_by_day_generic(request):
    qs = (
        get_allowed_merchant(request)
        .values(
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(
            bank_transactions=Count(
                "transaction_id",
                distinct=True,
                filter=(Q(source="A")),
            ),
            wallet_transactions=Count(
                "transaction_id",
                distinct=True,
                filter=(Q(source="W")),
            ),
        )
        .order_by("-Date")
    )
    return qs


def merchant_revenue_trend_by_day_generic(request):
    qs = (
        get_allowed_merchant(request)
        .filter(transaction_status="S")
        .values(
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(
            bank_transactions=Coalesce(
                Sum(
                    Cast("transaction_amount", FloatField()),
                    filter=(Q(source="A")),
                ),
                Value(0.0),
            ),
            wallet_transactions=Coalesce(
                Sum(
                    Cast("transaction_amount", FloatField()),
                    filter=(Q(source="W")),
                ),
                Value(0.0),
            ),
        )
        .order_by("-Date")
    )
    return qs


def merchant_transaction_history(request):
    abandoned_interval = get_int_env_value("TRANSACTION_ABANDON_TIMEOUT")
    now = datetime.now(get_timezone())
    qs = (
        add_row_numbers_for_transactions(request)
        .values(
            "transaction_id",
            "currency",
            "transaction_amount",
            "transaction_status",
            "transaction_remarks",
            "sender_name",
            "sender_acc_number",
            "qr_id",
            "qr_type",
            "qr_description",
            "transaction_type",
            "node_name",
            "source",
            "receiver_acc_number",
            "receiver_name",
        )
        .annotate(Abandond_Time=F("timestamp") + timedelta(seconds=abandoned_interval))
        .annotate(
            Transaction_status=Case(
                When(transaction_status="S", then=Value("Success")),
                When(
                    transaction_status="I",
                    Abandond_Time__gt=now,
                    then=Value("Initiated"),
                ),
                When(transaction_status="F", then=Value("Failed")),
                When(
                    transaction_status="P",
                    Abandond_Time__gt=now,
                    then=Value("In progress"),
                ),
                When(
                    transaction_status="A",
                    then=Value("Abandoned")
                ),
                When(
                    transaction_status__in=["I", "P"],
                    Abandond_Time__lte=now,
                    then=Value("Abandoned"),
                ),
                output_field=CharField(),
            ),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .values(
            "transaction_id",
            "currency",
            "transaction_type",
            "transaction_amount",
            "transaction_remarks",
            "Transaction_status",
            "qr_id",
            "qr_type",
            "qr_description",
            "source",
            "sender_name",
            "sender_acc_number",
            "receiver_name",
            "receiver_acc_number",
            "node_name",
            "Timestamp",
        )
        .distinct("transaction_id")
    )
    ordered_qs = sorted(qs, key=lambda x: x["Timestamp"], reverse=True)
    return (
        ordered_qs,
        [
            "transaction_id",
            "currency",
            "transaction_type",
            "transaction_amount",
            "transaction_remarks",
            "Transaction_status",
            "qr_id",
            "qr_type",
            "qr_description",
            "source",
            "sender_name",
            "sender_acc_number",
            "receiver_name",
            "receiver_acc_number",
            "node_name",
            "Timestamp",
        ],
        "transaction_details",
    )


def generate_hierarchy(node_id, filtered_data, key):
    node = {"name": "", "value": 0, "children": []}
    dynamic_db_connection("analytics")
    current_node = MerchantHierarchy.objects.using(get_db_name("analytics")).get(node_id=node_id)

    node["name"] = current_node.node_name
    node["value"] = 0

    node_data = filtered_data.filter(node_id=node_id)

    if key == "revenue":
        total_amount = node_data.aggregate(
            total_amount=Sum(Cast("transaction_amount", FloatField()))
        )["total_amount"]
        if total_amount:
            node["value"] += total_amount  # Adding the revenue amount to the node value
    elif key == "transactions":
        transaction_count = node_data.aggregate(
            transaction_count=Count("transaction_id")
        )["transaction_count"]
        if transaction_count:
            node[
                "value"
            ] += transaction_count  # Adding the transaction count to the node value

    child_nodes = MerchantHierarchy.objects.using(get_db_name("analytics")).filter(
        node_id__in=current_node.node_id_of_children
    )

    for child_node in child_nodes:
        child_hierarchy = generate_hierarchy(child_node.node_id, filtered_data, key)
        if child_hierarchy:
            node["children"].append(child_hierarchy)
            node["value"] += child_hierarchy["value"]  # add child values to parent

    return node


def merchant_revenue_hierarchy_sunburst_generic(request, key):
    filtered_data = get_allowed_merchant(request).filter(transaction_status="S")
    payload = {}
    if filtered_data:
        root_node_id = request.headers.get("Bb-Node-Id")
        if root_node_id:
            hierarchy = generate_hierarchy(root_node_id, filtered_data, key)
            level = calculate_hierarchy_level(hierarchy)
            payload = {"level": level, "value": [hierarchy]}
        else:
            # Return an empty hierarchy if root_node_id is empty(standalone merchant)
            payload = {"level": 0, "value": []}
    return payload


def calculate_hierarchy_level(node):
    if not node.get("name"):
        return 0
    if not node["children"]:
        return 1
    max_child_level = 0
    for child in node["children"]:
        child_level = calculate_hierarchy_level(child) + 1
        max_child_level = max(max_child_level, child_level)
    return max_child_level
