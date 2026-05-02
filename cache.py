# NOTE: Redis connection for caching layer.
# -------------------------------------------------

import redis
import json
import os

# -------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

required_envs = {
    "REDIS_HOST": REDIS_HOST,
    "REDIS_PORT": REDIS_PORT,
}

missings_env = [name for name, value in required_envs.items() if value is None]

if missings_env:
    raise RuntimeError(
        f"Missing required environments variables: {', '.join(missings_env)}"
    )

# -------------------------------------------------
r = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True)
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
