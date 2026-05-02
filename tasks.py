import requests
from celery_app import celery_app
from database import SessionLocal
from models import Application, HealthCheck

# -----------------------------------------------------


def check_single_application(db, application):
    try:
        response = requests.get(application.url, timeout=5)
        status = response.status_code == 200
        http_code = response.status_code
        response_time = response.elapsed.total_seconds()
    except requests.RequestException:
        status = False
        http_code = 0
        response_time = 0

    new_check = HealthCheck(
        application_id=application.id,
        status=status,
        http_code=http_code,
        response_time=response_time,
    )

    db.add(new_check)
    db.commit()


# -----------------------------------------------------


@celery_app.task
def check_all_applications():
    db = SessionLocal()
    try:
        applications = db.query(Application).all()

        for application in applications:
            check_single_application(db, application)
    finally:
        db.close()
