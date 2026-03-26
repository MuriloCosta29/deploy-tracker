# NOTE: Redis connection for caching layer.

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# decode_responses means -> Redis returns strings instead of bytes, which is easier to work with.
