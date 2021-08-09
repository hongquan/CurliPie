import json
import functools


JSONDecodeError = json.JSONDecodeError

try:
    import orjson  # noqa

    def orjson_dump(o):
        return orjson.dumps(o).decode()
    json_dump = orjson_dump
    json_load = orjson.loads
    JSONDecodeError = orjson.JSONDecodeError
except ModuleNotFoundError:
    try:
        import rapidjson
        json_dump = functools.partial(rapidjson.dumps, ensure_ascii=False)
        json_load = rapidjson.loads
        JSONDecodeError = rapidjson.JSONDecodeError
    except ModuleNotFoundError:
        import json
        json_dump = functools.partial(json.dumps, ensure_ascii=False, separators=(',', ':'))
        json_load = json.loads
