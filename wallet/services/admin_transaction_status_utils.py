from main.tenant_middleware import get_current_tenant_name
from main.utils.boiler_plate import query
from wallet.models import TransactionsTransaction
from wallet.serializers import TransactionSerializer


def wallet_mw_generic(request, type_list):
    qs = query(request, TransactionsTransaction, TransactionSerializer, "transaction")
    qs = qs.filter(tenant=get_current_tenant_name(), status__in=type_list).count()
    return qs
