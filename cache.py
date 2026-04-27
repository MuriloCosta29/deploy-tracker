# NOTE: Redis connection for caching layer.
# -------------------------------------------------

import redis
import json
import os

# -------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
# -------------------------------------------------
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
# decode_responses means -> Redis returns strings instead of bytes, which is easier to work with.
# --------------------------------------------------


def get_cache(key):
    value = r.get(key)
    if value is not None:
        new_value = json.loads(value)
        return new_value

    return None


# -------------------------------------------------


def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


# -------------------------------------------------


def set_cache(key, data):
    data = [to_dict(item) for item in data]
    value = json.dumps(data, default=str)
    r.set(key, value, ex=300)


# -------------------------------------------------


def delete_cache(key):
    r.delete(key)


# -------------------------------------------------
