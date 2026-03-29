from celery import Celery

# -------------------------------------------------

# the name can't have uppercase or space.
celery_app = Celery(
    "deploy_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)
