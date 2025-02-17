from auth.authentication import BBAuth
from django.core.management import BaseCommand, call_command

from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Startup command to refresh permissions and refresh views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--create",
            "-c",
            nargs="?",
            default="True",
            choices=["False", "True"],
            help="Specify to create views. default value is 'True'.",
        )
        parser.add_argument(
            "--name",
            "-n",
            nargs="?",
            default="all",
            help="Specify the db alias name for the views "
            "to be executed. default value is 'all'.",
        )
        parser.add_argument(
            "--db_engine",
            "-db",
            nargs="?",
            default=settings.DB_ENGINE,
            help="Specify the db engine name for the views. default value is 'postgres'.",
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
        create = options.get("create")
        if create == "True":
            file_name = options.get("name")
            db_engine = options.get("db_engine")
            use_default_db = options.get("use_default_db")
            tenant = options.get("tenant")
            logger.info("Creating Views")
            call_command(
                "create_views",
                name=file_name,
                db_engine=db_engine,
                use_default_db=use_default_db,
                tenant=tenant,
            )
        else:
            logger.info("Skipping Create Views")
        BBAuth.push_permissions()
        with open(f"{settings.BASE_DIR}/post_start.txt", "w") as file:
            file.write("Success")
