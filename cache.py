# NOTE: Redis connection for caching layer.
# -------------------------------------------------

import redis
import json

json = json
# -------------------------------------------------

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# decode_responses means -> Redis returns strings instead of bytes, which is easier to work with.


# -------------------------------------------------
# Gets data from Redis by key, important: Returns Python object or none if not found.
def get_cache(key):
    r.get(key)


# -------------------------------------------------
# Converts data to JSON and stores in Redis
def set_cache(key, data):
    data = get_cache(key)
    json.dumps(data)


# -------------------------------------------------
def delete_cache(key):
    r.delete(key)
