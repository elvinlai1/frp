import json

from django.db.models import QuerySet


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, QuerySet):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
