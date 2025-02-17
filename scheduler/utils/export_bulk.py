import importlib
import conf
from django.http import HttpRequest
from io import BytesIO
import zipfile
from main.tenant_middleware import set_current_tenant_name, set_timezone
import logging

logger = logging.getLogger(__name__)


def create_request_object(filters, tenant):
    request = HttpRequest()
    request.method = "POST"
    request.COOKIES = {"tenant": tenant}
    request.data = filters
    return request


def export_bulk(request, path, tenant,time_zone):
    set_current_tenant_name(tenant)
    set_timezone(time_zone)
    logger.warning(f"running for the function :{path}")
    module_name, view_set_name, function_name = path.split("/")
    module = importlib.import_module(module_name)
    view_set_obj = getattr(module, view_set_name)
    response = getattr(view_set_obj, function_name)(view_set_obj, request)
    items = response.content
    file_name = response["Content-Disposition"].split("filename=")[1]
    return items, file_name


def create_zip_file_from_stringio(data_list):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(
            zip_buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zipf:
        for data_buffer in data_list:
            buffer, filename = data_buffer
            zipf.writestr(filename, buffer)
    zip_buffer.seek(0)
    return zip_buffer
