# NOTE: All endpoints related to the /applications resource

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Application
from database import get_session
from schemas import ApplicationItem
from cache import get_cache, set_cache, delete_cache

# Route files create routers -- Smaller groups of routes that plug into the
# main.app
# GET /applications - List all
# GET /applications/{id} - get one
# POST /applications - create
# PATCH /applications/{id} - edit
# DELETE /applications/{id} - delete
# -------------------------------------------------------------------------------
router = APIRouter()

# -------------------------------------------------------------------------------


@router.get("/applications")
def list_applications(db: Session = Depends(get_session)):
    cached = get_cache("applications_all")
    if cached:
        return cached
    applications = db.query(Application).all()
    set_cache("applications_all", applications)
    return applications


# -------------------------------------------------------------------------------


@router.get("/applications/{id}")
def one_application(id: int, db: Session = Depends(get_session)):
    one_application = db.query(Application).filter(Application.id == id).first()
    return one_application


# -------------------------------------------------------------------------------


@router.post("/applications")
def create_application(
    application_data: ApplicationItem, db: Session = Depends(get_session)
):
    new_app = Application(name=application_data.name, url=application_data.url)
    db.add(new_app)
    db.commit()
    delete_cache("applications_all")
    db.refresh(new_app)
    return new_app


# -------------------------------------------------------------------------------


@router.delete("/applications/{id}")
def delete_application(id: int, db: Session = Depends(get_session)):
    del_app = db.query(Application).filter(Application.id == id).first()
    db.delete(del_app)
    db.commit()
    delete_cache("applications_all")
    return del_app


# ------------------------------------------------------------------------------------------------


@router.patch("/applications/{id}")
def change_app(
    id: int, application_data: ApplicationItem, db: Session = Depends(get_session)
):
    changing_app = db.query(Application).filter(Application.id == id).first()
    changing_app.name = application_data.name
    changing_app.url = application_data.url
    db.commit()
    delete_cache("applications_all")
    db.refresh(changing_app)
    return changing_app
