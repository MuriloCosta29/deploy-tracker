# ------------------------------------------------------------------------
# Grandson.
# -------------------------------------------------------------------------

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import HealthCheck
from database import get_session
from cache import get_cache, set_cache, delete_cache

# -------------------------------------------------------------------------
router = APIRouter()


# TODO: Create endpoint to view health check history


@router.get("/applications/{id}/healthchecks")
def list_applications_history(id: int, db: Session = Depends(get_session)):
    cached = get_cache(f"healthchecks_app_{id}")
    if cached:
        return cached
    health_check = db.query(HealthCheck).filter(HealthCheck.application_id == id).all()
    set_cache(f"healthchecks_app_{id}", health_check)
    return health_check
