from auth.tags import AuthTags
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from rest_framework.response import Response
from main.utils.export import export_csv
from main.utils.boiler_plate import return_table
from client_specific.services.live_transactions_utils import (api_login_services, successful_transaction_generic, \
                                                              successful_transaction_goal_completed_generic,
                                                              successful_transaction_goal_not_completed,
                                                              failed_transaction, \
                                                              system_aborted, user_aborted,
                                                              detail_report_new_generic)


class LiveTransactionViewSet(GenericViewSet):
    @extend_schema(
        operation_id="api_login",
        tags=[AuthTags.PUBLIC],
        description="Used to show the api login details in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="api_login")
    def apiloginservices(self, request, *args, **kwargs):
        items, _, _ = api_login_services(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="api_login_export",
        tags=[AuthTags.PUBLIC],
        description="Used to download the api login details in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="api_login_export")
    def apiloginservices_export(self, request, *args, **kwargs):
        items, fieldNames, fileName = api_login_services(request)
        response = export_csv(items, fieldNames, f"{fileName}.csv")
        return response

    @extend_schema(
        operation_id="live_successful_transaction",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of successful transactions"
    )
    @action(methods=["POST"], detail=False, url_path="live_successful_transaction")
    def Successful_transaction(self, request, *args, **kwargs):
        value = successful_transaction_generic(request)
        return Response(data={"count": value})

    @extend_schema(
        operation_id="live_successful_transaction_goal_completed",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of successful transactions (goal completed) login details in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_successful_transaction_goal_completed")
    def Successful_transaction_goal_completed(self, request, *args, **kwargs):
        qs = successful_transaction_goal_completed_generic(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="live_successful_transaction_goal_not_completed",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of successful transactions (goal not completed) login details in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_successful_transaction_goal_not_completed")
    def Successful_transaction_goal_not_completed(self, request, *args, **kwargs):
        qs = successful_transaction_goal_not_completed(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="live_failed_transaction",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of failed transactions in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_failed_transaction")
    def Failed_transaction(self, request, *args, **kwargs):
        val = failed_transaction(request)
        return Response(data={"count": val})

    @extend_schema(
        operation_id="live_system_aborted",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of system aborted in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_system_aborted")
    def System_aborted(self, request, *args, **kwargs):
        qs = system_aborted(request)
        return Response(data={"count": qs})

    @extend_schema(
        operation_id="live_user_aborted",
        tags=[AuthTags.PUBLIC],
        description="Used to show the count of user aborted in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_user_aborted")
    def User_aborted(self, request, *args, **kwargs):
        qs = user_aborted(request)
        return Response(data={"count": qs})

    # @action(methods=["POST"], detail=False, url_path="detailed_report_1")
    # def detailed_report(self, request, *args, **kwargs):
    #     items, fieldNames, fileName = detailed_report(request)
    #     return return_table(items, request)
    #
    # @action(methods=["POST"], detail=False, url_path="detailed_report_export")
    # def detailed_report_export(self, request, *args, **kwargs):
    #     items, fieldNames, fileName = detailed_report(request)
    #     response = export_csv(items, fieldNames, f"{fileName}.csv")
    #     return response

    @extend_schema(
        operation_id="live_detailed_report",
        tags=[AuthTags.PUBLIC],
        description="Used to show the detailed report table in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_detailed_report")
    def detailed_report_new(self, request, *args, **kwargs):
        items, fieldNames, fileName = detail_report_new_generic(request)
        return return_table(items, request)

    @extend_schema(
        operation_id="live_detailed_report_export",
        tags=[AuthTags.PUBLIC],
        description="Used to download the detailed report table in standalone dashboard"
    )
    @action(methods=["POST"], detail=False, url_path="live_detailed_report_export")
    def detailed_report_new_export(self, request, *args, **kwargs):
        items, fieldNames, fileName = detail_report_new_generic(request)
        response = export_csv(items, fieldNames, f"{fileName}.csv")
        return response
