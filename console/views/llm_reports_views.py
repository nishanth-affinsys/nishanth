from auth.tags import AuthTags

from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from console.services.llm_reports_utils import (
    total_doc_uploaded_bigno_generic,
    total_links_given_bigno_generic,
    llm_conversations_log_generic,
)

from main.settings import MAX_PDF_LIMIT
from main.utils.export import export_csv, export_pdf
from main.utils.boiler_plate import (
    get_generic_response,
    return_table,
)

from drf_spectacular.utils import extend_schema


class LLMReportsViewSet(GenericViewSet):
    @extend_schema(
        operation_id="llm_total_docs_uploaded_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="total docs uploaded",
    )
    @action(methods=["POST"], detail=False, url_path="llm_total_docs_uploaded_bigno")
    def total_docs_uploaded_bigno(self, request, *args, **kwargs):
        params = total_doc_uploaded_bigno_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="llm_total_links_given_bigno",
        tags=[AuthTags.AUTHORIZE],
        description="total docs uploaded",
    )
    @action(methods=["POST"], detail=False, url_path="llm_total_links_given_bigno")
    def total_links_given_bigno(self, request, *args, **kwargs):
        params = total_links_given_bigno_generic(request)
        return get_generic_response(params)

    @extend_schema(
        operation_id="llm_conversations_log",
        tags=[AuthTags.AUTHORIZE],
        description="total docs uploaded",
    )
    @action(methods=["POST"], detail=False, url_path="llm_conversations_log")
    def llm_conversations_log(self, request, *args, **kwargs):
        items, _, _ = llm_conversations_log_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="llm_conversations_log_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="total docs uploaded",
    )
    @action(methods=["POST"], detail=False, url_path="llm_conversations_log_export_csv")
    def llm_conversations_log_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = llm_conversations_log_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="llm_conversations_log_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="total docs uploaded",
    )
    @action(methods=["POST"], detail=False, url_path="llm_conversations_log_export_pdf")
    def llm_conversations_log_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = llm_conversations_log_generic(request)
        if len(response) > MAX_PDF_LIMIT:
            response = response[:MAX_PDF_LIMIT]
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            "Conversation Log",
            request.user.username,
        )
        return items
