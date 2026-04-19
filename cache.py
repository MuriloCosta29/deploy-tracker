# NOTE: Redis connection for caching layer.
# -------------------------------------------------

import redis
import json

# -------------------------------------------------

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# decode_responses means -> Redis returns strings instead of bytes, which is easier to work with. -------------------------------------------------
# json.dumps() -> Convert Python(dicts and lists) to JSON-string.
# json.loads() -> Convert JSON string back to python

# -------------------------------------------------
# Gets data from Redis by key, important: Returns Python object or none if not found.
# IMPORTANT: I have to convert for strings two(2) reasons
# 1. Redis can only store strings.
# 2. The endpoints returns Python objects (lists, dicts).


def get_cache(key):
    value = r.get(key)  # Search for one key, example: "applications_all"
    if (
        value is not None
    ):  # Redis only saves (String/JSON) | FastAPI needs (Lists/dicts) to work. | I use json.loads to translate the text back into Python.
        new_value = json.loads(value)
        return new_value

    return None


# -------------------------------------------------


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


# -------------------------------------------------


# Converts data to JSON and stores in Redis
# `ex=300` sets the key to expire automatically after 300 seconds(5 minutes).
#
def set_cache(key, data):
    data = [to_dict(item) for item in data]
    value = json.dumps(data, default=str)
    r.set(key, value, ex=300)


# -------------------------------------------------
def delete_cache(key):
    r.delete(key)


# -------------------------------------------------
