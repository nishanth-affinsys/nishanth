import os
import django
from django.core import serializers
from main.settings import BASE_DIR


def create_fixture(model, dbschema, count):
    n = model.objects.using(dbschema).count()
    if n > count:
        n = n - count
    queryset = model.objects.using(dbschema).all()[n:]
    data = serializers.serialize("json", queryset)
    f = open(f"{BASE_DIR}/tests/fixtures/{model._meta.model_name}.json", "w")
    f.write(data)
    f.close()
