import functools

try:
    import orjson

    def orjson_dump(o):
        return orjson.dumps(o).decode()
    json_dump = orjson_dump
    json_load = orjson.loads
except ModuleNotFoundError:
    try:
        import rapidjson
        json_dump = functools.partial(rapidjson.dumps, ensure_ascii=False)
        json_load = rapidjson.loads
    except ModuleNotFoundError:
        import json
        json_dump = functools.partial(json.dumps, ensure_ascii=False, separators=(',', ':'))
        json_load = json.loads
