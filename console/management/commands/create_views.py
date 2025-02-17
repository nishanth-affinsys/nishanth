from django.core.management import BaseCommand

from console.management.utils.utils import refresh_views
from django.conf import settings


class Command(BaseCommand):
    help = "Management command used to create views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--name",
            "-n",
            nargs="?",
            default="all",
            help="Specify the db alias name for the views "
            "to be executed. default value is 'all'",
        )
        parser.add_argument(
            "--db_engine",
            "-db",
            nargs="?",
            default=settings.DB_ENGINE,
            help="Specify the db engine name for the views. default value is 'postgres'",
            choices=["postgres", "oracle", "sqlite"],
        )
        parser.add_argument(
            "--use_default_db",
            "-default",
            nargs="?",
            default=str(settings.USE_DATABASE_AS_DEFAULT),
            help="Specify False for using dynamic db engine. default value is True.",
            choices=["True", "False"],
        )
        parser.add_argument(
            "--tenant",
            "-t",
            nargs="?",
            default="None",
            help="Specify the tenant name for the generation of views",
        )

    def handle(self, *args, **options):
        file_name = options.get("name")
        db_engine = options.get("db_engine")
        use_default_db = options.get("use_default_db")
        tenant = options.get("tenant")
        if file_name == "all":
            for service_name in settings.TENANTS:
                refresh_views(db_engine, service_name, use_default_db, tenant)
        else:
            refresh_views(db_engine, file_name, use_default_db, tenant)
