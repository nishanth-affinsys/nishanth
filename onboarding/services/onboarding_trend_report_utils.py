from django.db.models import (
    Count,
    Value,
    Func,
    F,
    Q,
    CharField,
)

from django.db.models.functions import Cast, TruncDate
from main.tenant_middleware import get_current_tenant_name, get_timezone
from onboarding.serializers import OnboardingSerializer
from main.utils.boiler_plate import query
from main.utils.dynamic_db import dynamic_db_connection, get_db_name


def channelwise_onboarding_generic(request, onboarding_channel, customer_type):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, onboarding_channel, OnboardingSerializer, get_db_name("onboarding")
    )
    items = (
        qs1.filter(customer_type=customer_type)
        .values(Date=TruncDate("create_timestamp", tzinfo=get_timezone()))
        .annotate(
            Agent=Count(
                1,
                filter=(Q(onboarding_channel="Agent") & Q(queue_code="QSUCCESS")),
            ),
            Self=Count(
                1,
                filter=(Q(onboarding_channel="Self") & Q(queue_code="QSUCCESS")),
            ),
            Staff=Count(
                1,
                filter=(Q(onboarding_channel="Staff") & Q(queue_code="QSUCCESS")),
            ),
        )
        .order_by("-Date")
    )
    return items


def total_customer_onboarded_generic(request, onboarding_channel, customer_type):
    dynamic_db_connection("onboarding")
    qs1 = query(
        request, onboarding_channel, OnboardingSerializer, get_db_name("onboarding")
    )
    items = (
        qs1.filter(customer_type=customer_type)
        .values(
            Month=Cast(
                Func(
                    F("create_timestamp"),
                    Value("YYYY-Mon"),
                    function="TO_CHAR",
                ),
                output_field=CharField(),
            )
        )
        .annotate(Count=Count(1, filter=Q(queue_code="QSUCCESS")))
        .filter(Count__gt=0)
        .order_by("-Month")
    )
    return items


def productwise_account_opened_generic(request, model_name):
    dynamic_db_connection("onboarding")
    qs = query(request, model_name, OnboardingSerializer, get_db_name("onboarding"))
    items = (
        qs.filter(queue_code="QSUCCESS")
        .annotate(label=F("product_name"))
        .values("label")
        .annotate(count=Count("label"))
    )
    return items
