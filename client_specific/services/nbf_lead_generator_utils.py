# from django.db.models import Q, F, Case, When, Value, CharField, Max
#
# from console.serializers import TransactionSerializer
# from main.utils.boiler_plate import query
#
# from django.db.models.functions import Trunc
# from console.models import StageLog
# from main.tenant_middleware import get_current_tenant_name, get_timezone
# from main.utils.dynamic_db import dynamic_db_connection, get_db_name
#
# user_status = "User status"
#
#
# def leads_generic(request, stage, stage_result):
#     dynamic_db_connection("analytics")
#     params = {
#         "request": request,
#         "models": StageLog,
#         "serializers": TransactionSerializer,
#         "db_schema": get_db_name("analytics"),
#         "filter_kwargs": {
#             "stage": stage,
#             "stage_result": stage_result,
#         },
#         "values": ["channel_id"],
#         "count": True,
#         "distinct": True,
#     }
#     print(params)
#
#     return params
#
#
# def lead_by_products_generic(request):
#     dynamic_db_connection("analytics")
#     field = "Loan"
#     if get_current_tenant_name() == "islamic":
#         field = "Finance"
#     qs = query(
#         request,
#         StageLog,
#         TransactionSerializer,
#         db_schema=get_db_name("analytics"),
#     )
#     qs1 = (
#         qs.filter(
#             stage=user_status,
#             stage_result__in=["yes", "no"],
#             transaction_intent__in=[
#                 "accountCurrent",
#                 "suggestCurrentAccount",
#                 "accountCurrentClassic",
#                 "accountCurrentTwinBenefit",
#                 "accountDeposit",
#                 "accountDepositFixed",
#                 "accountSaving",
#                 "suggestSavingAccount",
#                 "accountSavingBasic",
#                 "accountSavingMaximumSaver",
#                 "cardCredit",
#                 "suggestCreditCard",
#                 "cardCreditInfinite",
#                 "cardCreditClassic",
#                 "cardCreditPlatinum",
#                 "cardCreditPlatinumExclusive",
#                 "cardDebit",
#                 "cardDebitClassic",
#                 "cardDebitPlatinum",
#                 "insuranceMotor",
#                 "loanPersonal",
#                 "loanHome",
#                 "loanMotor",
#                 "loanAuto",
#                 "loanOverdraft",
#                 "accountDepositWakala",
#             ],
#         )
#         .values("channel_id", "transaction_intent")
#         .annotate(max_time=Max("timestamp"))
#         .annotate(
#             product=Case(
#                 When(
#                     Q(transaction_intent="accountCurrent"),
#                     then=Value("Current Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="suggestCurrentAccount"),
#                     then=Value("Suggest Current Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountCurrentClassic"),
#                     then=Value("Classic Current Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountCurrentTwinBenefit"),
#                     then=Value("Twin Benefit Account"),
#                 ),
#                 When(Q(transaction_intent="accountDeposit"), then=Value("Deposit")),
#                 When(
#                     Q(transaction_intent="accountDepositFixed"),
#                     then=Value("Fixed Deposit"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountSaving"),
#                     then=Value("Saving Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="suggestSavingAccount"),
#                     then=Value("Suggest Saving Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountSavingBasic"),
#                     then=Value("Basic Saving Account"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountSavingMaximumSaver"),
#                     then=Value("Max Saver Account"),
#                 ),
#                 When(Q(transaction_intent="cardCredit"), then=Value("Credit Card")),
#                 When(
#                     Q(transaction_intent="suggestCreditCard"),
#                     then=Value("Suggest Credit Card"),
#                 ),
#                 When(
#                     Q(transaction_intent="cardCreditInfinite"),
#                     then=Value("Infinite Credit Card"),
#                 ),
#                 When(
#                     Q(transaction_intent="cardCreditClassic"),
#                     then=Value("Classic Credit Card"),
#                 ),
#                 When(
#                     Q(transaction_intent="cardCreditPlatinumExclusive"),
#                     then=Value("Platinum Exclusive Credit Card"),
#                 ),
#                 When(Q(transaction_intent="cardDebit"), then=Value("Debit Card")),
#                 When(
#                     Q(transaction_intent="cardDebitClassic"),
#                     then=Value("Classic Debit Card"),
#                 ),
#                 When(
#                     Q(transaction_intent="cardDebitPlatinum"),
#                     then=Value("Platinum Debit Card"),
#                 ),
#                 When(
#                     Q(transaction_intent="insuranceMotor"),
#                     then=Value("Motor Insurance"),
#                 ),
#                 When(
#                     Q(transaction_intent="loanPersonal"),
#                     then=Value(f"Personal {field}"),
#                 ),
#                 When(Q(transaction_intent="loanHome"), then=Value(f"Home {field}")),
#                 When(Q(transaction_intent="loanMotor"), then=Value("Motor Loan")),
#                 When(
#                     Q(transaction_intent="loanOverdraft"),
#                     then=Value("Overdraft Loan"),
#                 ),
#                 When(
#                     Q(transaction_intent="accountDepositWakala"),
#                     then=Value("Wakala Deposit"),
#                 ),
#                 When(Q(transaction_intent="loanAuto"), then=Value("Car Finance")),
#                 When(
#                     Q(transaction_intent="cardCreditPlatinum"),
#                     then=Value("Platinum credit card"),
#                 ),
#                 When(Q(transaction_intent="takafulAuto"), then=Value("Car Takaful")),
#                 default=F("transaction_intent"),
#                 output_field=CharField(),
#             ),
#             status=Case(
#                 When(Q(stage=user_status) & Q(stage_result="no"), then=Value("NTB")),
#                 When(
#                     Q(stage=user_status) & Q(stage_result="yes"),
#                     then=Value("ETB"),
#                 ),
#                 output_field=CharField(),
#             ),
#         )
#         .values("channel_id", "product", "status")
#         .distinct()
#         .annotate(
#             timestamp=Trunc(F("max_time"), "second", tzinfo=get_timezone()),
#         )
#         .order_by("-timestamp")
#     )
#     return (
#         qs1,
#         ["channel_id", "product", "status", "timestamp"],
#         "lead_by_products",
#     )
