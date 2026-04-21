from prometheus_client import Counter, Gauge, Histogram

# Uppercase because are constants.
# WARNING: Problem with Grafana! Don't showing HEALTH_CHECK_COUNT.
# • The problem occurs, because FastAPI runs in one process and Celery worker in another process i.e  -> Two separate process.
# • Each has its own copy of the metric when Celery increments your copy, the Prometheus scrapes the FastAPI copy.


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
