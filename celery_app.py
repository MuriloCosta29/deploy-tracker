from celery import Celery
from cache import REDIS_HOST

# -------------------------------------------------

# the name can't have uppercase or space.
celery_app = Celery(
    "deploy_tracker",
    broker=f"redis://{REDIS_HOST}:6379/0",
    backend=f"redis://{REDIS_HOST}:6379/0",
)

# Write about: What is Celery Beat? What the function of Celery Beat?
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
# do the celery when start, import the module `tasks`, and register the tasks are there.

celery_app.conf.timezone = "UTC"
