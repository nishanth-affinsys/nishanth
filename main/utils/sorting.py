# function to apply sorting in queryset
from django.db.models.query import QuerySet


def sorting(request, filter_qs):
    ordered_list = filter_qs
    sort_value = request.GET.get("sort")
    sort_type = request.GET.get("sort-type")
    if sort_type == "asc":
        ordered_list = (
            sorted(
                filter_qs,
                key=lambda di: (
                    di[sort_value] is None,
                    (
                        di[sort_value].lower()
                        if isinstance(di[sort_value], str)
                        else (
                            str(di[sort_value]).lower()
                            if isinstance(di[sort_value], list)
                            else (
                                str(di[sort_value]).lower()
                                if isinstance(di[sort_value], QuerySet)
                                else di[sort_value]
                            )
                        )
                    ),
                ),
            )
            if sort_value
            else filter_qs
        )
    elif sort_type == "desc":
        ordered_list = (
            sorted(
                filter_qs,
                key=lambda di: (
                    di[sort_value] is None,
                    (
                        di[sort_value].lower()
                        if isinstance(di[sort_value], str)
                        else (
                            str(di[sort_value]).lower()
                            if isinstance(di[sort_value], list)
                            else (
                                str(di[sort_value]).lower()
                                if isinstance(di[sort_value], QuerySet)
                                else di[sort_value]
                            )
                        )
                    ),
                ),
                reverse=True,
            )
            if sort_value
            else filter_qs
        )

    return ordered_list


"""
To sort particular column of the table chart, either in ascending order or descending order
Pass through query params in API
"""
