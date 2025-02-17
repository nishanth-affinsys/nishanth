from boilerplate.lib.utils.db_router import DynamicDatabaseConnection
from main.tenant_middleware import get_current_tenant_name
from django.conf import settings

import logging

logger = logging.getLogger(__name__)


def dynamic_db_connection(schema_name, tenant_name=None):
    try:
        if tenant_name is None:
            tenant_name = get_current_tenant_name()
        with DynamicDatabaseConnection(tenant_name, schema_name):
            logger.debug(f"Connection established to db: {tenant_name}")
    except Exception as e:
        print(e)


def dynamic_db_consumer_connection(schema_name, tenant_name):
    try:
        with DynamicDatabaseConnection(tenant_name, schema_name):
            logger.debug("Connection established")
    except Exception as e:
        print(e)


def get_db_name(service_name, tenant_name=None):
    return (
        service_name
        if settings.USE_DATABASE_AS_DEFAULT
        else f"{service_name}_{get_current_tenant_name() if tenant_name is None else tenant_name}"
    )


def get_db_consumer_name(service_name, tenant_name):
    return (
        service_name
        if settings.USE_DATABASE_AS_DEFAULT
        else f"{service_name}_{tenant_name}"
    )
