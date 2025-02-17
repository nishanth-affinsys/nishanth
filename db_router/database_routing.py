from db_router.database_routing_middleware import _LOCAL


class DatabaseRouting:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        setattr(_LOCAL, "client_code", self.db_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        delattr(_LOCAL, "client_code")
