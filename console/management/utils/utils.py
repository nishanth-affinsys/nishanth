import re
import os
import json
from django.db import transaction, connections
from django.core.management import call_command
from django.conf import settings
from main.settings import get_env_value
import logging
from main.celery import background
from console.models import BotbuilderProject
from datetime import timedelta
from django.utils import timezone
import openpyxl

logger = logging.getLogger(__name__)


def get_tenants():
    tenants = list(
        BotbuilderProject.objects.using("botbuilder")
        .filter(is_active=True)
        .values_list("tenant", flat=True)
    )
    return tenants


class DBException(Exception):
    def __init__(self, db_name):
        self.message = f"DB Connection for {db_name} not found"
        super().__init__(self.message)


def generate_views(file_path, pattern, service_name, db_engine, tenant=None):
    with open(file_path, "r") as f:
        sql_content = f.read()
        matches = re.findall(pattern, sql_content)
        matches = set(matches)
        for match in matches:
            try:
                env_value = get_env_value(match)
                sql_content = sql_content.replace(
                    f"${{{match}}}", f"{env_value}_{tenant}" if tenant else env_value
                )
                sql_content = sql_content.replace(
                    f"{env_value}_{tenant}",
                    (
                        f"{env_value}_{tenant}_bkp"
                        if "_backup" in service_name
                        else f"{env_value}_{tenant}"
                    ),
                )

            except Exception as e:
                raise DBException(match)
    if len(sql_content) < 1:
        logger.error(
            f"No views to be executed in db alias '{service_name}' with db engine '{db_engine}'"
        )
        return
    cursor = connections[service_name].cursor()
    try:
        query = None
        try:
            if db_engine == "oracle":
                for i, query in enumerate(sql_content.split(";\n")):
                    with transaction.atomic():
                        cursor.execute(query)
            else:
                with transaction.atomic():
                    cursor.execute(sql_content)
            logger.info(
                f"successfully Executed views of '{service_name}' and '{tenant}' with db engine {db_engine}"
            )
        except Exception as e:
            if query:
                logger.error(f"Exception raised while Executing Query {query}: {e}")
            else:
                logger.error(
                    f"Exception raised while Executing views of '{service_name}': {e}"
                )
    except Exception as e:
        logger.error(f"Error caught while generating views: {e}")
    finally:
        cursor.close()
        f.close()


def create_views(file_path, pattern, db_engine, service_name, tenants=None):
    if not os.path.exists(file_path):
        logger.info(
            f"No views to be executed in db alias '{service_name}' with db engine '{db_engine}'"
        )
        return

    if service_name not in settings.TENANTS:
        logger.error(f"Make sure the db alias '{service_name}' is valid and connected")
        return

    if tenants is None and isinstance(tenants, list):
        generate_views(file_path, pattern, service_name, db_engine)
    else:
        try:
            if isinstance(tenants, list):
                for tenant in tenants:
                    if tenant == "default":
                        generate_views(file_path, pattern, service_name, db_engine)
                    else:
                        generate_views(
                            file_path, pattern, service_name, db_engine, tenant
                        )
            else:
                generate_views(file_path, pattern, service_name, db_engine, tenants)
        except Exception as e:
            logger.error("Exception while generating views: %s", e)


def refresh_views(db_engine, service_name, dynamic_db, tenant):
    pattern = r"\${(\w+)}"
    service_file = service_name.replace("_backup", "")
    file_path = f"{settings.BASE_DIR}/console/management/utils/sql_views/{service_file}_{db_engine}.sql"
    try:
        if dynamic_db == "True":  # Dynamic DB is turned off : client dev
            create_views(file_path, pattern, db_engine, service_name)
        else:
            if tenant != "None":
                create_views(file_path, pattern, db_engine, service_name, tenant)
            else:
                tenants_list = get_tenants()
                create_views(file_path, pattern, db_engine, service_name, tenants_list)
    except Exception as e:
        logger.error(f"Exception raised while creating views: {e}")


@background
def create_views_consumer():
    logger.info("Wrapper for triggering listener")


def schedule_views(data: dict):
    tenant = data["tenant"]
    now = str(
        (timezone.now() + timedelta(minutes=settings.TIME_SKIP_VIEWS)).strftime(
            "%Y-%m-%dT%H:%M"
        )
    )
    logger.debug(f"Received tenant: {tenant}")
    from tasks.utils import deactivate_task

    deactivate_task(task_id=f"create_views_{tenant}")
    create_views_consumer(task_id=f"create_views_{tenant}", start_date=now)


def get_permissions_file(type):
    if type == "All":
        path = f"{settings.BASE_DIR}/console/static/"
        filenames = []
        permissions = {}
        for root, _, files in os.walk(path):
            for file_name in files:
                if os.path.isfile(os.path.join(path, file_name)):
                    filenames.append(str(file_name))

        for filename in filenames:
            with open(f"{path}{filename}") as file:
                dashboard_data = json.load(file)
            for key in dashboard_data.keys():
                data = dashboard_data["common"]
                permissions[filename] = {
                    "Name": data["chart_title"],
                    "Permission": filename.split(".")[0].replace("_", " "),
                    "Endpoint": filename.replace(".json", ""),
                }
        generate_excel_file(permissions)

    else:
        with open(f"{settings.BASE_DIR}/console/static/{type}.json") as file:
            dashboard_data = json.load(file)
        permissions = {}
        for key in dashboard_data.keys():
            data = dashboard_data[key]
            permissions[key] = {
                "Name": data["chart_title"],
                "Permission": key.replace("_", " "),
                "Endpoint": key,
            }
        generate_excel_file(permissions)


def generate_excel_file(permissions):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data"
    headers = ["File Name", "Name", "Permission", "Endpoint"]
    ws.append(headers)
    for filename, values in permissions.items():
        row_data = [filename, values["Name"], values["Permission"], values["Endpoint"]]
        ws.append(row_data)

    excel_filename = "permissions.xlsx"
    wb.save(excel_filename)
    logger.info("Permissions Generated")
