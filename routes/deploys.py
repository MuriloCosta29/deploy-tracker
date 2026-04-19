# NOTE: All endpoints related to the /deploys resource.
# GET /deploys - List all
# GET /deploys/{id} - get one
# POST /deploys - create
# PATCH /deploys/{id} - edit
# DELETE /deploys/{id} - delete

# --------------------------------------------------------------------------------------------

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Deploy
from database import get_session
from schemas import DeployItem
from cache import get_cache, set_cache, delete_cache

# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Son.
# --------------------------------------------------------------------------------


@router.get("/deploys")
def list_deploys(db: Session = Depends(get_session)):
    cached = get_cache("deploys_all")
    if cached:
        return cached
    deploys = db.query(Deploy).all()
    set_cache("deploys_all", deploys)
    return deploys


# --------------------------------------------------------------------------------


@router.get("/deploys/{id}")
def one_deploy(id: int, db: Session = Depends(get_session)):
    deploy_by_id = db.query(Deploy).filter(Deploy.id == id).first()
    return deploy_by_id


# --------------------------------------------------------------------------------
# Important rule! Left = database(Model) | Right = User(Schema)


@router.post("/deploys")
def create_deploy(deploy_data: DeployItem, db: Session = Depends(get_session)):
    new_deploy = Deploy(
        version=deploy_data.version,
        status=deploy_data.status,
        application_id=deploy_data.application_id,
        # 👆 the left side comes from models.py | Right side comes from schemas.py
    )
    db.add(new_deploy)
    db.commit()
    delete_cache("deploys_all")
    db.refresh(new_deploy)
    return new_deploy


# --------------------------------------------------------------------------------


@router.delete("/deploys/{id}")
def delete_deploy(id: int, db: Session = Depends(get_session)):
    del_deploy = db.query(Deploy).filter(Deploy.id == id).first()
    db.delete(del_deploy)
    db.commit()
    delete_cache("deploys_all")
    return del_deploy


# --------------------------------------------------------------------------------


# WARNING: Revise this!!!
@router.patch("/deploys/{id}")
def change_deploy(id: int, deploy_data: DeployItem, db: Session = Depends(get_session)):
    changing_deploy = db.query(Deploy).filter(Deploy.id == id).first()
    changing_deploy.version = deploy_data.version
    changing_deploy.status = deploy_data.status
    changing_deploy.application_id = deploy_data.application_id
    db.commit()
    delete_cache("deploys_all")
    db.refresh(changing_deploy)
    return changing_deploy
