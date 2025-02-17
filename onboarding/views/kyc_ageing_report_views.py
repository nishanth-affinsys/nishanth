from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from main.utils.boiler_plate import return_table
from main.utils.export import export_csv, export_pdf
from onboarding.services.kyc_ageing_report_utils import kyc_ageing_report_generic, \
    onboarding_short_kyc_exception_generic


class KYCAgeingReportViewSet(GenericViewSet):
    @extend_schema(
        operation_id="kyc_ageing_report",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display overall ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_ageing_report")
    def kyc_ageing_report(self, request, *args, **kwargs):
        result, _, _ = kyc_ageing_report_generic(request)
        return return_table(result, request)

    @extend_schema(
        operation_id="kyc_ageing_report_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display overall ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_ageing_report_export_csv")
    def kyc_ageing_report_export_csv(self, request, *args, **kwargs):
        response, field_names, file_name = kyc_ageing_report_generic(request)
        items = export_csv(response, field_names, f"{file_name}.csv")
        return items

    @extend_schema(
        operation_id="kyc_ageing_report_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="Used to display overall ageing for Retail",
    )
    @action(methods=["POST"], detail=False, url_path="kyc_ageing_report_export_pdf")
    def kyc_ageing_report_export_pdf(self, request, *args, **kwargs):
        response, field_names, file_name = kyc_ageing_report_generic(request)
        items = export_pdf(
            response,
            field_names,
            f"{file_name}.pdf",
            " KYC Ageing Report",
            request.user.username,
        )
        return items

    @extend_schema(
        operation_id="onboarding_short_kyc_exception",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_short_kyc_exception")
    def onboarding_short_kyc_exception(self, request):
        response, _, _ = onboarding_short_kyc_exception_generic(request)
        return return_table(response, request)

    @extend_schema(
        operation_id="onboarding_short_kyc_exception_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="onboarding_short_kyc_exception_export_csv",
    )
    def onboarding_short_kyc_exception_export_csv(self, request):
        response, fieldNames, fileName = onboarding_short_kyc_exception_generic(request)
        return export_csv(response, fieldNames, f"{fileName}.csv")

    @extend_schema(
        operation_id="onboarding_short_kyc_exception_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="onboarding_short_kyc_exception_export_pdf",
    )
    def onboarding_short_kyc_exception_export_pdf(self, request):
        response, fieldNames, fileName = onboarding_short_kyc_exception_generic(request)
        return export_pdf(
            response,
            fieldNames,
            f"{fileName}.pdf",
            "KYC Exception Applications (2 days)",
            request.user.username,
        )

    @extend_schema(
        operation_id="onboarding_kyc_exception",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(methods=["POST"], detail=False, url_path="onboarding_kyc_exception")
    def onboarding_kyc_exception(self, request):
        response, _, _ = onboarding_short_kyc_exception_generic(request, days=5)
        return return_table(response, request)

    @extend_schema(
        operation_id="onboarding_kyc_exception_export_csv",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_kyc_exception_export_csv"
    )
    def onboarding_kyc_exception_export_csv(self, request):
        response, fieldNames, fileName = onboarding_short_kyc_exception_generic(
            request, days=5
        )
        return export_csv(response, fieldNames, f"{fileName}.csv")

    @extend_schema(
        operation_id="onboarding_kyc_exception_export_pdf",
        tags=[AuthTags.AUTHORIZE],
        description="used to show report email containing applications in the KYC Exception queue for more than 2 days.",
    )
    @action(
        methods=["POST"], detail=False, url_path="onboarding_kyc_exception_export_pdf"
    )
    def onboarding_kyc_exception_export_pdf(self, request):
        response, fieldNames, fileName = onboarding_short_kyc_exception_generic(
            request, days=5
        )
        return export_pdf(
            response,
            fieldNames,
            f"{fileName}.pdf",
            "KYC Exception Applications (5 days)",
            request.user.username,
        )
