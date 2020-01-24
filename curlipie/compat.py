
try:
    import orjson

    def orjson_dump(o):
        return orjson.dumps(o).decode()
    json_dump = orjson_dump
    json_load = orjson.loads
except ImportError:
    import rapidjson
    json_dump = rapidjson.dumps
    json_dump = rapidjson.dumps
