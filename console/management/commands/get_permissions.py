import logging
from django.core.management import BaseCommand
from console.management.utils.utils import get_permissions_file

logger = logging.getLogger("__name__")


class Command(BaseCommand):
    help = "Get permissions for all dashboard for that release"

    def add_arguments(self, parser):
        parser.add_argument(
            "--template",
            "-t",
            nargs="?",
            default="All",
            help="specify the template file",
        )

    def handle(self, *args, **options):
        get_permissions_file(options["template"])
