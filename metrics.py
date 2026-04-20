from prometheus_client import Counter, Histogram

# Uppercase because are constants.

REQUEST_COUNT = Counter(
    "request_count",
    "Total request count",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint", "status"],
)
