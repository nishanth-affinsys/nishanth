from db_router.database_routing_middleware import get_current_db_name


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        current_db = get_current_db_name()
        return current_db if current_db is not None else None

    def db_for_write(self, model, **hints):
        current_db = get_current_db_name()
        return current_db if current_db is not None else None

    def allow_relation(self, *args, **kwargs):
        return None

    def allow_syncdb(self, *args, **kwargs):
        return None

    def allow_migrate(self, *args, **kwargs):
        return None
