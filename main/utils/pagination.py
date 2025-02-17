from collections import OrderedDict

from django.core.paginator import Paginator, EmptyPage, Page
from rest_framework.response import Response
from rest_framework.utils.urls import replace_query_param, remove_query_param
from main.settings import get_env_value

import logging

logger = logging.getLogger(__name__)


class CustomPaginator(Paginator):
    """
    Custom Paginator class to get count, and next & previous links
    """

    MAX_PER_PAGE = get_env_value("MAX_PER_PAGE")
    page_query_param = "page"

    def __init__(self, items, request):
        self.request = request
        self._page = None
        super().__init__(items, self.MAX_PER_PAGE)

    def page(self, number):
        self._page = super().page(number)
        return self._page

    def get_next_link(self):
        if not self._page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self._page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        if not self._page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self._page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)


def get_paginated_response(items, request):
    paginator = CustomPaginator(items, request)
    page_num = request.GET.get("page", 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)
    return Response(
        OrderedDict(
            [
                ("count", page.paginator.count),
                ("next", paginator.get_next_link()),
                ("previous", paginator.get_previous_link()),
                ("results", list(page)),
            ]
        )
    )


"""
For creating pagination, for next page (link), previous page (link), it applies for all table chart.
Default 10 entries will be in single page
It is passed through query params in API
"""
