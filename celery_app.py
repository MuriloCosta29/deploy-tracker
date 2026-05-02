from celery import Celery
import os


# -------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

required_envs = {
    "REDIS_HOST": REDIS_HOST,
    "REDIS_PORT": REDIS_PORT,
}

missing_envs = [name for name, value in required_envs.items() if value is None]

if missing_envs:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_envs)}"
    )
# -------------------------------------------------
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
# -------------------------------------------------
celery_app = Celery(
    "deploy_tracker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
# -------------------------------------------------

celery_app.conf.beat_schedule = {
    "health_check_30s": {
        "task": "tasks.health_checker",
        "schedule": 30.0,  # seconds
        "args": (1,),
    },
}

celery_app.conf.include = ["tasks"]
# Auto-discover tasks from tasks.py

celery_app.conf.timezone = "UTC"
