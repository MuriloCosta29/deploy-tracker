from prometheus_client import Counter, Gauge, Histogram

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

HEALTH_CHECK_UP = Gauge(
    "health_check_up",
    "Whether the application is up (1) or down (0)",
    ["application_id"],
)
