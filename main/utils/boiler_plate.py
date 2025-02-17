from main.utils.search import search
from main.utils.sorting import sorting
from functools import partial

from rest_framework.response import Response
from main.utils.pagination import get_paginated_response
from main.utils.export import export_csv, export_pdf, export_excel
from main.settings import MAX_PDF_LIMIT


# Used to set the number of records in pdf to be downloaded


# Function performing searching and sorting in the queryset
def search_and_sort(request, q):
    items = q
    search_func = partial(search, request)
    filter_qs = list(filter(search_func, list(items)))
    s = sorting(request, filter_qs)
    return s


# Boiler template for getting the queryset
def get_queryset_from_request(
    serializers, models1, request, db_schema, *args, **kwargs
):
    serializer = serializers(data=request.data)
    serializer.is_valid(raise_exception=True)
    i = models1.objects.using(db_schema).filter(**serializer.validated_data)
    return i


def query(request, models, serializers, db_schema):
    return get_queryset_from_request(serializers, models, request, db_schema)


def return_count(items):
    return Response(data={"count": items})


def return_table(items, request):
    response_item = search_and_sort(request, items)
    return get_paginated_response(response_item, request)


def get_formatted_params(params: dict):
    if not params.get("values"):
        params.update(values=[])
    if not params.get("values_kwargs"):
        params.update(values_kwargs={})
    if not params.get("annotate"):
        params.update(annotate={})
    if not params.get("exclude"):
        params.update(exclude={})
    if not params.get("filter_args"):
        params.update(filter_args=[])
    if not params.get("filter_kwargs"):
        params.update(filter_kwargs={})
    if not params.get("order_by"):
        params.update(order_by=[])
    if not params.get("distinct_args"):
        params.update(distinct_args=[])
    if not params.get("pdf_kwargs"):
        params.update(pdf_kwargs={})
    if not params.get("csv_kwargs"):
        params.update(csv_kwargs={})
    return params


def get_generic_response(params):
    params = get_formatted_params(params)
    get_qs = query(
        params.get("request"),
        params.get("models"),
        params.get("serializers"),
        params.get("db_schema"),
    )
    if params.get("distinct_args"):
        filtered_qs = (
            get_qs.filter(*params.get("filter_args"), **params.get("filter_kwargs"))
            .exclude(**params.get("exclude"))
            .values(*params.get("values"), **params.get("values_kwargs"))
            .annotate(**params.get("annotate"))
            .order_by(*params.get("order_by"))
            .distinct(*params.get("distinct_args"))
        )
    else:
        filtered_qs = (
            get_qs.filter(*params.get("filter_args"), **params.get("filter_kwargs"))
            .exclude(**params.get("exclude"))
            .values(*params.get("values"), **params.get("values_kwargs"))
            .annotate(**params.get("annotate"))
            .order_by(*params.get("order_by"))
        )

    if params.get("distinct"):
        filtered_qs = filtered_qs.distinct()

    if params.get("pdf_kwargs") and len(params.get("pdf_kwargs")) > 0:
        if len(filtered_qs) > MAX_PDF_LIMIT:
            filtered_qs = filtered_qs[:MAX_PDF_LIMIT]
        return export_pdf(filtered_qs, **params.get("pdf_kwargs"))

    if params.get("csv_kwargs") and len(params.get("csv_kwargs")) > 0:
        return export_csv(filtered_qs, **params.get("csv_kwargs"))

    if params.get("excel_kwargs") and len(params.get("excel_kwargs")) > 0:
        return export_excel(filtered_qs, **params.get("excel_kwargs"))

    if params.get("query_set"):
        if params.get("count") and params.get("distinct"):
            filtered_qs = filtered_qs.distinct().count()
            return filtered_qs
        elif params.get("count") and params.get("distinct") and params.get("aggregate"):
            filtered_qs = (
                filtered_qs.distinct().count().aggregate(**params.get("aggregate"))
            )
            return filtered_qs
        elif params.get("count") and params.get("aggregate"):
            filtered_qs = filtered_qs.count().aggregate(**params.get("aggregate"))
            return filtered_qs
        elif params.get("aggregate"):
            filtered_qs = filtered_qs.aggregate(**params.get("aggregate"))
            return filtered_qs
        elif params.get("count"):
            filtered_qs = filtered_qs.count()
            return filtered_qs
        else:
            return filtered_qs
    else:
        if params.get("count") and params.get("distinct"):
            filtered_qs = filtered_qs.distinct().count()
            return return_count(filtered_qs)
        elif params.get("count") and params.get("distinct") and params.get("aggregate"):
            filtered_qs = (
                filtered_qs.distinct().count().aggregate(**params.get("aggregate"))
            )
            return return_count(filtered_qs)
        elif params.get("count") and params.get("aggregate"):
            filtered_qs = filtered_qs.count().aggregate(**params.get("aggregate"))
            return return_count(filtered_qs)
        elif params.get("aggregate"):
            filtered_qs = filtered_qs.aggregate(**params.get("aggregate"))
            return return_count(filtered_qs)
        elif params.get("count"):
            filtered_qs = filtered_qs.count()
            return return_count(filtered_qs)
        elif params.get("not_paginated"):
            return Response(filtered_qs)
        else:
            return return_table(filtered_qs, params.get("request"))


"""
get_generic_response function is to generate the generic reponse which will be used by all the charts functions, it takes params as a parameter, and
based on params it returns the filtered queryset. It will handle all types of charts i.e., either count, or table

It calls get_formatted_params function and query function where  get_formatted_params functions checks for the required field needed for particular 
charts and update the param, and query fucntion returns the general querset with the basic filter functionality (time and channel)

"""
