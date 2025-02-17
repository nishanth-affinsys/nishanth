from django.db.models import (
    Count,
    FloatField,
    Avg,
    DateField,
    Sum,
    F,
)
from django.db.models.functions import Cast, ExtractHour, TruncDate, Trunc

from main.tenant_middleware import get_timezone
from wallet.services.merchant_qr_utils import get_allowed_merchant


def customer_segmentation_bubbles_generic(request):
    qs = (
        get_allowed_merchant(request)
        .filter(
            transaction_status="S",
        )
        .exclude(transaction_type__isnull=True)
        .values("transaction_type")
        .annotate(
            average_amount=Avg(Cast("transaction_amount", output_field=FloatField())),
            transactions=Count("transaction_id", distinxt=True),
            radius=Count("sender_name", distinct=True),
        )
    )
    result = {}
    for item in qs:
        transaction_type = item["transaction_type"]
        if transaction_type not in result:
            result[transaction_type] = []
        result[transaction_type].append(
            {
                "transactions": item["transactions"],
                "average_amount": item["average_amount"],
                "radius": item["radius"],
            }
        )

    return result


def average_revenue_trendline_merch_generic(request):
    qs = (
        get_allowed_merchant(request)
        .filter(
            transaction_status="S",
        )
        .values(
            Date=TruncDate("timestamp", tzinfo=get_timezone()),
        )
        .annotate(
            amount=Avg(
                Cast("transaction_amount", FloatField()),
            )
        )
    )
    return qs


def merchant_hourly_analysis_generic(request):  # irrespective of the day
    qs = (
        get_allowed_merchant(request)
        .filter(
            transaction_status="S",
            source="W",
        )
        .annotate(
            Hour=ExtractHour("timestamp", tzinfo=get_timezone()),
        )
        .values("Hour")
        .annotate(
            total_transaction_amount=Sum(
                Cast("transaction_amount", FloatField()),
            ),
        )
        .order_by("Hour")
    )
    return qs
