from django.core.management import BaseCommand

from console.management.utils.utils import delete_views
from django.conf import settings


class Command(BaseCommand):
    help = "Management command used to delete views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--db_engine",
            "-db",
            nargs="?",
            default=settings.DB_ENGINE,
            help="Specify the db engine name for the views to be deleted. default value is 'postgres'",
            choices=["postgres", "oracle", "sqlite"],
        )

    def handle(self, *args, **options):
        db_engine = options.get("db_engine")
        if db_engine == "oracle":
            for alias in settings.TENANTS:
                delete_views(db_engine, alias)
        else:
            delete_views(db_engine)
