import os
import json
import conf
import requests
from os import walk
from django.conf import settings
from django.core.cache import cache
from main.tenant_middleware import get_current_tenant_name
import logging

logger = logging.getLogger(__name__)


def extract_titles_from_dashboard(file_path, tenant):
    with open(file_path, "r") as file:
        data = json.load(file)
        if conf.getenv(tenant, key="DASHBOARD_LOCATION") in data.keys():
            titles = [
                {"title": chart["title"], "path": chart.get("path", "")}
                for chart in data.get(
                    conf.getenv(tenant, key="DASHBOARD_LOCATION")
                ).get("charts")
                if chart.get("path")
            ]
            if titles:
                return titles


def get_user_permissions(cookies, headers):
    try:
        if settings.STUB_INTERNAL_PERMISSIONS_API:
            with open(
                f"{settings.BASE_DIR}/console/static/test/test_permissions.json"
            ) as file:
                dashboard_permissions = json.load(file)
            file.close()
        else:
            internal_permissions_api = settings.INTERNAL_PERMISSIONS_API
            response = requests.get(
                internal_permissions_api, cookies=cookies, headers=headers
            )
            dashboard_permissions = response.json()
        names = [obj["name"] for obj in dashboard_permissions.get("permissions", [])]
        return names
    except Exception as e:
        print(e)


def get_dashboard_names(request, tenant):
    cookies = request.COOKIES
    headers = request.headers
    permissions = get_user_permissions(cookies, headers)
    path = f"{settings.BASE_DIR}/console/static/"
    response = []
    filenames = []
    for _, dir, filenames_walk in walk(path):
        if dir:
            filenames = filenames_walk
    for filename in filenames:
        dashboard_permission = filename.split(".")[0]
        if dashboard_permission in permissions:
            with open(f"{path}{filename}") as file:
                dashboard_data = json.load(file)
            file.close()
            if conf.getenv(tenant, key="DASHBOARD_LOCATION") in dashboard_data.keys():
                data = dashboard_data[conf.getenv(tenant, key="DASHBOARD_LOCATION")]
            else:
                data = dashboard_data.get("common")

            body = {
                "key": dashboard_permission,
                "value": data["chart_title"],
                "charts": [
                    {"value": chart["title"], "key": chart["path"]}
                    for chart in data["charts"]
                    if chart.get("path")
                ],
            }
            if body.get("charts"):
                response.append(body)
    cache.set("dashboard_details", json.dumps(response))
    return response


def refresh_dashboard_cache(request, tenant):
    cache.delete("dashboard_details")
    get_dashboard_names(request, tenant)


def get_repo_url(tenant):
    if settings.GIT_PROVIDER == 'github':
        repo_url = f"https://github.com/{settings.GIT_USER}/{tenant}"
    else:
        repo_url = f"{settings.GIT_HTTP_PROXY_URL}/{settings.GIT_WORKSPACE}/{tenant}"
    return repo_url
