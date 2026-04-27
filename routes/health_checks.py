# NOTE: All endpoints related to the /healthchecks resource.
# -------------------------------------------------------------------------

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import HealthCheck
from database import get_session
from cache import get_cache, set_cache
from metrics import HEALTH_CHECK_UP

# -------------------------------------------------------------------------

router = APIRouter()

# -------------------------------------------------------------------------


@router.get("/applications/{id}/healthchecks")
def list_applications_history(id: int, db: Session = Depends(get_session)):
    cached = get_cache(f"healthchecks_app_{id}")
    if cached:
        return cached
    health_check = db.query(HealthCheck).filter(HealthCheck.application_id == id).all()
    if health_check:
        latest = health_check[-1]
        if latest.status:
            HEALTH_CHECK_UP.labels(application_id=str(id)).set(1)
        else:
            HEALTH_CHECK_UP.labels(application_id=str(id)).set(0)

    set_cache(f"healthchecks_app_{id}", health_check)

    return health_check
