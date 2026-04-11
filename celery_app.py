from celery import Celery

# -------------------------------------------------

# the name can't have uppercase or space.
celery_app = Celery(
    "deploy_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

# Write about: What is Celery Beat? What the function of Celery Beat?
celery_app.conf.beat_schedule = {
    "health_check_30s": {
        "task": "tasks.health_checker",
        "schedule": 30.0,  # seconds
        "args": (1,),
    },
}

celery_app.conf.include = ["tasks"]
# do the celery when start, import the module `tasks`, and register the tasks are there.

celery_app.conf.timezone = "UTC"
