import ast

from django.db.models import (
    F,
)
from django.db.models.functions import Trunc

from console.models import MessageLog, LlmUpload
from console.serializers import LlmUploadSerializer, LlmMessagelogSerializer
from main.tenant_middleware import get_timezone
from main.utils.boiler_plate import query
from main.utils.dynamic_db import get_db_name, dynamic_db_connection


def total_doc_uploaded_bigno_generic(request):
    dynamic_db_connection("llm")
    params = {
        "request": request,
        "models": LlmUpload,
        "serializers": LlmUploadSerializer,
        "db_schema": get_db_name("llm"),
        "filter_kwargs": {
            "indexing_status": "Completed",
            "object_type": "file",
        },
        "count": True,
    }
    return params


def total_links_given_bigno_generic(request):
    dynamic_db_connection("llm")
    params = {
        "request": request,
        "models": LlmUpload,
        "serializers": LlmUploadSerializer,
        "db_schema": get_db_name("llm"),
        "filter_kwargs": {
            "indexing_status": "Completed",
            "object_type": "url",
        },
        "count": True,
    }
    return params


def llm_conversations_log_generic(request):
    dynamic_db_connection("analytics")
    qs = query(request, MessageLog, LlmMessagelogSerializer, get_db_name("analytics"))
    msg_qs = (
        qs.filter(message__isnull=False)
        .values(
            Customer_Id=F("channel_id"),
            User_Session_Id=F("session_id"),
            Channel=F("channel"),
            Message=F("message"),
            Source=F("source"),
            Intent=F("intent"),
            Timestamp=Trunc(F("timestamp"), "second", tzinfo=get_timezone()),
        )
        .order_by("-Timestamp")
    )
    bot_message = " "
    result = []
    for item in msg_qs:
        source = item["Source"]
        if source == "bot":
            message_data = ast.literal_eval(item.get("Message"))
            if message_data.get("data"):
                data = message_data["data"][0]
                title = data.get("title", " ")
                subtitle = data.get("subtitle", " ")
                if title and subtitle:
                    bot_message = title + " " + subtitle
                elif title:
                    bot_message = title
                else:
                    bot_message = subtitle
        if source == "llm":
            message_data = ast.literal_eval(item.get("Message"))
            if message_data.get("card"):
                message_data = message_data["card"]
                if message_data.get("data"):
                    data = message_data["data"][0]
                    title = data.get("title", " ")
                    subtitle = data.get("subtitle", " ")
                    if title and subtitle:
                        bot_message = title + " " + subtitle
                    elif title:
                        bot_message = title
                    else:
                        bot_message = subtitle
            else:
                bot_message = item["Message"]
        if bot_message:
            data = {
                "Customer_Id": item["Customer_Id"],
                "User_Session_Id": item["User_Session_Id"],
                "Channel": item["Channel"],
                "Message": bot_message,
                "Source": source,
                "Intent": item["Intent"],
                "Timestamp": item["Timestamp"],
            }
            result.append(data)
    result = sorted(result, key=lambda x: x["Timestamp"], reverse=True)
    return (
        result,
        ["Customer_Id", "User_Session_Id", "Channel", "Message", "Source", "Intent", "Timestamp"],
        "llm_conversation_log",
    )
