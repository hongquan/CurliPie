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
        json_dump = rapidjson.dumps
        json_load = rapidjson.loads
    except ModuleNotFoundError:
        import json
        json_dump = functools.partial(json.dumps, separators=(',', ':'))
        json_load = json.loads
