from celery import Celery
from cache import REDIS_HOST

# -------------------------------------------------

celery_app = Celery(
    "deploy_tracker",
    broker=f"redis://{REDIS_HOST}:6379/0",
    backend=f"redis://{REDIS_HOST}:6379/0",
)

celery_app.conf.beat_schedule = {
    "health_check_30s": {
        "task": "tasks.health_checker",
        "schedule": 30.0,  # seconds
        "args": (
            1,
        ),  # TODO: Dynamically check all registered applications instead of hardcoded id
    },
}

celery_app.conf.include = ["tasks"]
# Auto-discover tasks from tasks.py

celery_app.conf.timezone = "UTC"
