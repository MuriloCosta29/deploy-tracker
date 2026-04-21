import requests
from celery_app import celery_app
from database import SessionLocal
from models import Application, HealthCheck
# -------------------------------------------------
# 200 -> OK | 404 -> Not Found | 500 -> Error
# -------------------------------------------------


@celery_app.task
def health_checker(application_id):
    db = SessionLocal()
    app_class = db.query(Application).filter(Application.id == application_id).first()
    response = requests.get(app_class.url)  # Get the application url
    status_code = response.status_code
    is_up = status_code == 200

    time = response.elapsed.total_seconds()  # Time it took the website to respond.

    new_check = HealthCheck(
        application_id=application_id,
        status=is_up,
        http_code=response.status_code,
        response_time=time,
    )

    db.add(new_check)
    db.commit()
    db.close()  # Need to close manually, because i don't have `get_session` to close the session automatically.
