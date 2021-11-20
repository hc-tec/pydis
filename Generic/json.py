
import json


def convert_to_builtin_type(obj):
    if isinstance(obj, list):
        data = []
        for o in obj:
            data.append(convert_to_builtin_type(o))
        return data
    try:
        return obj.__dict__
    except AttributeError:
        return None


def json_dumps(obj):
    try:
        return json.dumps(obj)
    except TypeError:
        return json.dumps(obj, default=convert_to_builtin_type)


def json_loads(obj):
    return json.loads(obj)
