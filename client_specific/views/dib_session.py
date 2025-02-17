# from datetime import timedelta
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.decorators import api_view, action
# from django.db.models import (
#     Count,
#     Avg,
#     Case,
#     When,
#     Value,
#     Avg,
#     Q,
#     Max,
#     Min,
#     Func,
#     ExpressionWrapper,
#     Case,
#     When,
#     IntegerField,
#     F,
#     DateField,
#     TimeField, DateTimeField,
# )
# from client_specific.models import Usersessionsig9Ccrl3A0Djayyw4Muydq
#
#
# class SessionViewSet(GenericViewSet):
#     @action(methods=["POST"], detail=False, url_path="session_expire")
#     def session_expire(self, request, *args, **kwargs):
#         user_session_info = Usersessionsig9Ccrl3A0Djayyw4Muydq.objects.using("default").values().order_by("customer_id","timestamp")
#         customer = user_session_info[0].get("customer_id")
#         session_expire = user_session_info[0].get("timestamp") + timedelta(minutes=1440)
#         response = []
#         for i in user_session_info:
#             if i.get("customer_id") != customer:
#                 customer = i.get("customer_id")
#                 session_expire = i.get("timestamp") + timedelta(minutes=1440)
#                 result = {
#                     "channel": i.get("channel"),
#                     "customer": customer,
#                     "timestamp": i.get("timestamp"),
#                     "session_expire": session_expire
#                 }
#                 response.append(result)
#             elif i.get("timestamp") >= session_expire:
#                 session_expire = i.get("timestamp") + timedelta(minutes=1440)
#                 result = {
#                     "channel": i.get("channel"),
#                     "customer": customer,
#                     "timestamp": i.get("timestamp"),
#                     "session_expire": session_expire
#                 }
#                 response.append(result)
#             else:
#                 result = {
#                     "channel": i.get("channel"),
#                     "customer": customer,
#                     "timestamp": i.get("timestamp"),
#                     "session_expire": session_expire
#                 }
#                 response.append(result)
#         return Response(response)
