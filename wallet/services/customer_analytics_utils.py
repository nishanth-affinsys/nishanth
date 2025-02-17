from __future__ import annotations
from django.db.models import (
    Sum,
    FloatField,
    Count,
    Q,
    Case,
    When,
)
from django.db.models.functions import Cast, TruncDate
from main.settings import PAYMENT_CATEGORY_QR
from main.tenant_middleware import get_timezone, get_current_tenant_name
from main.utils.boiler_plate import query
from wallet.models import TransactionsTransaction, TransactionsTransactionuser
from wallet.serializers import TransactionSerializer


def total_money_sent_cust(request, provider, user_id):
    ids_list = (
        TransactionsTransactionuser.objects.using("transaction").filter(
            user_id=user_id, provider=provider, tenant=get_current_tenant_name()
        )
    ).values_list("id")
    qs = query(
        request, TransactionsTransaction, TransactionSerializer, db_schema="transaction"
    )
    qs1 = (
        qs.filter(
            initiator__in=ids_list,
            status="S",
        )
        .exclude(receiver__in=ids_list)
        .aggregate(total_sum=Sum(Cast("amount", output_field=FloatField())))
    )
    total_sum = qs1["total_sum"] if qs1["total_sum"] is not None else 0
    return total_sum


def total_money_received_cust(request, provider, user_id):
    ids_list = (
        TransactionsTransactionuser.objects.using("transaction").filter(
            user_id=user_id, provider=provider, tenant=get_current_tenant_name()
        )
    ).values_list("id")
    qs = query(
        request,
        TransactionsTransaction,
        TransactionSerializer,
        db_schema="transaction",
    )
    qs1 = (
        qs.filter(
            receiver__in=ids_list,
            status="S",
        )
        .exclude(initiator__in=ids_list)
        .aggregate(total_sum=Sum(Cast("amount", output_field=FloatField())))
    )

    total_sum = qs1["total_sum"] if qs1["total_sum"] is not None else 0
    return total_sum


def transaction_status_linechart_cust(request, provider, user_id):
    qs = query(
        request,
        TransactionsTransaction,
        TransactionSerializer,
        db_schema="transaction",
    )
    qs1 = (
        qs.filter(
            initiator_id__provider=provider,
            initiator_id__user_id=user_id,
            tenant=get_current_tenant_name(),
        )
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            Initiated=Count("uuid", filter=Q(status="I")),
            Inprogress=Count("uuid", filter=Q(status="P")),
            Successful=Count("uuid", filter=Q(status="S")),
            Failed=Count("uuid", filter=Q(status="F")),
            Abandoned=Count("uuid", filter=Q(status="A"))
        )
        .order_by("Date")
    )
    return qs1


def income_vs_expenses_cust(request, provider, user_id):
    ids_list = (
        TransactionsTransactionuser.objects.using("transaction").filter(
            user_id=user_id,
            provider=provider,
        )
    ).values_list("id")

    qs = query(
        request,
        TransactionsTransaction,
        TransactionSerializer,
        db_schema="transaction",
    )
    qs1 = (
        qs.filter(
            status="S",
            tenant=get_current_tenant_name(),
        )
        .values(Date=TruncDate("timestamp", tzinfo=get_timezone()))
        .annotate(
            income=Sum(
                Cast("amount", output_field=FloatField()),
                filter=Q(receiver_id__in=ids_list) & ~Q(initiator_id__in=ids_list),
            ),
            expenses=Sum(
                Cast("amount", output_field=FloatField()),
                filter=Q(initiator_id__in=ids_list) & ~Q(receiver_id__in=ids_list),
            ),
        )
        .order_by("Date")
    )
    result = []
    for item in qs1:
        income = item["income"] if item["income"] is not None else 0
        expenses = abs(item["expenses"]) if item["expenses"] is not None else 0
        if income != 0 or expenses != 0:
            result.append(
                {"Date": item["Date"], "income": income, "expenses": expenses}
            )
    return result


def spent_received_qr_payments_cust(request, provider, user_id):
    ids_list = (
        TransactionsTransactionuser.objects.using("transaction").filter(
            user_id=user_id, provider=provider, tenant=get_current_tenant_name()
        )
    ).values_list("id")
    qs = query(
        request,
        TransactionsTransaction,
        TransactionSerializer,
        db_schema="transaction",
    )
    received_amount = (
        qs.filter(
            receiver_id__in=ids_list,
            status='S',
            transaction_definition__code__in=["QRPAY", "QRREFR"]
        )
        .exclude(
            initiator_id__in=ids_list,
        )
        .aggregate(
            received=Sum(
                Case(
                    When(
                        receiver_id__user_id=int(user_id),
                        then=Cast("amount", output_field=FloatField()),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
        )["received"]
    )
    sent_amount = (
        qs.filter(
            initiator_id__in=ids_list,
            initiator_id__provider=provider,
            status='S',
            transaction_definition__code__in=["QRPAY", "QRREFR"],
        )
        .exclude(
            receiver_id__in=ids_list,
        )
        .aggregate(
            sent=Sum(
                Case(
                    When(
                        initiator_id__user_id=int(user_id),
                        then=Cast("amount", output_field=FloatField()),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
        )["sent"]
    )
    payload = [
        {
            "label": "received",
            "count": received_amount or 0,
        },
        {
            "label": "sent",
            "count": sent_amount or 0,
        },
    ]

    return payload


def money_spent_categories(request, provider, user_id):
    ids_list = (
        TransactionsTransactionuser.objects.using("transaction").filter(
            user_id=user_id, provider=provider, tenant=get_current_tenant_name()
        )
    ).values_list("id")
    qs = query(
        request,
        TransactionsTransaction,
        TransactionSerializer,
        db_schema="transaction",
    )
    categories_data = (
        qs.filter(
            initiator_id__provider=provider,
            initiator_id__in=ids_list,
            status="S",
            tenant=get_current_tenant_name(),
        )
        .exclude(
            receiver_id__in=ids_list
        )
        .values("transaction_definition__category__name")
        .annotate(amount=Sum(Cast("amount", output_field=FloatField())))
    )
    items = [
        {
            "count": item["amount"] if item["amount"] is not None else 0,
            "label": item["transaction_definition__category__name"],
        }
        for item in categories_data
    ]
    return items
