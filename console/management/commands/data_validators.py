from django.core.management.base import BaseCommand
from asyncio.log import logger
from console import models as event
from handoff import models as handoff
from clickstream import models as clickstream
from campaign_manager import models as campaign

from main import settings
import inspect

"""
Data validators- Health checkups for tables, Validations for each tables, to check if the quantum of discrepencies is too high , like to check all null
values in a column, or number of null entries, etc.

"""


class Command(BaseCommand):
    help = "Checking NULL columns in the models."

    DB_MODULE_MAP = {
        "event": event,
        "handoff": handoff,
        "clickstream": clickstream,
        "campaign": campaign,
    }

    def get_db_models(self, db):
        models_list = []
        if self.DB_MODULE_MAP.get(db):
            module_name = self.DB_MODULE_MAP[db]
        else:
            return None
        for members in inspect.getmembers(module_name, inspect.isclass):
            models_list.append(members[1])
        return models_list

    def handle(self, *args, **kwargs):
        self.stdout.write("Cheking all NULLs !!")
        print()
        l = []
        logger.warning(f"Column || Tables || Schema ")
        print()
        for db in settings.DATABASES:
            if self.get_db_models(db):
                models_list = self.get_db_models(db)
                for model in models_list:
                    for field in model._meta.get_fields():
                        d = {field.name: None}
                        if len(model.objects.using(db).filter(**d)) == len(
                            model.objects.using(db).all()
                        ):
                            logger.warning(f"{field.name} || {model.__name__} || {db} ")

        print()

        self.stdout.write("Cheking each Column wise NULLs !!")
        print()
        logger.warning(f"Column || Count || Tables || Schema ")
        print()
        for db in settings.DATABASES:
            if self.get_db_models(db):
                models_list = self.get_db_models(db)
                for model in models_list:
                    for field in model._meta.get_fields():
                        d = field.name
                        filter_kwargs = {f"{d}__isnull": True}
                        no_of_null = len(
                            model.objects.using(db).filter(**filter_kwargs)
                        )
                        if no_of_null > 50:
                            logger.warning(
                                f"{field.name} || {no_of_null} || {model.__name__} || {db}"
                            )
