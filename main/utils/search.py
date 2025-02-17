# function to apply searching in queryset


def search(request, di):
    search_type = request.GET.get("search_type")
    if search_type == "complete":
        search_value = request.GET.get("search")
        if search_value is None:
            return True
        else:
            search_value = search_value.lower()
            for k, val in di.items():
                if isinstance(val, str) and search_value in val.lower():
                    return True
                elif not isinstance(val, str) and search_value in str(val).lower():
                    return True
            return False
    else:
        search_key = request.GET.get("key")
        search_value = request.GET.get(search_key)
        if search_value is None:
            return True
        else:
            search_value = search_value.lower()
            for k, val in di.items():
                if (
                    isinstance(val, str)
                    and search_value in val.lower()
                    and k == str(search_key)
                ):
                    return True
                elif (
                    not isinstance(val, str)
                    and search_value in str(val).lower()
                    and k == str(search_key)
                ):
                    return True
            return False


"""
funtionality to enable search option in all the table charts.
Pass through query params in API
"""
