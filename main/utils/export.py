import json
from io import StringIO, BytesIO
import csv
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from rest_framework.response import Response
from django.core import serializers as ser
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from django.db.models.functions import Cast, Trunc
from django.db.models import F

from django.template.loader import get_template
from main.tenant_middleware import get_timezone
from xhtml2pdf import pisa
import pandas as pd


# function to export the reports in csv format
def export_csv(items, fieldNames, fileName):
    buffer = StringIO()
    buffer.write("\ufeff")  # BOM encoding to support MSexcel
    writer = csv.DictWriter(buffer, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(list(items))

    buffer.seek(0)
    response = HttpResponse(
        content=buffer.getvalue(), content_type="text/csv; charset=utf-8"
    )
    response["Content-Disposition"] = f"attachment; filename={fileName}"

    return response


def export_pdf(items, fieldNames, fileName, title, user):
    now = datetime.now(get_timezone())
    timestamp = now.strftime("%B %d, %Y %H:%M:%S")
    objs = json.dumps(list(items), cls=DjangoJSONEncoder)
    objs = json.loads(objs)
    context = {
        "Objs": objs,
        "Fields": fieldNames,
        "Title": title,
        "Timestamp": timestamp,
        "User": user,
        "Filename": fileName,
    }
    template = get_template("index.html")
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = f"inline; filename={fileName}"
        response["Content-Transfer-Encoding"] = "binary"
        return response
    return None


def export_excel(items, timestamp_keys, fileName):
    user_data = pd.DataFrame(items)
    user_data[timestamp_keys] = user_data[timestamp_keys].apply(
        lambda col: pd.to_datetime(col)
        .dt.tz_convert("UTC")
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )
    buffer_data = BytesIO()
    writer = pd.ExcelWriter(buffer_data, engine="openpyxl")
    user_data.to_excel(writer, index=False)
    writer.close()
    buffer_data.seek(0)
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f"attachment; filename={fileName}"
    response.write(buffer_data.getvalue())
    return response
